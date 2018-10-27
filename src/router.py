import selectors
import socket
import sys
import re
from threading import Lock, Timer
from collections import defaultdict

DEFAULT_PORT   = 55151
DEFAULT_PERIOD = 30

class Router:

    def __init__(self, addr, period=None):
        self.__addr   = addr
        self.__period = period if period is not None else DEFAULT_PERIOD
        self.__port   = DEFAULT_PORT
        self.__sock   = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind((self.__addr, self.__port))
        self.__routes = defaultdict()
        self.__links  = dict()
        # Setting the selector for input (stdin and udp)
        self.__selector = selectors.DefaultSelector()
        self.__selector.register(sys.stdin, selectors.EVENT_READ, self.__handle_command)
        self.__selector.register(self.__sock, selectors.EVENT_READ, self.__handle_message)
        # Setting the locks to critical sessions
        self.__routes_lock = Lock()
        self.__links_lock  = Lock()

    def run(self):
        while True:
            evts = self.__selector.select()
            for key, mask in evts:
                callback_funct = key.data
                if key.fileobj == sys.stdin:
                    cmd = input()
                    callback_funct(cmd)

                    print(self.__links)
                    print(self.__routes)
                elif key.fileobj == self.__sock:
                    print('Message handler not implemented yet. Sorry.')

    def add_link(self, addr, weight):
        # Check whether we have a valid addr
        if not self.__check_addr(addr):
            self.__logexit('Error. Invalid IP.')

        if addr == self.__addr:
            print('Error on adding link: router trying to make a link to itself.')
            sys.exit(1)
        self.__links_lock.acquire()
        self.__links[addr] = weight
        self.__links_lock.release()

    def remove_link(self, addr):
        # Check whether we have a valid addr
        if not self.__check_addr(addr):
            self.__logexit('Error. Invalid IP.')

        # First we safely remove the addr from the routing table
        self.__routes_lock.acquire()
        for key, mask in self.__routes.items():
            try:
                del self.__routes[key][addr]
                pass
            except:
                pass
        self.__routes_lock.release()

        # Then we safely remove the addr from the link table
        self.__links_lock.acquire()
        del self.__links[addr]
        self.__links_lock.release()

    def __handle_command(self, cmd_input):
        # TODO: perform all the commands in this function
        cmd = cmd_input.split(' ')
        length =  len(cmd)

        if length == 3 and cmd[0] == 'add':
            try:
                self.add_link(cmd[1], int(cmd[2]))
            except Exception as e:
                print(e)
                sys.exit(1)
        elif length == 2 and cmd[0] == 'del':
            self.remove_link(cmd[1])
        else:
            print('Invalid command. Try again.')

    def __handle_message(self):
        # TODO: handle all the message types we receive by UDP
        pass

    def __check_addr(self, ip):
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

    def __logexit(self, msg):
        print(msg)
        sys.exit(1)
