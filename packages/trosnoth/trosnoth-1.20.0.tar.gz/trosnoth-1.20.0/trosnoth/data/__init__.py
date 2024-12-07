# Trosnoth (Ubertweak Platform Game)
# Copyright (C) Joshua D Bartlett
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import os
import sys
from pathlib import Path

user = object()     # Used to write/read user data.

USERROOT = os.path.expanduser('~')
USERHOME = os.path.join(USERROOT, '.trosnoth')


def getPath(module, *bits):
    if module is user:
        return getUserPath(*bits)

    if isinstance(module, bytes):
        module = module.decode('ascii')
    if isinstance(module, str):
        bits = (module,) + bits
        module = sys.modules['trosnoth.data']

    if _datapath is None:
        return os.path.join(os.path.dirname(module.__file__), *bits)
    return os.path.join(_datapath, '_internal', module.__name__.replace('.', '/'), *bits)


def getUserPath(*bits):
    makeDirs(USERHOME)
    return os.path.join(USERHOME, *bits)


def makeDirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


# Check whether this is within py2exe/pyinstaller
def get_exe_dir():
    import sys
    if getattr(sys, 'frozen', False) or hasattr(sys, 'importers'):
        return os.path.dirname(sys.executable)
    return None


def get_overridable_path(relative_path):
    for base in (user_path, base_path):
        if os.path.exists(base / relative_path):
            return base / relative_path
    raise FileNotFoundError(base_path / relative_path)


_datapath = get_exe_dir()
base_path = Path(__file__).parent if _datapath is None else Path(_datapath) / '_internal' / 'trosnoth' / 'data'
user_path = Path(USERHOME)
try:
    user_path.mkdir(parents=True, exist_ok=True)
except IOError:
    pass
