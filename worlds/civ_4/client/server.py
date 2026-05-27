import asyncio
import sys
from argparse import Namespace
from enum import Enum
from typing import TYPE_CHECKING, Any

from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop
from NetUtils import ClientStatus
from Utils import gui_enabled

import socket
import socketserver

class ArchipelagoHandler(socketserver.StreamRequestHandler):
    def handle(self):
        data = self.rfile.readline()
        print("from connected user: " + str(data))
        #data = input(' -> ')
        self.wfile.write(data)

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection

def serverProgramB():
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024
    server = socketserver.TCPServer((host, port), ArchipelagoHandler)
    server.serve_forever()

if __name__ == '__main__':
    server_program()
