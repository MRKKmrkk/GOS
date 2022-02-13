import socket
import tkinter
import threading
import os
from tkinter import scrolledtext

class GOSClientListener(threading.Thread):

    def __init__(self, client):
        self.client = client
        self.flag = True
        super(GOSClientListener, self).__init__()

    def run(self) -> None:

        while self.flag:
            msg = self.client.connection.recv(1024).decode("utf-8")
            print(msg)
            if msg == '{"cmd": "kill"}':
                self.client.killGTAV()

class GOSClientSend(threading.Thread):

    def __init__(self, connection):
        self.connection = connection
        super(GOSClientSend, self).__init__()

    def run(self) -> None:
        self.connection.sendall('{"cmd": "kill"}'.encode("utf-8"))

class GOSClient:

    def killGTAV(self):
        code = os.system("..\\GTAProcessTerminate\\cmake-build-debug\\GTAProcessTerminate.exe")
        if code == 1:
            self.textMessage("kill GTAV success!")
        else:
            self.textMessage("kill GTAV fail!")

    def textMessage(self, msg):
        self.text.insert("end", msg + "\n")

    def connect(self):
        host = self.s1.get()
        port = self.s2.get()
        if len(host) == 0 or len(port) == 0:
            self.textMessage("host or port can not be empty!")
        else:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((host, int(port)))
            self.connection = conn
            self.textMessage("connect success!")

            self.listener = GOSClientListener(self)
            self.listener.start()

    def close(self):
        if self.connection is None:
            self.textMessage("you have not connect yet!")
        else:
            self.listener.flag = False
            self.listener = None
            self.connection.close()
            self.connection = None
            self.textMessage("close success!")

    def killAllGTAV(self):
        if self.connection is None:
            self.textMessage("you have not connect yet!")
        else:
            self.killGTAV()
            g = GOSClientSend(self.connection)
            g.start()

    def __init__(self):
        window = tkinter.Tk()
        window.title('GTA5 GOS')

        l1 = tkinter.Label(text="server host")
        l1.grid(row=0, column=0)

        s1 = tkinter.StringVar()
        entry1 = tkinter.Entry(window, textvariable=s1)
        entry1.grid(row=0, column=1)

        l2 = tkinter.Label(text="server port")
        l2.grid(row=1, column=0)

        s2 = tkinter.StringVar()
        entry2 = tkinter.Entry(window, textvariable=s2)
        entry2.grid(row=1, column=1)

        i = 0
        mpb = tkinter.Button(window, text='only kill my GTAV', command=self.killGTAV)
        mpb.grid(row=2, column=0, columnspan=4)

        button1 = tkinter.Button(window, text=' connect', command=self.connect)
        button1.grid(row=0, column=2)
        button2 = tkinter.Button(window, text='     close', command=self.close)
        button2.grid(row=1, column=2)
        button3 = tkinter.Button(window, text='kill GTAV', command=self.killAllGTAV)
        button3.grid(row=2, column=2)

        scrolW = 50
        scrolH = 18
        text = scrolledtext.ScrolledText(window, width=scrolW, height=scrolH, wrap=tkinter.WORD)
        text.grid(row=10, columnspan=8, sticky=tkinter.E)

        self.text = text
        self.s1 = s1
        self.s2 = s2
        self.connection = None
        self.listener = None

    def main(self):
        tkinter.mainloop()


if __name__ == '__main__':

    gc = GOSClient()
    gc.main()
