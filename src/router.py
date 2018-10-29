import selectors
import socket
import sys
import re
import random
from threading import Lock, Timer
from collections import defaultdict
from message import *

DEFAULT_PORT   = 55151
DEFAULT_PERIOD = 15
MAX_UDP_SIZE = 65507
MAX_WEIGHT = sys.maxsize

class Router:

    def __init__(self, addr, period, startcmd=None):
        self.__addr   = addr
        self.__period = period
        self.__port   = DEFAULT_PORT
        self.__sock   = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind((self.__addr, self.__port))
        self.__routes = defaultdict()
        self.__links  = dict()
        self.__routes_timer = dict()
        # Setting the selector for input (stdin and udp)
        self.__selector = selectors.DefaultSelector()
        self.__selector.register(sys.stdin, selectors.EVENT_READ, self.__handle_command)
        self.__selector.register(self.__sock, selectors.EVENT_READ, self.__handle_message)
        # Setting the locks to critical sessions
        self.__routes_lock = Lock()
        self.__links_lock  = Lock()
        self.__routes_timer_lock  = Lock()
        # Setting the timer for updating routes information
        self.__timer = Timer(self.__period, self.__send_update)
        self.__timer.start()
        # Initialization with previous installed commands
        if not startcmd is None:
            self.__startup_command(startcmd)

    def __startup_command(self, input_file):
        with open(input_file) as fp:
            for line in fp:
                self.__handle_command(line)

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
                    self.__handle_message()

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
        print('Link added...')
        print(self.__links)
        print(self.__routes)

    def remove_link(self, addr):
        # Check whether we have a valid addr
        if not self.__check_addr(addr):
            self.__logexit('Error. Invalid IP.')

        # First we safely remove the addr from the routing table
        self.__remove_routes(addr)

        # Then we safely remove the addr from the link table
        self.__links_lock.acquire()
        del self.__links[addr]
        self.__links_lock.release()
        print('Link removed...')
        print(self.__links)
        print(self.__routes)

    def send_message(self, message):
        self.__routes_lock.acquire()
        self.__links_lock.acquire()

        routes = self.__get_routes(message.get_destination())

        self.__routes_lock.release()
        self.__links_lock.release()

        if(len(routes == 0)):
            # Send error message to origin
            error_message = Data(self.__addr, message.get_source(), "data", "Error: Unknown route to "+ str(message.get_destination()))
            data = Packet.to_struct(Packet.jsonEncoding(error_message.to_dict()))
            send_message(data)

        else:
            data = Packet.to_struct(Packet.jsonEncoding(message.to_dict()))
            self.__sock.sendto(data, (random.choice(routes)))

    def __send_update(self):
        print('Sending update...')

        self.__routes_lock.acquire()
        self.__links_lock.acquire()
        print('Locking variables...')

        routes = self.__routes.keys() | self.__links.keys()
        print(routes)

        for link in self.__links:
            print('Iterating over links...')
            distances = {}
            for dest in routes:
                print('Iterating over distances...')
                if (dest != link):
                    # Removes all entries received from link
                    routes = list(filter(lambda x: x[0] != link, self.__routes[dest]))

                    if (len(routes) == 0):
                        continue

                    min_weight, _ = self.__get_min_route(routes)
                    distances[dest] = min_weight
                    print('Updating min distance...')

            print('Building update message...')
            message = Update(self.__addr, link, "update", distances)
            print('Sending update message...')
            self.send_message(message)
            print('Done...')

        self.__routes_lock.release()
        self.__links_lock.release()

        # Resetting the timer
        #self.__timer.cancel()
        #self.__timer = Timer(self.__period, self.__send_update)
        #self.__timer.start()

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
        print('Handling message...')
        print(self.__links)
        print(self.__routes)

        message, _ = self.__sock.recvfrom(MAX_UDP_SIZE)
        message_dict = Packet.jsonDecoding(Packet.to_string(message))

        if (message_dict["type"] == "data"):
            data_message = Data(message_dict["source"], message_dict["destination"], message_dict["type"], message_dict["payload"])
            self.__handle_data_message(data_message)

        elif (message_dict["type"] == "update"):
            update_message = Update(message_dict["source"], message_dict["destination"], message_dict["type"], message_dict["distances"])
            self.__handle_update_message(update_message)

        elif (message_dict["type"] == "trace"):
            trace_message = Trace(message_dict["source"], message_dict["destination"], message_dict["type"], message_dict["hops"])
            self.__handle_trace_message(trace_message)

    def __handle_data_message(self, message):
        print(message.__payload)
        self.send_message(message)

    def __handle_update_message(self, message):
        if (message.__dest == self.__addr):
            self.__routes_lock.acquire()
            self.__links_lock.acquire()
            self.__routes_timer_lock.acquire()

            for dest in message.__distances.keys():
                # Removes all old entries from src
                routes = list(filter(lambda x : x[0] != message.get_source(), self.routes[dest]))
                # Adds new entries received
                routes.append((message.get_source(), message.get_distances[dest]))

                self.__routes[dest] = routes

            if (message.get_source() in self.__routes_timer):
                self.__routes_timer[message.get_source()].cancel()
            self.__routes_timer[message.get_source()] = Timer(4*self.__period, self.__remove_routes, [message.get_source()])
            self.__routes_timer[message.get_source()].start()

            self.__routes_lock.release()
            self.__links_lock.release()
            self.__routes_timer_lock.release()

        else:
            self.send_message(message)

    def __handle_trace_message(self, message):
        message.get_hops().append(self.__addr)

        if (message.get_destination() == self.__addr):
            trace = Packet.jsonEncoding(message.to_dict())
            message = Data(self.__addr, message["source"], "data", trace)
            self.send_message(message)

        else:
            self.send_message(message)

    def __get_routes(self, dest):
        m = MAX_WEIGHT
        routes = list()

        if (dest in self.__routes):
            m, routes = self.__get_min_route(self.__routes[dest])

        if (dest in self.__links):
            if (self.__links[dest] < m):
                m = self.__links[dest]
                routes = [dest]

            elif (self.__links[dest] == m):
               routes.append(dest)

        return routes

    def __get_min_route(self, routes):
        min_weight = min(a[1], key = lambda x: x[1])[1]
        min_routes = list(filter(lambda x: x[1] == m, routes))
        return min_weight, min_routes

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

    def __reset_timer(self):
        timer = Timer(self.__period, self.__send_update)
        self.__timer.cancel()
        self.__timer = timer
        self.__timer.start()

    def __remove_routes(self, addr):
        self.__routes_lock.acquire()

        for dest in self.__routes.keys():
            # Removes all old entries from addr
            routes = list(filter(lambda x : x[0] != addr, self.routes[dest]))
            self.__routes[dest] = routes

        self.__routes_lock.release()

    def __logexit(self, msg):
        print(msg)
        sys.exit(1)
