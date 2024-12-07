import asyncio
import threading
import time
from typing import Coroutine, Any, Union
from queue import Queue


class Scheduler:
    def __init__(self):
        self.loop = None
        self.thread = None

        self.task_queue = Queue[Union[Coroutine[Any, Any, Any], None]]()

    def initialize(self, is_blocking: bool):
        if is_blocking:
            try:
                self.loop = asyncio.get_event_loop()
            except RuntimeError:
                self.loop = asyncio.new_event_loop()

        else:

            def run_in_thread():
                self.loop = asyncio.new_event_loop()

                while True:
                    try:
                        task = self.task_queue.get()
                        if task is None:  # Use None as a signal to stop the loop
                            break
                        self.loop.run_until_complete(task)
                    except Exception as e:
                        print(f"Error in thread: {e}")

            self.thread = threading.Thread(target=run_in_thread, daemon=True)
            self.thread.start()

    def run_until_complete(self, coroutine: Coroutine[Any, Any, Any]):
        # Run blocking tasks in thread
        if self.thread is not None:
            self.task_queue.put(coroutine)
        elif self.loop is not None:
            self.loop.run_until_complete(coroutine)

    def create_task(self, coroutine: Coroutine[Any, Any, Any]):
        if self.loop is not None:
            return self.loop.create_task(coroutine)

    def create_future(self) -> Union[asyncio.Future[Any], None]:
        if self.loop is not None:
            return asyncio.Future[Any](loop=self.loop)

    def ensure_future(self, coroutine: Coroutine[Any, Any, Any]):
        if self.loop is not None:
            return asyncio.ensure_future(coroutine, loop=self.loop)

    def stop(self):
        if self.thread is not None:
            self.task_queue.put(None)
            self.thread.join()

            self.loop = None
            self.thread = None

    def sleep(self, seconds: float):
        if self.loop is not None:
            return asyncio.sleep(seconds)

    def time(self):
        if self.loop is not None:
            return self.loop.time()
        else:
            return time.time()
