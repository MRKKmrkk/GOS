from gosSocket import *
import sys

class Handler:

    def __init__(self, mq):
        self.messageQueue = mq

    def handle(self, uid, message):
        if message == '{"cmd": "kill"}':
            self.messageQueue.mass('{"cmd": "kill"}')


if __name__ == '__main__':

    s = GOSSocketServer(
        sys.argv[1],
        int(sys.argv[2]),
        5,
        Handler
    )
    s.start()
    s.join()
