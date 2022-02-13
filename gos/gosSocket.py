import socket
import threading

class GOSMessage:

    def __init__(self, uid, message):
        self.uid = uid
        self.message = message


class GOSMessageQueue:

    def __init__(self):

        self.messageMap = {}
        self.lock = threading.Lock()

    def put(self, uid, message):

        if uid in self.messageMap:
            self.messageMap[uid].append(GOSMessage(uid, message))
        else:
            self.messageMap[uid] = [GOSMessage(uid, message)]

    def mass(self, message):

        for uid in self.messageMap:
            self.put(uid, message)

    def take(self, uid):

        if uid not in self.messageMap:
            return None
        mq = self.messageMap[uid]

        if len(mq) <= 0:
            return None

        data = mq[0]
        del mq[0]
        return data

    def registry(self, uid):
        self.messageMap[uid] = []


class GOSBaseHandler:

    def __init__(self, mq):
        self.messageQueue = mq

    def handle(self, uid, message):
        pass


class GOSConnectionRecv(threading.Thread):

    def __init__(self, connection, handler, uid):
        self.connection = connection
        self.handler = handler
        self.uid = uid
        super(GOSConnectionRecv, self).__init__()

    def run(self) -> None:
        while True:
            message = self.connection.recv(1024).decode("utf-8")
            print(self.uid + ":" + message)
            self.handler.handle(self.uid, message)


class GOSConnectionSend(threading.Thread):

    def __init__(self, mq, uid, connection):
        self.messageQueue = mq
        self.uid = uid
        self.connection = connection
        super(GOSConnectionSend, self).__init__()

    def run(self) -> None:
        while True:
            msg = self.messageQueue.take(self.uid)
            if msg is not None:
                print("send to " + msg.message)
                self.connection.sendall(msg.message.encode("utf-8"))


class GOSSocketServer(threading.Thread):

    def __init__(self, ip, port, backLog, handler):
        self.BUFFER_SIZE = 1024
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, port,))
        self.server.listen(backLog)

        self.messageQueue = GOSMessageQueue()
        self.handler = handler(self.messageQueue)

        self.connections = []
        super(GOSSocketServer, self).__init__()

    def run(self):

        while True:
            try:
                conn, address = self.server.accept()
                self.connections.append(conn)
                uid = GOSUtil.getUid(address[0], address[1])
                self.messageQueue.registry(uid)
                gr = GOSConnectionRecv(conn, self.handler, uid)
                gr.start()
                gs = GOSConnectionSend(self.messageQueue, uid, conn)
                gs.start()
            except Exception as e:
                break
        self.server.close()


class GOSUtil:

    @staticmethod
    def getUid(ip, port):
        return ip + "," + str(port)
