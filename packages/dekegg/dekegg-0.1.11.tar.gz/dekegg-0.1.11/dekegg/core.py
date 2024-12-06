import os
import sys
import glob
import tempfile
from dektools.file import normal_path, write_file, remove_path
from dektools.zip import decompress_files


def build_egg(path_project, bdist='bdist_egg', pyc=False):
    cwd = os.getcwd()
    os.chdir(path_project)
    path_out = tempfile.mkdtemp(prefix='dekegg-build_egg-out')
    os.system(' '.join(
        [
            sys.executable,
            "setup.py",
            "clean",
            "-a", bdist,  # bdist_egg , bdist_fullegg
            " --exclude-source-files" if pyc else "",
            "-d", path_out
        ]
    ))
    os.chdir(cwd)
    path_egg = glob.glob(os.path.join(path_out, "*.egg"))[0]
    path_egg = write_file(None, t=True, m=path_egg)
    remove_path(path_out)
    return path_egg


def is_egg(path_file):
    return os.path.splitext(path_file)[1].lower() == '.egg' and os.path.isfile(path_file)


def sure_egg_path(path):
    path = normal_path(path)
    if os.path.exists(path):
        return path
    cursor = path
    while True:
        if not is_egg(cursor):
            dirname = os.path.dirname(cursor)
            if dirname == cursor:
                break
            else:
                cursor = dirname
        else:
            return decompress_files(cursor) + path[len(cursor):]
    raise FileNotFoundError(path)
