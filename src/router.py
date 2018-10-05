#!/usr/bin/python3
import argparse
import json
import socket

#Try for using in the interpreter
import cmd

DEFAULT_PORT		= 55151
DEFAULT_PERIOD		= 30
class Message:
	__src		= None
	__dest		= None
	__type		= None

	def __init__(self, src, dest, msg_type):
		self.__src		= src
		self.__dest		= dest
		self.__type		= msg_type


class Packet:
	def json_encoding(json_dict):
		json_str = json.dumps(json_dict)
		return json_str

	def json_decoding(json_str):
		json_dict = json.loads(json_str)
		return json_dict

class Router:
	__ip		= None
	__period	= DEFAULT_PERIOD
	__port		= DEFAULT_PORT
	__sock		= None

	def __init__(self, ip, period):
		self.__ip		= ip
		self.__period	= period
		self.__port		= DEFAULT_PORT
		self.__sock		= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__sock.bind((self.__ip, self.__port))

	def run(self):
		pass



	def parse_args():
		parser = argparse.ArgumentParser()
		parser.add_argument("--addr", help="Router address")
		parser.add_argument("--update-period", help="Router update sending time", type=int)
		parser.add_argument("--startup-command", help="Command input file")
		args = parser.parse_args()
		return args

if __name__ == "__main__":
	args = Router.parse_args()
	router = Router(args.addr, args.update_period)
	router.run()