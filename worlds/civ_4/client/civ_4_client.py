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
import json

# TODO NEED TO WRITE A SAFE UNPICKLER!!!
import pickle

server_for_civ_4 = None
civ_4_writer = None

# APQuest overrides ClientCommandProcessor, I don't think I need to, at least not yet

class Civ4Context(CommonContext):
    game = "Civilization IV"
    items_handling = 0b111  # full remote

    #communication_task = None

    async def civ4_loop(self):
        while not self.exit_event.is_set():
            pass

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(Civ4Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def async_server(self, reader, writer):
        global civ_4_writer
        civ_4_writer = writer

        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = await reader.read(1024)

            if not data:
                # if data is not received break
                break
            converted_data = pickle.loads(data)
            if converted_data["type"] == "connect":
                self.server_address = converted_data["server"]
                self.auth = converted_data["username"]
                self.password = converted_data["password"]
                self.server_task = asyncio.create_task(server_loop(self), name="server loop")
            elif converted_data["type"] == "LocationChecks":
                locations = converted_data["locations"]
                await self.check_locations(locations)
            print("from connected user: " + str(converted_data))


    def send_message_to_civ_4(self, cmd: str, args: dict[str, Any]) -> None:
        print(str(args))
        message_dict = {"cmd": cmd}
        message_pickle = pickle.dumps(message_dict, protocol=2)
        civ_4_writer.write(message_pickle)
        civ_4_writer.drain()

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        print("cmd = " + str(cmd))
        if cmd == "ConnectionRefused":
            self.send_message_to_civ_4(cmd, args)
        if cmd == "Connected":
            print("args = " + str(args))
            self.send_message_to_civ_4(cmd, args)
    
    def handle_connection_loss(self, msg: str) -> None:
        super().handle_connection_loss(msg)
        # I think this might break stuff with the new format
        self.send_message_to_civ_4("ConnectionLoss", {"msg": msg})
        

# DELETED 'args: Namespace' FROM THIS SINCE IT WOULDN'T RUN
async def main() -> None:

    ctx = Civ4Context()
    global server_for_civ_4
    #ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    # CLIENT LOOP STUFF GOES HERE

    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    #ctx.communication_task = asyncio.create_task(server_program_noninteractive(), name="communication loop")

    server_for_civ_4 = await asyncio.start_server(ctx.async_server, host, port)
    await server_for_civ_4.start_serving()

    await ctx.exit_event.wait()
    await ctx.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
