import socket
import sys
import re

DEFAULT_PORT   = 55151
DEFAULT_PERIOD = 30

class Router:
    __ip     = None
    __period = DEFAULT_PERIOD
    __port   = DEFAULT_PORT
    __sock   = None

    def __init__(self, ip, period):
        self.__ip     = ip
        self.__period = period
        self.__port   = DEFAULT_PORT
        self.__sock   = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind((self.__ip, self.__port))

    def run(self):
        while True:
            cmd = raw_input()
            ip, weight = self.__parse_command(cmd)
            if ip is None and weight is None:
                pass

    def __parse_command(self, cmd_input):
        cmd = cmd_input.split(' ')
        length =  len(cmd)
        ip     = None
        weight = None

        if length == 3 and cmd[0] == 'add':
            try:
                ip = cmd[1]
                weight = int(cmd[2])
                if not self.__check_ip(ip):
                    print('Invalid IP. Try again.')
            except Exception as e:
                print(e)
                sys.exit(1)
        elif length == 2 and cmd[0] == 'del':
            ip = cmd[1]
            if not self.__check_ip(ip):
                print('Invalid IP. Try again.')
        else:
            print('Invalid command. Try again.')
        return ip, weight

    def __check_ip(self, ip):
        b = ip.split('.')
        if len(b) != 4:
            return False
        for elem in b:
            try:
                if int(elem) < 0 or int(elem) > 255:
                    return False
            except Exception as e:
                return False
        return True