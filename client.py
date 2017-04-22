import socket
import sys
from socket import AF_INET, SOCK_STREAM

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

		while True:
			data = raw_input("Send something to server: ")
			s_fd.sendall(data)
			data = s_fd.recv(4096)
			if data in [None, ""]:
				break
			print("{}".format(data))

		s_fd.close()

	def register_client(self, s_fd):
		s_fd.sendall("NICK {} USER {}".format(self.nickname, self.name))	
		data = s_fd.recv(4096)
		print(data)


def main(name, nickname):
	print("{}:{}".format(name, nickname))
	irc_client = IRCClient("192.168.0.100", 1238, name, nickname)
	irc_client.start_client()

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
