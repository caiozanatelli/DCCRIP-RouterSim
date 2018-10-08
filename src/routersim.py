#!/usr/bin/python3
import argparse
import router

#Try for using in the interpreter
import cmd

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
