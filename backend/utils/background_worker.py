# background_worker.py
# A tiny in-memory worker queue to run tasks without blocking API.

import asyncio
from threading import Thread
from queue import Queue

class BackgroundWorker:

    def __init__(self):
        self.queue = Queue()
        self.loop = asyncio.new_event_loop()

        # Start worker in a dedicated thread
        worker_thread = Thread(target=self._start, daemon=True)
        worker_thread.start()

    def _start(self):
        """Starts the dedicated async event loop and processes tasks forever."""
        asyncio.set_event_loop(self.loop)
        self.loop.create_task(self._process_tasks())
        self.loop.run_forever()

    async def _process_tasks(self):
        while True:
            func, args = await asyncio.to_thread(self.queue.get)
            await func(*args)
            self.queue.task_done()

    def add_task(self, func, *args):
        """
        Push a function into the background queue.
        """
        self.queue.put((func, args))

    def queue_size(self):
        return self.queue.qsize()
