# Trosnoth (UberTweak Platform Game)
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
Provides two sets of database utilities:
 - dbqueue.add() is used to defer the writing to the database to a
    queue which will be called asynchronously. This should be used with
    asynchronous django DB functions, or combined with
    asgiref.sync.sync_to_async
 - dbqueue.run_in_synchronous_thread runs the given function in a thread
    with no async main loop, to make Django happy. It blocks until the
    function completes
'''

import asyncio
import functools
import logging
import queue
import threading

from twisted.internet import defer, reactor

log = logging.getLogger(__name__)


DELAY = 0.01

async_queue = asyncio.Queue()
initialised = False
stopping = False


def ensure_initialised():
    global initialised
    if initialised:
        return

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        log.warn(
            'Called dbqueue.add() from synchronous thread. '
            'Running sychronously.')
        return

    initialised = True

    reactor.addSystemEventTrigger('before', 'shutdown', teardown)

    asyncio.create_task(_async_loop())


async def _async_loop():
    while async_queue or not stopping:
        fn = await async_queue.get()
        log.debug('dbqueue: running %r', fn)
        try:
            await fn()
        except Exception:
            log.exception('Error in queued database function')

        # Yield until the next main loop iteration
        loop = asyncio.get_running_loop()
        f = loop.create_future()
        loop.call_soon(f.set_result, None)
        await f


def add(fn):
    '''
    Adds the given function to the database queue.
    '''
    ensure_initialised()
    async_queue.put_nowait(fn)


def teardown():
    '''
    This is called during the Twisted reactor shutdown sequence, so we
    use Twisted deferreds instead of asyncio futures to make sure the
    shutdown doesn't complete until the db queue is empty.
    '''
    assert initialised

    global stopping
    stopping = True

    d = defer.Deferred()
    log.info('Stopping database queue...')

    @async_queue.put_nowait
    async def queue_is_empty():
        log.info('Database queue stopped')
        d.callback(None)

    return d


class SynchronousThread(threading.Thread):
    '''
    This exists for the purpose of convincing Django that there's
    absolutely no way that its ORM calls could be run concurrently
    from different async coroutines.
    '''
    def __init__(self):
        super().__init__(name='Django synchronous thread', daemon=True)
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()

    def run(self):
        while not stopping:
            target, args, kwargs = self.input_queue.get()
            try:
                result = True, target(*args, **kwargs)
            except Exception as e:
                result = False, e
            self.output_queue.put(result)


_synchronous_thread = None


def run_in_synchronous_thread(fn, *args, **kwargs):
    global _synchronous_thread

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        # We're already in a non-asyncio thread
        return fn(*args, **kwargs)

    if _synchronous_thread is None:
        _synchronous_thread = SynchronousThread()
        _synchronous_thread.start()

    _synchronous_thread.input_queue.put((fn, args, kwargs))
    success, result = _synchronous_thread.output_queue.get()
    if not success:
        raise result
    return result


def in_synchronous_thread(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return run_in_synchronous_thread(fn, *args, **kwargs)
    return wrapper
