from setuptools import find_packages
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install
from scripts.sqlcipher_compile import  SqlcipherCompiler
from scripts.utils import (
    copy_sqlite_module_and_replace_name, replace_text_in_file, 
    get_github_release_info,download_and_extract_to,inset_content_to_file,
    patten_is_in_file_content
)
import os,sys
import shutil

module_name = 'CryptoSqlite'


def prepare_sqlite3_module_source(build_folder:str):

    # Download cpython source code according to the current python version
    cpython_download_url, _ = get_github_release_info('python', 'cpython',f'v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')
    pysrcfoler = download_and_extract_to(cpython_download_url, build_folder)

    sqlite_c_code_folder = os.path.join(build_folder, pysrcfoler,'Modules', '_sqlite')

    # Change py module nameex
    copy_sqlite_module_and_replace_name(os.path.join(build_folder, pysrcfoler,'Lib', 'sqlite3'), module_name)
    
    # Change c module name
    replace_text_in_file(os.path.join(sqlite_c_code_folder, 'module.c'),'_sqlite3', f"_{module_name}")
    replace_text_in_file(os.path.join(sqlite_c_code_folder, 'module.h'),'_sqlite3', f"_{module_name}")

    need_define_marco= False
    if patten_is_in_file_content(os.path.join(sqlite_c_code_folder, 'module.h'), "MODULE_NAME"):
        replace_text_in_file(os.path.join(sqlite_c_code_folder, 'module.h'),'MODULE_NAME "sqlite3"', f'MODULE_NAME "{module_name}"')
    else:
        need_define_marco = True


    sqlite_c_codes = [os.path.join(r, f) for r,p,fs in os.walk(sqlite_c_code_folder) for f in fs if f.endswith('.c')]
    return pysrcfoler, sqlite_c_code_folder,sqlite_c_codes,need_define_marco


class CustomBuildExt(build_ext):
    
    def __init__(self, dist):
        super().__init__(dist)
        self.build_folder = self.distribution.get_command_obj('build').build_base

        sqlite_src_folder,sqlite_c_code_folder,sqlite_c_codes,need_define_marco = prepare_sqlite3_module_source(self.build_folder)

        self.need_define_marco = need_define_marco
        self.distribution.ext_modules = [
            Extension(f"_{module_name}", sources=sqlite_c_codes,include_dirs=[
                    # sqlite_src_folder,
                    os.path.join(sqlite_src_folder,'Include', 'internal')
                ]
            )
        ]


    def get_ext_filename(self, ext_name):

        return os.path.join(module_name, super().get_ext_filename(ext_name))

    def run(self):

        SQLCIPHER_INCLUDE_DIRS = None
        SQLCIPHER_LIBRARY_DIRS = None
        SQLCIPHER_VERSION = os.environ.get('SQLCIPHER_VERSION', None)
        if not SQLCIPHER_VERSION:
            SQLCIPHER_INCLUDE_DIRS = os.environ.get('SQLCIPHER_INCLUDE_DIRS', None)
            SQLCIPHER_LIBRARY_DIRS = os.environ.get('SQLCIPHER_LIBRARY_DIRS', None)
        
        if not SQLCIPHER_INCLUDE_DIRS:
            sqlcipher_download_url,_ = get_github_release_info('sqlcipher','sqlcipher',SQLCIPHER_VERSION)
            sqlcipher_folder =  download_and_extract_to(sqlcipher_download_url,self.build_folder)

            sqlcipher_lib_path,dllbasename,dllname = SqlcipherCompiler(os.path.join(self.build_folder, sqlcipher_folder)).compile()
            sqlcipher_inc_path = sqlcipher_lib_path
        else:
            sqlcipher_inc_path = SQLCIPHER_INCLUDE_DIRS
            sqlcipher_lib_path = SQLCIPHER_LIBRARY_DIRS
            dllbasename = 'sqlcipher'

        for ext in self.extensions:
            ext.libraries.append(dllbasename)
            ext.include_dirs.append(sqlcipher_inc_path)
            ext.library_dirs.append(sqlcipher_lib_path)

        if os.name == 'posix':
            ext.extra_link_args.append('-Wl,-rpath,.')
            inset_content_to_file(os.path.join(self.build_lib, module_name, '__init__.py'),
                            f'import os,ctypes\nctypes.CDLL(os.path.join(os.path.abspath(os.path.dirname(__file__)), "{dllname}"))\n',
                            lambda x: x.startswith('from'))

        
        if self.need_define_marco:
            ext.define_macros.append(('MODULE_NAME',f'"{module_name}"'))
            
        super().run()

        shutil.copyfile(os.path.join(sqlcipher_lib_path, dllname), os.path.join(self.build_lib,module_name,dllname))



class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        shutil.rmtree('build')


with open("README.md", "r", encoding="utf-8") as f:
  long_description = f.read()

setup(
    name=module_name,
    version='0.0.3',
    ext_modules=[Extension("faker",sources=[])],
    cmdclass={
        'build_ext': CustomBuildExt,
        'install':CustomInstallCommand
    },
    url='https://github.com/Quenwaz/CryptoSqlite',
    description='python version of sqlcipher',
    long_description=long_description,
    author='zkh',
    author_email='404937333@qq.com',
    keywords="sqlite3, cipher",
    setup_requires=["cython"],
    install_requires=[],
    long_description_content_type='text/markdown',
    packages=find_packages(where="."),
    platforms=["Windows", "Linux"],
    license='MIT License',
    python_requires=">=3.7,<4.0",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
