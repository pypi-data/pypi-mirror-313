
import tarfile
import os
import shutil

def progress_hook(blocknum, block_size, total_size):
    progress_percent = 100.0 * blocknum * block_size / total_size
    print(f"\rdownloading:{progress_percent:.2f}%",end="")


def get_tar_first_level_dir(tar_file_path):
    first_level_dir = None

    with tarfile.open(tar_file_path, 'r') as tar:
        members = tar.getmembers()

        for member in members:
            if member.isdir():
                first_level_dir = member.name
                break

    return first_level_dir

def download_and_extract_to(url:str, dst:str):
    import urllib.request
    import tempfile

    url_pieces = url.split('/')
    name = f"{url_pieces[5]}-{url_pieces[-1]}.tar.gz"
    save_to = os.path.join(tempfile.gettempdir(), name)
    urllib.request.urlretrieve(url, save_to,reporthook = progress_hook)
    folername = get_tar_first_level_dir(save_to)
    with tarfile.open(save_to, 'r:gz') as tar: 
        tar.extractall(path=dst)

    return folername


def get_github_release_info(owner, repo,ver:str=None):
    import urllib.request
    import json

    perpage = 100
    download_url = None
    download_hash = None
    for curpage in range(1,1000):
        url = f"https://api.github.com/repos/{owner}/{repo}/tags?page={curpage}&per_page={perpage}"
        
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/vnd.github+json')
        
        with urllib.request.urlopen(req) as response:
            data = json.load(response)
            if len(data) == 0:
                raise Exception('specify version not found.')
            
            if ver == None:
                ret = data[:1]
            else:
                ret = list(filter(lambda k: k['name'] == ver, data))

            if len(ret) > 0:
                download_url = ret[0]['tarball_url']
                download_hash = ret[0]['commit']['sha']
                break

    return download_url, download_hash

def inset_content_to_file(file_path, content, cond):
    with open(file_path, 'r') as file:
        content_lines = file.readlines()
    
    pos  = -1
    for idx,line in enumerate(content_lines):
        if cond(line):
            pos = idx
            break

    if pos == -1:
        return
    
    content_lines = content_lines[:pos] + [content] + content_lines[pos:]

    with open(file_path, 'w') as file:
        file.write("".join(content_lines))

def patten_is_in_file_content(file_path, pattern:str):
    with open(file_path, 'r',encoding="utf-8") as file:
        file_data = file.read()

    return file_data.find(pattern) != -1

def replace_text_in_file(file_path, old_text, new_text):
    with open(file_path, 'r',encoding="utf-8", errors='ignore') as file:
        file_data = file.read()

    new_file_data = file_data.replace(old_text, new_text)

    with open(file_path, 'w',encoding="utf-8") as file:
        file.write(new_file_data)

def copy_sqlite_module_and_replace_name(src, dst):
    for root, folders, files in os.walk(src):
        relroot = os.path.relpath(root, src)


        dstfolder = os.path.join(dst, relroot) if relroot != '.' else dst
        os.makedirs(dstfolder,exist_ok=True)
        for f in files:
            dstfile = os.path.join(dstfolder, f)
            if os.path.exists(dstfile):
                os.remove(dstfile)
            shutil.copyfile(os.path.join(root, f), dstfile)
            print(dstfile)
            replace_text_in_file(dstfile,'_sqlite3', f" {dst}._{dst}")
            replace_text_in_file(dstfile,'sqlite3', dst)