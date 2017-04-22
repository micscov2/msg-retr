import logging

class ChannelInfo(object):
	def __init__(self, topic, member):
		self.topic = topic
		self.members = [member]

	def add_member(self, member):
		self.members.append(member)

	def remove_member(self, member):
		self.members.remove(member)

	def get_members(self):
		return self.members


class ClientInfo(object):
	def __init__(self, name, nickname, host, port):
		self.name = name
		self.nickname = nickname
		self.host = host
		self.port = port

	def __str__(self):	
		return "{}:{}:{}:{}".format(self.name, self.nickname, self.host, self.port)	
