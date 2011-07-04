from __future__ import print_function

import sys
import socket
from contextlib import contextmanager

ADDR = HOST, PORT = "localhost", 9698


class ThinkpadlightClient(object):

	def __init__(self, addr=ADDR):
		self.addr = self.host, self.port = addr
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def set_light(self, status):
		self.sock.send((b"1" if status else b"0") + b"\n")
		received = self.sock.recv(1)
		return received

	@contextmanager
	def connect(self):
		self.sock.connect(self.addr)
		yield self
		# Send empty line to indicate end
		self.sock.send(b"\n")
		self.sock.close()


""" USAGE """
if __name__ == "__main__":
	import time
	print("This makes the light flash twice. Don't forget to start the server as root first.")

	try:
		with ThinkpadlightClient() as tc:

			for x in range(2):
				tc.set_light(1)
				time.sleep(1)
				tc.set_light(False)
				time.sleep(1)
	except socket.error as e:
		if e.errno == 111:  # 111 is "Connection refused"
			print("Connection refused. Please make sure thinkpadlightd is running", file=sys.stderr)
			exit(1)
