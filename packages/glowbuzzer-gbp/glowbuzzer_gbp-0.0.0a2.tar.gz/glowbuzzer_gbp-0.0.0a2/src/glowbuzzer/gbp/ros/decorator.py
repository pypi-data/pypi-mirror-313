import asyncio
from abc import ABC
from asyncio import AbstractEventLoop

'''
Decorator used to wrap a method of a class that inherits from AsyncIoSupport.
These methods are then run in the context of the asyncio event loop, rather than the ROS2 event loop.
Note that these methods will block the ROS2 event loop, so the MultiThreadedExecutor must be used.
In order that the method does not block indefinitely, a timeout is set. It's also important to use
`executor.spin_once(0)` to ensure that the asyncio event loop is not blocked.
'''


class AsyncIoSupport(ABC):
    loop: AbstractEventLoop = None

    def __init__(self, loop: AbstractEventLoop):
        self.loop = loop


def with_asyncio(timeout=20):
    def decorator(func):
        def wrapper(*args, **kwargs):
            node: AsyncIoSupport = args[0]

            if not node.loop:
                raise Exception(
                    "Event loop not set. Make sure with_asyncio is used in a class that inherits from AsyncIoSupport"
                )

            return asyncio.run_coroutine_threadsafe(func(*args, **kwargs), node.loop).result(timeout)

        return wrapper

    return decorator
