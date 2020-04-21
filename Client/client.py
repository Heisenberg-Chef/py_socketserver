import socket

HOST,PORT = '127.0.0.1',9999
data = 'hello'

class CliHandler():
    def call(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((HOST,PORT))
        sock.send(input(">>:").encode())
        
    def start(self):
        while True:
            self.call()
            
if __name__ == '__main__':
    coco = CliHandler()
    coco.start()