#!/usr/bin/env python3
import socketserver, threading,sys

class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print('[+] connected', self.request, file=sys.stderr)
        self.request.sendall(b'220 (vsFTPd 3.0.3)\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr,flush=True)
        self.request.sendall(b'230 Login successful.\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        self.request.sendall(b'200 yolo\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        self.request.sendall(b'200 yolo\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        self.request.sendall(b'257 "/" is the current directory\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        self.request.sendall(b'227 Entering Passive Mode (127,0,0,1,43,203)\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        self.request.sendall(b'227 Entering Passive Mode (127,0,0,1,43,203)\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        self.request.sendall(b'200 Switching to Binary mode.\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        self.request.sendall(b'125 Data connection already open. Transfer starting.\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        # 226 Transfer complete.
        self.request.sendall(b'250 Requested file action okay, completed.')
        exit()

def ftp_worker():
    with socketserver.TCPServer(('0.0.0.0', 2048), MyTCPHandler) as server:
        while True:
            server.handle_request()
threading.Thread(target=ftp_worker).start()