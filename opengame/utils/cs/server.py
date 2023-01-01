import socket
from threading import Thread
from typing import Callable, Any

from .client import User


class Server(object):
    def __init__(self, host: str = '127.0.0.1', port: int = 6666, debug: bool = False, **kwargs):
        self.sock = socket.socket()
        self.sock.bind((host, port))
        if debug:
            print(f'Bind {host}: {port}', **kwargs)
        self.users = []

        _empty_func = lambda user: None
        self._when_user = _empty_func
        self._when_user_quit = _empty_func
        self._debug = debug
        
    def run(self, requests: int = 10, **kwargs):
        self.sock.listen(requests)
        while True:
            sock, addr = self.sock.accept()
            if self._debug:
                print(f'Get connected: ({sock}, {addr})', **kwargs)
            user = User(sock, addr)
            self.users.append(user)
            t = Thread(target=self._when_user_really, args=(user, ))
            t.start()
            if self._debug:
                print('Started thread', **kwargs)
    
    def _when_user_really(self, user: User):
        try:
            self._when_user(user)
        except ConnectionError:
            self.users.remove(user)
            self._when_user_quit(user)
            
    def broadcast(self, data: str, **kwargs):
        for user in self.users:
            user.send(data)
        if self._debug:
            print(f'Broadcast {data}', **kwargs)
            
    def when_user_connected(self, func: Callable[[User], Any]):
        self._when_user = func
        
    when_user = when_user_connected
    
    def when_user_quited(self, func: Callable[[User], Any]):
        self._when_user_quit = func
