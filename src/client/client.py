import socket
import requests
import sys
from socket import AF_INET, SOCK_STREAM
import threading
import time
import logging

logging.basicConfig(filename="client.log", level=logging.DEBUG)
logger = logging.getLogger(" [CLIENT] - ")

class IRCClient(object):
	def __init__(self, host, port, name):
		self.host = host
		self.port = port
		self.name = name

	def return_res(self, data):
		data = data.split(" ")[1].split(",")
		output_f = 0
		for item in data:
			output_f += int(item)
		
		return str(output_f)

	def start_client(self):
		s_fd = socket.socket(AF_INET, SOCK_STREAM)
		s_fd.connect((self.host, self.port))
		self.register_client(s_fd)

		threading.Thread(target=self.listen_for_server_input, args=(s_fd, )).start()
		# To allow proper printing of description on console
		time.sleep(2)
		first_time = True
		while True:
			data = raw_input("")
			s_fd.sendall(data)

		s_fd.close()

	def listen_for_server_input(self, s_fd):
		logger.info("Listening for server input on separate thread\n")
		while True:
			data = s_fd.recv(4096)
			print("[SERVER] - {}".format(data))
			if "COMPUTE" in data.split(" ")[0]:
			    print("Server wants client to compute something {}".format(data))
			    s_fd.sendall("COMPUTE " + self.return_res(data))
			    print("Sent COMPUTE to server")
                s_fd.sendall("COMPUTE {}".format(16))
                print("Sent COMPUTE {}".format(16))

	def register_client(self, s_fd):
		logger.debug("Registering client")
		s_fd.sendall("REGISTER {}\n".format(self.name))	
		data = s_fd.recv(4096)
		print(data)


def main(host, port, name):
	irc_client = IRCClient(host, int(port), name)
	irc_client.start_client()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python client.py <name>")
        sys.exit(1)
    else:
        host, port, name = requests.get("http://localhost:6666/server").text.split(":")
        try:
            main(host, port, sys.argv[1])
        except socket.error:
            print("Exception caught while connecting to server, please check if {}:{} is running".format(host, port))
