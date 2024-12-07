import asyncio
import contextlib
import gc
from contextvars import ContextVar
import functools
import ipaddress
import logging
import os
from pathlib import Path
import re
import string
from time import monotonic as time_function

from trosnoth.const import DEFAULT_SERVER_PORT



def timeNow():
    '''
    This function exists so that even things which get a reference to timeNow()
    at import time can still be fooled by patching time_function.
    '''
    return time_function()


def new(count):
    '''new(count) - returns an iterator object which will give count distinct
    instances of the object class.  This is useful for defining setting
    options.  For example, north, south, east, west = new(4) . There is no
    reason that these options should be given numeric values, but it is
    important that north != south != east != west.
    '''
    for i in range(count):
        yield object()


def shade(colour, contrast, brightness):
    r, g, b = colour
    offset = (1 - contrast) * brightness * 255
    return (
        int(offset + r * contrast + 0.5),
        int(offset + g * contrast + 0.5),
        int(offset + b * contrast + 0.5),
    )


def filename_with_suffix(filename, suffix):
    if not filename:
        return filename
    base, ext = os.path.splitext(filename)
    return f'{base}{suffix}{ext}'


def initLogging(debug=False, logFile=None, prefix=''):
    import twisted.python.log
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter(
        '%(asctime)s {prefix}%(message)s'.format(prefix=prefix)))
    logging.getLogger().addHandler(h)
    if logFile:
        Path(logFile).parent.mkdir(parents=True, exist_ok=True)
        h = logging.FileHandler(logFile)
        h.setFormatter(logging.Formatter(
            '%(asctime)s {prefix}%(message)s'.format(prefix=prefix)))
        logging.getLogger().addHandler(h)
        logging.info('Initialised logging.')

    # Remove asyncio debug and info messages, but leave warnings.
    logging.getLogger('asyncio').setLevel(logging.WARNING)

    twisted.python.log.startLoggingWithObserver(
        twisted.python.log.PythonLoggingObserver(),
        setStdout=False,
    )


# Convenience functions for wrapping long strings based on maximum pixel width
# http://www.pygame.org/wiki/TextWrapping

def truncline(text, font, maxwidth):
    real = len(text)
    stext = text
    width = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    while width > maxwidth:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        width = font.size(stext)[0]
        real = len(stext)
        done = 0
    return real, done, stext


def wrapline(text, font, maxwidth):
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped


def format_numbers(numbers):
    if all(n % 1 < .005 for n in numbers):
        return [str(round(n)) for n in numbers]
    return [str(n) for n in numbers]


def format_number(n):
    return format_numbers([n])[0]


class BasicContextManager(object):
    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        pass


def stripPunctuation(nick):
    exclude = set(string.punctuation + ' ')
    return ''.join(ch for ch in nick if ch not in exclude)


FQDN_SEGMENT = re.compile(r'^[a-z0-9]([a-z-0-9]{0,61}[a-z0-9])?$', re.IGNORECASE)


def parse_server_string(server_string, default_port=DEFAULT_SERVER_PORT):
    # 1. It could be just an IP address
    try:
        ipaddress.ip_address(server_string)
        return (server_string, default_port)
    except ValueError:
        pass

    # 2. Otherwise, if it has a colon that separates host and port
    if ':' in server_string:
        host, port = server_string.rsplit(':', 1)
        try:
            port = int(port)
        except ValueError:
            raise ValueError('Invaild server string')
        if not (0 <= port <= 65535):
            raise ValueError('Invaild server string (port number out of allowed range)')
    else:
        host = server_string
        port = default_port

    # 3. The remaining hostname part could be an IP address
    try:
        ipaddress.ip_address(host)
        return (host, port)
    except ValueError:
        pass

    # 4. The hostname must be a valid FQDN
    if len(host) <= 1:
        raise ValueError('Invalid server string (host name too short)')
    if len(host) >= 253:
        raise ValueError('Invalid server string (host name too long)')

    if not all(FQDN_SEGMENT.match(bit) for bit in host.split('.')):
        raise ValueError('Invalid server string')
    if all(bit.isdigit() for bit in host.split('.')):
        raise ValueError('Invalid server string')
    return (host, port)


console_locals = ContextVar('console_locals', default={})


@contextlib.contextmanager
def new_console_context(initial_locals=()):
    new_dict = dict(console_locals.get())
    new_dict.update(initial_locals)
    token = console_locals.set(new_dict)
    try:
        yield
    finally:
        console_locals.reset(token)


def run_async_main_function(async_main):
    '''
    Runs the Twisted reactor until async_main returns or rasies an
    error.
    '''
    from twisted.internet import asyncioreactor, reactor

    if not isinstance(reactor, asyncioreactor.AsyncioSelectorReactor):
        raise RuntimeError('twisted asyncioreactor is not yet installed')

    async def inner():
        try:
            return await async_main()
        finally:
            if reactor.running:
                reactor.stop()

    task = asyncio.get_event_loop().create_task(inner())
    reactor.run()

    if not task.done():
        # Reactor must have been stopped manually
        raise SystemExit()
    return task.result()


def run_in_pygame(fn):
    '''
    Decorator which ensures that the pygame window is shown when the
    wrapped function is run. If the pygame window was not shown before
    the wrapped function launched, closes it again on return.
    '''
    from trosnoth.gui.app import get_pygame_runner

    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        pygame_runner = get_pygame_runner()
        if pygame_runner.is_showing():
            return await fn(*args, **kwargs)

        from trosnoth.settings import ClientSettings
        params = ClientSettings.get().display.get_video_parameters()
        return await pygame_runner.show_window(
            functools.partial(fn, *args, **kwargs),
            *params,
        )

    return wrapper


class UIScreenRunner:
    '''
    Provides an awaitable interface for a UI screen that's built using
    an event-driven system. The caller should await the run() method,
    and the UI screen should link completion events (e.g. 'Ok' and
    'Cancel' buttons) to the done() method.

    Does not allow reentrant calls.

    NOTE: In many cases it's simpler to just use a Future instead of
    a UIScreenRunner. The only thing a UIScreenRunner offers over a
    bare Future is the ability to start it again after it's finished.
    '''

    def __init__(self, start_function=None):
        self.future = None
        self.start_function = start_function

    @property
    def running(self):
        return self.future is not None and not self.future.done()

    def run(self):
        if self.running:
            raise RuntimeError('Already running')

        self.future = asyncio.get_running_loop().create_future()
        if self.start_function:
            self.start_function()

        return self.future

    def done(self, result):
        if not self.running:
            raise RuntimeError('Not running')
        future, self.future = self.future, None
        future.set_result(result)

    def error(self, exception):
        if not self.running:
            raise RuntimeError('Not running')
        future, self.future = self.future, None
        future.set_exception(exception)


def clean_garbage():
    '''
    Runs the garbage collector now, and in a few seconds. This gives
    time for the async main loop to clean up closed sockets etc.
    '''
    gc.collect()
    asyncio.get_event_loop().call_later(2.5, gc.collect)
