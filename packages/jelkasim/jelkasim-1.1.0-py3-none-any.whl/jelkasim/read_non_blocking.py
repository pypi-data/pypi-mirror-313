import threading
from time import sleep

class NonBlockingBytesReader:
    def __init__(self, f) -> None:
        self.f = f
        self.result = b""
        self.stop = False

    def start(self):
        self.stop = False
        self.worker = threading.Thread(target=self._f)
        self.worker.start()
        return self

    def _f(self):
        while not self.stop:
            try:
                r = self.f()
            except ValueError:
                break
            self.result += r
            sleep(0.005)
    
    def __call__(self):
        with threading.Lock():
            r = self.result
            self.result = b""
        return r
    
    def close(self):
        self.stop = True
        