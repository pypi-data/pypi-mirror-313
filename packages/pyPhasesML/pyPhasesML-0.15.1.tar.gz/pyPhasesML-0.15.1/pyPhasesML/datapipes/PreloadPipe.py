from queue import Queue, Full
from threading import Condition, Lock, Thread, current_thread

from pyPhasesML.datapipes.DataPipe import DataPipe
from pyPhases import classLogger


@classLogger
class PreloadPipe(DataPipe):
    def __init__(self, datapipe: DataPipe, preloadCount=1):
        super().__init__(datapipe)
        self.queue = Queue(maxsize=preloadCount)
        self.done = False

    def start(self):
        thread = Thread(target=self._preload)
        thread.daemon = True  # don't wait for thread to finish
        thread.start()

    def _preload(self):
        for d in self.datapipe:
            self.queue.put(d, block=True)
        self.done = True
        return

    def __iter__(self):
        self.start()
        self.done = False
        return self

    def __next__(self):
        if self.done and self.queue.empty() or len(self) == 0:
            raise StopIteration

        return self.queue.get(block=True)
