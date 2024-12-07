from setuptools.command.build_ext import build_ext
from distutils.dist import Distribution
from distutils import util
from distutils import ccompiler
import subprocess
import sys,os


class SqlcipherCompiler(build_ext):

    def __init__(self, srcfolder, dllbasename = "sqlcipher"):
        super().__init__(Distribution())
        self.srcfolder = srcfolder
        self.dstfolder = srcfolder
        self.dllbasename = dllbasename
        self.env_sep = ";"
        self.is_windows = True
        if sys.platform == 'win32':
            
            self.dllname = f"{dllbasename}.dll"
            python_library_path = os.path.join(os.path.dirname(sys.executable), 'Library')
            libraries = ["libssl.lib","libcrypto.lib"]
        elif sys.platform == 'linux' or sys.platform == 'linux2':
            self.is_windows = False
            self.env_sep = ":"
            self.dllname = f"lib{dllbasename}.so.0"
            self.dstfolder = srcfolder + "/.libs"
            python_library_path = os.path.dirname(sys.executable)
            if not os.path.exists(os.path.join(python_library_path, "lib")):
                python_library_path = os.path.dirname(python_library_path)
            libraries = ["libcrypto.a"]
            static_libraries = os.path.join(python_library_path, 'lib',"libcrypto.a")
        self.include_dirs = [os.path.join(python_library_path, 'include')]
        self.library_dirs = [os.path.join(python_library_path, 'lib')]
        self.libraries = libraries

    def get_compile_cmd(self):

        if sys.platform == 'win32':
            return [
                {
                    "args": f'nmake /f Makefile.msc {self.dllname} \
                            EXT_FEATURE_FLAGS="-DSQLITE_HAS_CODEC -DSQLITE_TEMP_STORE=3" LTLIBS="{" ".join(self.libraries)}" \
                            SQLITE3DLL="{self.dllname}"'
                }
            ]
        else:
            return [
                {
                    "shell": True,
                    "args":f'./configure --enable-tempstore=yes CFLAGS="-DSQLITE_HAS_CODEC {" ".join(["-I" + p for p in self.include_dirs])}" LIB="{" ".join(["-l"+p for p in self.libraries])}" LDFLAGS="{" ".join(["-L" + p for p in self.library_dirs])}"'
                },
                {
                    "args": 'make'
                }
                ]
            
    
    def set_or_update_env(self, key, val):
        oldenv = {
            key: os.environ.get(key)
        }
        os.environ[key] = f"{oldenv[key]};{val}"
        return oldenv
    
    def restore_env(self, oldenvs:dict):
        for k, v in oldenvs.items():
            os.environ[k] =v if v else ''


    def compile(self):
        """

            Returns: (install folder, dllbasename, dllname)
        """
        compiler = ccompiler.new_compiler()
        if os.name == 'nt' and self.plat_name != util.get_platform():
            compiler.initialize(self.plat_name)

        oldenvs = dict()
        oldenvs.update(self.set_or_update_env('INCLUDE',self.env_sep.join(compiler.__class__.include_dirs + self.include_dirs)))
        oldenvs.update(self.set_or_update_env('LIB',self.env_sep.join(compiler.__class__.library_dirs + self.library_dirs)))
        if self.is_windows:
            oldenvs.update(self.set_or_update_env('PATH',compiler._paths))

        for cmd in self.get_compile_cmd():
            subprocess.check_call(**cmd,cwd=self.srcfolder)
        
        self.restore_env(oldenvs)
        return self.dstfolder,self.dllbasename,self.dllname
    
    def compile_with_meson(self):
        # require meson module
        subprocess.check_call(['meson', 'setup', 'build',f'-Dsqlcipher_folder={self.srcfolder}',"--reconfigure"])
        subprocess.check_call(['ninja', '-C', 'build', '-v'])


__all__ = ['SqlcipherCompiler']

