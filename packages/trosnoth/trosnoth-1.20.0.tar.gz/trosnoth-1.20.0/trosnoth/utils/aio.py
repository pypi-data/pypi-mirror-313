import asyncio
import functools
import inspect
import logging
import threading
from typing import List, Awaitable

from twisted.internet import defer, reactor
from twisted.python.failure import Failure

log = logging.getLogger(__name__)


def _catch(failure):
    # Without this, all traceback information from within the Twisted code
    # vanishes.
    if len(failure.value.args) > 1:
        return failure

    description = '{}\n--- deferred stack ---\n{}'.format(
        failure.value, failure.getTraceback())

    try:
        exc = type(failure.value)(description)
    except Exception:
        return failure
    return Failure(exc)


def check_reactor():
    if 'asyncio' not in type(reactor).__name__.lower():
        import sys
        sys.exit(
            'Asyncio reactor not installed in Twisted! (Saw {} instead.) '
            'Exiting.'.format(type(reactor).__name__))


def as_future(d):
    # noinspection PyUnreachableCode
    if __debug__:
        check_reactor()

    return d.addErrback(_catch).asFuture(asyncio.get_event_loop())


def as_deferred(f):
    # noinspection PyUnreachableCode
    if __debug__:
        check_reactor()

    return defer.Deferred.fromFuture(asyncio.ensure_future(f))


def return_deferred(async_fn):
    @functools.wraps(async_fn)
    def wrapper(*args, **kwargs):
        result = async_fn(*args, **kwargs)
        return as_deferred(result)
    return wrapper


async def cancel_task(task):
    '''
    Coroutine which cancels the given task and does not return until the
    task finishes all cleanup from being cancelled.

    :param task: a task that has not already been awaited
    '''

    loop = asyncio.get_running_loop()

    done = loop.create_future()

    async def wrapper():
        try:
            await task
        finally:
            if not done.done():
                done.set_result(None)

    wrapper_task = asyncio.create_task(wrapper())
    loop.call_soon(wrapper_task.cancel)

    await done


async def call_wait_and_catch(aw, caller):
    try:
        return await aw
    except Exception:
        log.exception(
            f'Error in concurrent task (from {caller.f_code.co_filename}:{caller.f_lineno})')
        return None


async def all_completed(awaitables: List[Awaitable]) -> List:
    '''
    Like asyncio.gather(), except for a few major differences:
        1. the awaitables are passed in a sequence rather than as
            variable-count arguments
        2. any exceptions in the awaitables are caught and logged, and
            a return value of None is used in the returned sequence.

    :param awaitables: a sequence of coroutines or tasks to wait for.
    '''
    caller = inspect.currentframe().f_back
    return await asyncio.gather(*[call_wait_and_catch(aw, caller) for aw in awaitables])


def create_safe_task(aw: Awaitable):
    '''
    Like asyncio.create_task(), except that any exceptions raised by the
    coroutine will be caught and logged, and the task will have a return
    value of None.

    :param aw: an awaitable
    :return: a Task
    '''
    caller = inspect.currentframe().f_back
    return asyncio.create_task(call_wait_and_catch(aw, caller))


class SimpleAsyncIterator:
    '''
    Callback-based code can return this so that the caller can use it in
    an async for statement.

    To push a value to the caller, use .next(value). To close the
    iterator, call .done().
    '''

    def __init__(self, cancel_callback=None):
        self.cancel_callback = cancel_callback
        self.future = asyncio.get_running_loop().create_future()

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            result = await self.future
        except asyncio.CancelledError:
            if self.cancel_callback:
                self.cancel_callback()
            raise
        self.future = asyncio.get_running_loop().create_future()
        return result

    def next(self, something):
        self.future.set_result(something)

    def done(self):
        if not self.future.done():
            self.future.set_exception(StopAsyncIteration())


def single_entry_task(fn):
    '''
    Decorator which indicates that the decorated asynchronous method can
    only be running once at a given time. If the method is called when
    it's already running, the first call will be cancelled.
    '''
    running = {}

    async def launch_method(wait_first, self, args, kwargs):
        await wait_first
        return await fn(self, *args, **kwargs)

    @functools.wraps(fn)
    async def wrapper(self, *args, **kwargs):
        # Create a new task and insert it into the dict so that, if
        # cancel() is called while we're waiting for the old task to
        # cancel, it doesn't try to cancel the old one first.
        f = asyncio.get_running_loop().create_future()
        new_task = asyncio.create_task(launch_method(f, self, args, kwargs))
        old_task = running.get(self)
        running[self] = new_task

        try:
            # Cancel the old task, then signal that the new one can properly
            # start.
            try:
                if old_task:
                    await cancel_task(old_task)
            except asyncio.CancelledError:
                new_task.cancel()
                raise
            f.set_result(None)
            return await new_task
        finally:
            if running.get(self) is new_task:
                del running[self]

    return wrapper


def delay_so_messages_will_apply_immediately(fn):
    '''
    Decorator that makes the decorated function or method wait for the
    next iteration of the main loop before running. This can be useful
    server-side because it ensures that messages sent from inside the
    wrapped function or method will be applied immediately (rather than
    potentially being deferred in sendServerCommand() because processing
    for another message is not yet complete).
    '''

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        asyncio.get_running_loop().call_soon(
            functools.partial(fn, *args, **kwargs))

    return wrapper
