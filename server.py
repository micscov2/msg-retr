import socket
import threading
import sys
from socket import AF_INET, SOCK_STREAM
from data import ClientInfo, ChannelInfo

DEFAULT_MAX_CONNECTIONS = 3

class IRCServer(object):
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.max_connections = DEFAULT_MAX_CONNECTIONS
		self.server_data = {}
		self.clients = {}

	def start_server(self):
		s_fd = socket.socket(AF_INET, SOCK_STREAM)
		s_fd.bind((self.host, self.port))
		s_fd.listen(self.max_connections)
		print("IRC Server listening on port 1238")

		while True:
			conn, addr = s_fd.accept()
			threading.Thread(target = self.process_client, args = (conn, addr)).start()

	def process_client(self, conn, addr):
		print("Address of client: {}".format(addr))
		client_info = self.init_client(conn, addr)

		while True:
			data = conn.recv(4096)
			print("CLIENT: {}".format(data))

			if 'JOIN' in data:
				_, channel_name = data.split(" ")
				if not channel_name in self.server_data.keys():
					self.server_data[channel_name] = {}
				self.server_data[channel_name][client_info.nickname] = client_info
				conn.sendall("{} joined {} successfully!".format(client_info.nickname, channel_name))

			if not data:
				break
		conn.close()

	def init_client(self, conn, addr):
		data = conn.recv(4096)
		print("CLIENT: {}".format(data))
		_, nickname, _, name = data.split(" ")
		host, port = addr
		client_info = ClientInfo(name, nickname, host, port)
		self.clients[nickname] = client_info
		conn.sendall("Welcome to IRC Server\nDeveloped by Monkey D. Luffy\n{} successfully registered".format(name))

		return client_info


def main(args):
	irc_server = IRCServer("192.168.0.100", 1238)
	irc_server.start_server()


if __name__ == '__main__':
	main(sys.argv)
