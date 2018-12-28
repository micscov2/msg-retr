import logging
import mongoengine as me
from mongoengine import Document

me.connect("mirc_db")

class ChannelInfo(Document):
    name = me.StringField(required=True, unique=True)
    members = me.ListField(me.StringField())

class ClientInfo(Document):
    name = me.StringField(required=True, unique=True)
    #nickname = me.StringField(required=True)
    messages = me.ListField(me.StringField())

class ServerData(object):
    def __init__(self):
        self.init = True
        self.clients = []
        self.groups = {}

    def server_startup(self):
        pass
