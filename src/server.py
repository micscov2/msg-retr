from socket import *   
from threading import Thread 
import time
import sys
import logging
from redis import StrictRedis
from data import ChannelInfo, ClientInfo
from utils import get_code_from_str


RECV_BUFFER_LIMIT = 2048

if len(sys.argv) <= 2:
    print "Usage ./start.sh <port> <server_name>"
    sys.exit(1)

server_name = sys.argv[2] + ":"
first_response = "Welcome to IRC Server: "
client_name_to_sock_mapping = {}
groups = {}
switcher = {}
comp_res_expected = 0
input_arr = ['1', '2', '3', '7', '3', '7', '8', '10', '1', '3']
comp_len = 5
client_name_to_res_mapping = {}
client_name_to_num_mapping = {}
# To be used to generate client_name_to_num_mapping
client_num = 1

logging.basicConfig(filename="server_" + server_name[:-1] + ".log", level=logging.INFO)
logger = logging.getLogger(" [SERVER] - ")

s_redis = StrictRedis(host="localhost", port=6379, db=0)

def redis_thread():
    while True:
        time.sleep(1)
        for group_name in groups.keys():
            if s_redis.get(group_name):
                s_name, msg = s_redis.get(group_name).split(":")
                if s_name != server_name[:-1]:
                    logger.info("Got msg from server: {}, msg: {}".format(s_name, msg))
                    broadcast_groups(groups[group_name], msg, None)
                    s_redis.delete(group_name)

def snapshot():
    while True:
        logger.info("")
        logger.info("PERF  groups: {}".format(len(client_name_to_sock_mapping)))
        logger.info("PERF clients: {}".format(len(groups)))
        logger.info("")
        for grp_name, clients in groups.iteritems():
            logger.info("Group: {}".format(grp_name))
            for client in clients:
                logger.info("Connected at: {}".format(client.getpeername()))
        logger.info("--------------")
        logger.info(client_name_to_sock_mapping.keys())
        time.sleep(10)
   
def send_compute_to_client():
    time.sleep(5)
    print("Sleep over")
    global comp_res_expected
    comp_res_expected = len(client_name_to_sock_mapping.keys())
    while comp_res_expected != 0:
        print comp_res_expected
        for client_name, client_sock in client_name_to_sock_mapping.iteritems():
            client_indx = client_name_to_num_mapping[client_name]
            inp = ",".join(input_arr[comp_len*(client_indx-1):comp_len*client_indx])
            client_sock.sendall("COMPUTE " + inp)
        print("Computation not over yet, sleep(1)")
        time.sleep(2)
    if comp_res_expected == 0:
        print("Computation over {}".format(client_name_to_res_mapping))

    output_f = 0
    if comp_res_expected == 0:
        for key, value in client_name_to_res_mapping.iteritems():
            output_f += int(value)
    print("Final Output = {}".format(output_f))
        


def join_group(client, group_name, user_name=None):
    if group_name in groups:
        clientList = groups[group_name]
        if client not in clientList:
            clientList.append(client)
    else:
        groups[group_name] = [client]

	s_redis.set(group_name, server_name + str(user_name) + " joined the group")
    broadcast_groups(groups[group_name], str(user_name) + " joined the group")
    logger.debug("len(groups[group_name]): {}".format(groups[group_name]))

def register(client, request, user_name=None):
    logger.debug("Registering user: {}".format(request))

    return request

def broadcast_groups(clients, msg, user_name=None):
    msg = str(msg).encode('ascii')
    logger.debug("broadcasting to ")
    for client in clients:
        logger.debug("client: {}".format(client))
        client.send(msg)

def multicast_groups(client, msg, user_name=None):
    arr = msg.split(" ")
    group_name = arr[1]
    msg_out = "".join(arr[2:])
    s_redis.set(group_name, server_name + msg_out)
    broadcast_groups(groups[group_name], msg_out)
 
def panic_handler(client, request):
    msg = "Invalid Request: " + str(request)
    msg = msg.encode('ascii')
    client.send(msg)            

def private_msg(client, request, user_name=None):
    global client_name_to_sock_mapping
    msgList = request.split(" ",1)
    endUser = msgList[0].rstrip()
    if endUser  in client_name_to_sock_mapping:
        endUsersoc =  client_name_to_sock_mapping[endUser];
        msg = msgList[-1].encode('ascii')
        endUsersoc.send(msg)
    else:
        msg = "Invalid username: "+ str(endUser)
        msg.encode('ascii')
        client.send(msg)

    logger.info(client_name_to_sock_mapping)

def process_input(client, request, user_name=None):
    msgList  = request.split(" ", 1)
    print(msgList)
    global comp_res_expected
    if msgList[0] == "COMPUTE":
        comp_res_expected -= 1
        client_name_to_res_mapping[user_name] = msgList[-1]
        print("output from process_input = {}, user_name = {}".format(request, user_name))
        return None
    key = int(get_code_from_str(msgList[0]))
    msg = str(msgList[-1])

    function = switcher.get(key, panic_handler)
    if key == 2:
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
        logger.info("Connection to " +  str(addr));
        Thread(target=client_handler, args=(client,)).start()


def client_handler(client):
    global client_name_to_sock_mapping, client_num
    client.send(first_response + server_name[:-1] + ", Press ^C to exit")
    user_name = None
    while True:
        request = client.recv(RECV_BUFFER_LIMIT)
        if not user_name:
            user_name = process_input(client, request.decode('utf-8'))
            user_name = user_name.rstrip()
            client_name_to_num_mapping[user_name] = client_num
            client_num += 1
            if user_name not in client_name_to_sock_mapping.keys():
                client_name_to_sock_mapping[user_name] = client
            else:
                msg = "Username not available".encode('ascii')
                client.send(msg)
        else:
            process_input(client, request.decode('utf-8'), user_name)
        
    logger.info("Done!")

def boot_up():
    global switcher

    switcher = { 
        0: join_group,
        1: broadcast_groups,
        2: multicast_groups,
        3: private_msg,
        4: register
    }

boot_up()
#Thread(target=snapshot, args=()).start()
Thread(target=send_compute_to_client, args=()).start()
Thread(target=redis_thread, args=()).start()
server(('',int(sys.argv[1])))
