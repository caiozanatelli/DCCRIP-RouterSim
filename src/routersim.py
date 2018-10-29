#!/usr/bin/python3
import argparse
import sys
from router import Router

def parse_args():
	parser = argparse.ArgumentParser(description='A router simulator that implements a \
			distance-vector routing protocol with network balance and routing measures')
	parser.add_argument("--addr", help="Router address", type=str, required=True)
	parser.add_argument("--update-period", help="Router update sending time", type=int)
	parser.add_argument("--startup-command", help="Command input file")
	args = parser.parse_args()
	return args

if __name__ == "__main__":
	args = parse_args()
	router = Router(args.addr, args.update_period, args.startup_command)
	router.run()
