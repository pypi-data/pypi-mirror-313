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

'''
The purpose of this file is to allow modules outside of trosnoth.welcome
to access functions that are common to trosnoth.welcome without risking
importing Qt if it's not already there.

This module MUST NOT import PySide6, either directly or indirectly.
'''
import asyncio
import contextlib
import functools
import logging
import sys

from trosnoth import data

log = logging.getLogger(__name__)


ICON_FILE = data.base_path / 'welcome' / 'icon.png'

TUTOR_IMAGE_FILE = data.base_path / 'welcome' / 'tutor.png'
WAITING_IMAGE_FILE = data.base_path / 'welcome' / 'tutor.png'
STOP_IMAGE_FILE = data.base_path / 'welcome' / 'stop.png'
QUESTION_IMAGE_FILE = data.base_path / 'welcome' / 'question.png'


def hide_qt_windows():
    if 'PySide6.QtCore' in sys.modules:
        from trosnoth.welcome.common import hide_qt_windows as hide
        return hide()
    return empty_context_manager()


@contextlib.contextmanager
def empty_context_manager():
    yield


class AsyncCallbackManager:
    def __init__(self):
        self.tasks = set()

    def start_coroutine(self, coro):
        task = asyncio.create_task(coro)
        self.tasks.add(task)
        task.add_done_callback(self.task_done)
        return task

    def task_done(self, future):
        self.tasks.remove(future)
        try:
            future.result()
        except asyncio.CancelledError:
            pass
        except Exception:
            log.exception('Exception in async task')

    def cancel_all(self):
        for task in list(self.tasks):
            if not task.done():
                task.cancel()


class HasAsyncCallbacks:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.async_manager = AsyncCallbackManager()


def async_callback(fn):
    @functools.wraps(fn)
    def wrapper(self: HasAsyncCallbacks, *args, **kwargs):
        return self.async_manager.start_coroutine(fn(self, *args, **kwargs))
    return wrapper


def run_callback_in_async_loop(fn, *fixed_args):
    # Sometimes on Windows, Qt events interrupt running code. To fix
    # this, we wrap callbacks in this function.
    try:
        initial_loop = asyncio.get_running_loop()
    except RuntimeError:
        initial_loop = None

    def callback(*args):
        loop = initial_loop or asyncio.get_running_loop()
        loop.call_soon_threadsafe(fn, *(fixed_args + args))

    return callback
