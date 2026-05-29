import asyncio
import sys
from argparse import Namespace
from enum import Enum
from typing import TYPE_CHECKING, Any

from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop
from NetUtils import ClientStatus
from Utils import gui_enabled

import socket
import select

# APQuest overrides ClientCommandProcessor, I don't think I need to, at least not yet

class Civ4Context(CommonContext):
    game = "Civilization IV"
    items_handling = 0b111  # full remote

    communication_task = None

    async def civ4_loop(self):
        while not self.exit_event.is_set():
            pass



def server_program():
    # THIS NEEDS TO BE ITS OWN THING

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

async def server_program_noninteractive():
    # THIS NEEDS TO BE ITS OWN THING
    print("starting server program")

    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    print(host)

    server_socket = socket.socket()  # get instance
    print("started socket")
    #server_socket.setblocking(False)
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("about to start listening")

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    #input = [server_socket]
    await asyncio.sleep(0.1)
    #inputready, outputready, exceptready = select.select(input, [], [], 0)
    conn = None
    address = None
    print("about to enter the loop")
    while conn is None:
        print("starting loop")
        conn, address = server_socket.accept()  # accept new connection
        await asyncio.sleep(3)
        print("did a loop")
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = "This is a non-interactive test of stuff"
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection

async def async_server(reader, writer):
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = await reader.read(1024)
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = "This is a non-interactive test of stuff"
        writer.write(data) # send data to the client
        #await writer.drain()  # Flow control, see later

# DELETED 'args: Namespace' FROM THIS SINCE IT WOULDN'T RUN
async def main() -> None:
    print("in main")

    ctx = Civ4Context()
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    # CLIENT LOOP STUFF GOES HERE
    # Presumably this needs to be replaced with a task something or other

    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server = await asyncio.start_server(async_server, host, port)
    await server.serve_forever()

    #ctx.communication_task = asyncio.create_task(server_program_noninteractive(), name="communication loop")

    await ctx.exit_event.wait()
    await ctx.shutdown()

if __name__ == '__main__':
    #server_program()

    asyncio.run(main())
