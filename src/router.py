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

	def to_dict(self):
		d = dict()
		d["type"] = self.__type
		d["source"] = self.__src
		d["desination"] = self.__dest
		return d

class Data(Message):
	__payload	= None

	def __init__(self, src, dest, msg_type, payload):
		Message.__init__(self, src, dest, msg_type)
		self.__payload		= payload

	def to_dict(self):
		d = super().to_dict(self)
		d["payload"] = self.__payload
		return d

class Update(Message):
	__distances	= None

	def __init__(self, src, dest, msg_type, distances):
		Message.__init__(self, src, dest, msg_type)
		self.__distances	= distances

	def to_dict(self):
		d = super().to_dict(self)
		d["distances"] = self.__distances
		return d

class Trace(Message):
	__hops	= None

	def __init__(self, src, dest, msg_type, hops):
		Message.__init__(self, src, dest, msg_type)
		self.__hops	= hops

	d = super().to_dict(self)
		d["hops"] = self.__hops
		return d

class Packet:
	def json_encoding(json_dict):
		json_str = json.dumps(json_dict)
		return json_str

	def json_decoding(json_str):
		json_dict = json.loads(json_str)
		return json_dict

	def to_struct(json_str):
		data = bytes(json_str, 'ascii')
		return data

	def to_string(data):
		json_str = data.decode('ascii')
		return json_str


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