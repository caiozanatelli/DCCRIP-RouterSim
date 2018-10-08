import socket

DEFAULT_PORT        = 55151
DEFAULT_PERIOD      = 30

class Router:
    __ip        = None
    __period    = DEFAULT_PERIOD
    __port      = DEFAULT_PORT
    __sock      = None

    def __init__(self, ip, period):
        self.__ip       = ip
        self.__period   = period
        self.__port     = DEFAULT_PORT
        self.__sock     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind((self.__ip, self.__port))

    def run(self):
        pass
    