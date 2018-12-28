from flask import Flask
from redis import StrictRedis
from time import sleep
from threading import Thread

app = Flask(__name__)

curr_server = 0
servers = []
curr_server_list = ""
s_redis = StrictRedis(host="localhost", port=6379, db=0)

def populate_servers():
    global servers
    servers = curr_server_list.split(",")

def sync_servers():
    global curr_server_list
    while 1:
        print("Syncing from DS")
        server_list = s_redis.get("servers")       
        print("Server list: {}".format(server_list))
        if server_list != curr_server_list:
            curr_server_list = server_list
            populate_servers()
        sleep(4)

@app.route("/server")
def get_server():
    global curr_server
    if curr_server + 1 == len(servers):
        curr_server = 0
    else:
        curr_server += 1

    return servers[curr_server]

# Polling thread for servers
Thread(target=sync_servers, args=()).start()

# API Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6666)
