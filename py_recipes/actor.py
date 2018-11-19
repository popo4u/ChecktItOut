# coding: utf-8

from queue import Queue
from threading import Thread, Event


class ActorExit(Exception):
    pass


class Actor:

    def __init__(self):
        self._mailbox = Queue()

    def start(self):
        self._terminated = Event()
        t = Thread(target=self._bootstrap)
        t.daemon = True
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def send(self, msg):
        self._mailbox.put(msg)

    def recv(self):
        msg = self._mailbox.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        self.send(ActorExit)

    def join(self):
        self._terminated.wait()

    def run(self):
        while True:
            msg = self.recv()


# Sample ActorTask
class PrintActor(Actor):
    def run(self):
        while True:
            msg = self.recv()
            print('Got:', msg)


def demo():
    # Sample use
    p = PrintActor()
    p.start()
    p.send('Hello')
    p.send('World')
    p.close()
    p.join()


if __name__ == "__main__":
    demo()