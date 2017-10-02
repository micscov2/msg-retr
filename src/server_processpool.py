#!/router/bin/python3
# This is server.py file

from socket import *                         # Import socket module
from threading import Thread                 # Import Thread module
from concurrent.futures import ProcessPoolExecutor as Pool

pool = Pool(4)
RECV_BUFFER_LIMIT = 2048
first_response = str("SERVER>>").encode('ascii')


def fib(n):
    n = int(n)
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def processInput(client_input):
    no = int(client_input)
    switcher = {
        0: "Join the group",
        1: "Create the group",
        2: "Send a multicast msg",
        3: "Send a private msg",
    }
    return switcher.get(no, "Wrong Number")

def server(address):
    sock = socket(AF_INET, SOCK_STREAM)          # Create a socket object
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Set socket options
    sock.bind(address)                           # Bind to the port
    sock.listen(5)                               # Now wait for client connection.
    while True:
        client, addr = sock.accept()      # Establish connection with client.
        print("Connection to ",addr);
        Thread(target=client_handler, args=(client,), daemon=True).start()


def client_handler(client):
    while True:
        client.send(first_response)
        req = client.recv(RECV_BUFFER_LIMIT)
        if not req:
            print("Closing connection")
            break
        subProcess = pool.submit(processInput, req)
        result = subProcess.result()
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
