import os
import sys
from dektools.file import read_text
from dektools.sys import sys_paths_relative
from .constants import dir_name_venv


def activate_venv(path_venv=None, ignore=False):
    path_venv = path_venv or dir_name_venv
    path_scripts = sys_paths_relative(path_venv)['scripts']
    this_file = os.path.join(path_scripts, 'activate_this.py')
    if not ignore or os.path.isfile(this_file):
        exec(read_text(this_file), {'__file__': this_file})


def is_venv_active(sp=None):
    return (sp or sys.prefix) != sys.base_prefix
