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
# 02110-1301, USA
import asyncio
import os
import sys
import traceback

from twisted.internet import asyncioreactor


def install_async_qt_reactor():
    '''
    Installs the asyncio/Qt/Twisted main loop. This will not work if a
    different Twisted reactor has already been installed.
    '''
    install_certificate_authorities()

    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication

    os.environ['QT_API'] = 'pyside6'

    from asyncqt import QSelectorEventLoop      # Must come after PySide6 import

    # Fix font and scaling issues: Qt5 tries its best to work on high
    # DPI monitors, but it ends up scaling text and other UI elements
    # differently, resulting in an ugly and partly unusable UI. The
    # simplest way to get around this is to tell Qt to just use 96 DPI
    # everywhere.
    QApplication.setAttribute(Qt.AA_Use96Dpi)
    # Due to https://bugreports.qt.io/browse/QTBUG-78609, on Windows the
    # font scaling doesn't respect AA_Use96Dpi, so we need to use this
    # development flag to look consistent across platforms.
    os.environ['QT_FONT_DPI'] = '96'

    loop = QSelectorEventLoop(QApplication())
    asyncio.set_event_loop(loop)
    asyncioreactor.install(loop)


_twisted_reactor_intentionally_chosen = False


def declare_twisted_reactor_was_intentionally_chosen():
    '''
    Use this if you need to import a module that calls
    declare_this_module_requires_qt_reactor, but you don't want to
    install the asyncio/Qt/Twisted main loop.
    '''
    global _twisted_reactor_intentionally_chosen
    _twisted_reactor_intentionally_chosen = True


def declare_this_module_requires_qt_reactor():
    '''
    This should be called before any direct or indirect Twisted imports
    in any module that requires the asyncio/Qt/Twisted main loop to be
    installed.

    If declare_twisted_reactor_was_intentionally_chosen() has been
    previously called, this call will do nothing.
    Otherwise, this function will install the asyncio/Qt/Twisted main
    loop if possible, and raise RuntimeError otherwise (e.g., if a
    different Twisted reactor has already been installed.)
    '''
    if _twisted_reactor_intentionally_chosen:
        return

    reactor = sys.modules.get('twisted.internet.reactor')
    if not reactor:
        install_async_qt_reactor()
        return

    if not isinstance(reactor, asyncioreactor.AsyncioSelectorReactor):

        raise RuntimeError(
            'Could not install the asyncio/Qt/Twisted main loop because a Twisted reactor has '
            'already been installed. You can fix this by:\n'
            ' * calling declare_this_module_requires_qt_reactor() before any Twisted imports '
            f'(probably early in {traceback.extract_stack()[0].filename})\n'
            ' * if you really do not want the asyncio/Qt/Twisted main loop to be installed, '
            'call declare_twisted_reactor_was_intentionally_chosen() before this import'
        )

    if 'asyncqt' not in sys.modules:
        asyncqt_main_loop = False
    else:
        from asyncqt import _QEventLoop
        asyncqt_main_loop = isinstance(asyncio.get_event_loop(), _QEventLoop)

    if not asyncqt_main_loop:
        raise RuntimeError(
            'Could not install the asyncio/Qt/Twisted main loop because a different asyncio main '
            'loop has already been set. You can fix this by:\n'
            '\n'
            '* calling declare_this_module_requires_qt_reactor() before any Twisted imports\n'
            f'   (probably early in {traceback.extract_stack()[0].filename})\n'
            '* if you really do not want the asyncio/Qt/Twisted main loop to be installed, '
            'call declare_twisted_reactor_was_intentionally_chosen() before this import'
        )


def declare_this_module_requires_asyncio_reactor():
    '''
    This should be called before any direct or indirect Twisted imports
    in any module that requires the asyncio/Twisted main loop to be
    installed, but does not require Qt.

    If declare_twisted_reactor_was_intentionally_chosen() has been
    previously called, this call will do nothing.
    Otherwise, this function will install the asyncio/Twisted main
    loop if possible, and raise RuntimeError otherwise (e.g., if a
    different Twisted reactor has already been installed.)
    '''
    if _twisted_reactor_intentionally_chosen:
        return

    reactor = sys.modules.get('twisted.internet.reactor')
    if not reactor:
        if sys.platform == 'win32':
            # On Windows with Python 3.8+, Twisted asyncioreactor
            # doesn't work properly with the default main loop, so
            # just use the Qt main loop.
            install_async_qt_reactor()
        else:
            asyncioreactor.install()
        return

    if not isinstance(reactor, asyncioreactor.AsyncioSelectorReactor):
        raise RuntimeError(
            'Could not install the asyncio/Twisted main loop because a Twisted reactor has '
            'already been installed. You can fix this by:\n'
            ' * calling declare_this_module_requires_asyncio_reactor() before any Twisted imports '
            f'(probably early in {traceback.extract_stack()[0].filename})\n'
            ' * if you really do not want the asyncio/Qt/Twisted main loop to be installed, '
            'call declare_twisted_reactor_was_intentionally_chosen() before this import'
        )


def install_certificate_authorities():
    if sys.platform == 'win32':
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
