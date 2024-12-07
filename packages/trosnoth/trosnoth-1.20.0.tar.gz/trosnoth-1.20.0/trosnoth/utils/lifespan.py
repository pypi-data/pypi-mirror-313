import asyncio
import contextlib

from trosnoth.utils.event import Event


class LifeSpan:
    '''
    Used by anything which may end at some point (e.g., level, trigger,
    server). Allows registration of things which should also be torn down
    when this LifeSpan ends.
    '''

    def __init__(self):
        self.ended = False
        self.on_ended = Event([])

    def stop(self):
        if self.ended:
            return
        self.ended = True
        self.on_ended()

        # Prevent this lifespan being used after it's ended
        self.on_ended.clear()
        self.on_ended = None


class ContextManagerFuture:
    def __init__(self):
        self.future = asyncio.get_running_loop().create_future()

    def __await__(self):
        return self.future.__await__()

    @contextlib.contextmanager
    def subscribe(self, fn):
        self.future.add_done_callback(fn)
        try:
            yield
        finally:
            self.future.remove_done_callback(fn)

    def add_done_callback(self, *args, **kwargs):
        return self.future.add_done_callback(*args, **kwargs)

    def cancel(self, msg=None):
        return self.future.cancel(msg)

    def cancelled(self):
        return self.future.cancelled()

    def done(self):
        return self.future.done()

    def exception(self):
        return self.future.exception()

    def remove_done_callback(self, *args, **kwargs):
        return self.future.remove_done_callback(*args, **kwargs)

    def result(self):
        return self.future.result()

    def set_exception(self, exception, /):
        return self.future.set_exception(exception)

    def set_result(self, result, /):
        return self.future.set_result(result)
