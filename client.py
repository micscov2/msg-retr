import socket
import sys
from socket import AF_INET, SOCK_STREAM
import threading
import time

class IRCClient(object):
	def __init__(self, host, port, name, nickname):
		self.host = host
		self.port = port
		self.name = name
		self.nickname = nickname

	def start_client(self):
		s_fd = socket.socket(AF_INET, SOCK_STREAM)
		s_fd.connect((self.host, self.port))
		self.register_client(s_fd)

		threading.Thread(target=self.listen_for_server_input, args=(s_fd, )).start()
		# To allow proper printing of description on console
		time.sleep(2)
		first_time = True
		while True:
			data = raw_input("Send something to server: ")
			s_fd.sendall(data)
			#if first_time:
			#	print("Recv data from server")
			#	data = s_fd.recv(4096)
			#	print("{}\n".format(data))
			#	print("Response recv: from server")
			#first_time = False

		s_fd.close()

	def listen_for_server_input(self, s_fd):
		print("Listening for server input on separate thread\n")
		while True:
			data = s_fd.recv(4096)
			print("Recieved from server: {}\n".format(data))

	def register_client(self, s_fd):
		s_fd.sendall("NICK {} USER {}\n".format(self.nickname, self.name))	
		data = s_fd.recv(4096)
		print(data)


def main(name, nickname, host, port):
	irc_client = IRCClient(host, int(port), name, nickname)
	irc_client.start_client()

if __name__ == '__main__':
	if len(sys.argv) < 5:
		print("Usage: python client.py <name> <nickname> <host> <port>\n")
		sys.exit()

	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
