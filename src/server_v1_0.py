#!/router/bin/python3           
# This is server.py file

from socket import *                         # Import socket module
from threading import Thread                 # Import Thread module
import time
from concurrent.futures import ProcessPoolExecutor as Pool
import logging
from data import ChannelInfo, ClientInfo

logging.basicConfig(filename="server.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)

pool = Pool(4)
RECV_BUFFER_LIMIT = 2048
first_response = str("IRC Server Connected: ").encode('ascii')

#clients = []
groups = {}

def snapshot():
    while True:
        print("---Snapshot---")
        for grp_name, clients in groups.iteritems():
            print("Group: {}".format(grp_name))
            for client in clients:
                print("Connected at: {}".format(client.getpeername()))
        print("--------------")
        time.sleep(10)
    
def joinGroup(client, group_name, user_name=None):
    if group_name in groups:
        clientList = groups[group_name]
        if client not in clientList:
            clientList.append(client)
    else:
        ChannelInfo(name=group_name, members=[user_name]).save()
        groups[group_name] = [client]

    broadcastGroups(groups[group_name], str(user_name) + " joined the group")
    logger.debug("len(groups[group_name]): {}".format(groups[group_name]))

def register(client, request, user_name=None):
    logger.debug("Registering user: {}".format(request))
    ClientInfo(name=request, messages=[]).save()

    return request

def broadcastGroups(clients, msg, user_name=None):
    msg = str(msg).encode('ascii')
    logger.debug("broadcasting to ")
    for client in clients:
        logger.debug("client: {}".format(client))
        client.send(msg)

def multicastGroups(client, msg, user_name):
    msg = str(msg).encode('ascii') 
 
def panicHandler(client, request):
    msg = "Invalid Request: " + str(request)
    msg = msg.encode('ascii')
    client.send(msg)            

def private_msg(client, request, user_name=None):
    pass

def processInput(client, request, user_name=None):
    msgList  = request.split(" ",1)
    key = int(msgList[0])
    msg = str(msgList[-1])
    switcher = { 
        0: joinGroup,
        1: broadcastGroups,
        2: multicastGroups,
        3: private_msg,
        4: register
    }
    function = switcher.get(key, panicHandler)
    if key >= 5:
        return function(client, request, user_name)
    else:
        return function(client, msg, user_name)
      
def server(address):
    sock = socket(AF_INET, SOCK_STREAM)          # Create a socket object
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Set socket options
    sock.bind(address)                           # Bind to the port
    sock.listen(5)                               # Now wait for client connection.
    while True:
        client, addr = sock.accept()      # Establish connection with client.
        print("Connection to ",addr);
        #clients.append(client)
	    # Removing daemon=True for now, as it is not working on Ubuntu 14.04
        Thread(target=client_handler, args=(client,)).start()


def client_handler(client):
    client.send(first_response)
    user_name = None
    while True:
        request = client.recv(RECV_BUFFER_LIMIT)
        if not user_name:
            user_name = processInput(client, request.decode('utf-8'))
        else:
            processInput(client, request.decode('utf-8'), user_name)
        
    print("Done!")

Thread(target=snapshot, args=()).start()
server(('',12345))


