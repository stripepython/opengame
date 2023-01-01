from typing import Any
import socket
    
    
class User(object):
    name: str = ''
    password: str = ''
    
    def __init__(self, sock: socket.socket, address: Any):
        self.sock = sock
        self.addr = address
        self.attitudes = {}
        
    def __getitem__(self, item):
        return self.attitudes[item]
    
    def __setitem__(self, key, value):
        self.attitudes[key] = value
        
    def send(self, string: str):
        self.sock.send(string.encode('utf-8'))
        
    def close(self):
        self.sock.close()
        
    def get(self, byte: int = 65536):
        return self.sock.recv(byte).decode('utf-8')
        

class Client(object):
    def __init__(self, host: str = '127.0.0.1', port: int = 6666):
        self.sock = socket.socket()
        self.sock.connect((host, port))
        
    def send(self, string: str):
        self.sock.send(string.encode('utf-8'))
        
    def get(self, byte: int = 65536):
        return self.sock.recv(byte).decode('utf-8')
    
    def close(self):
        self.sock.close()
