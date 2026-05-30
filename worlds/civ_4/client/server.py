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

    #communication_task = None

    async def civ4_loop(self):
        while not self.exit_event.is_set():
            pass

    async def async_server(self, reader, writer):
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = await reader.read(1024)
            data = data.decode()
            if not data:
                # if data is not received break
                break
            login_info = data.split(';')
            self.server_address = login_info[0]
            self.auth = login_info[1]
            self.password = login_info[2]
            self.server_task = asyncio.create_task(server_loop(self), name="server loop")
            print("from connected user: " + str(login_info))
            new_data = "This is a non-interactive test of stuff".encode()
            writer.write(new_data)  # send data to the client
            await writer.drain()  # Flow control, see later

# DELETED 'args: Namespace' FROM THIS SINCE IT WOULDN'T RUN
async def main() -> None:

    ctx = Civ4Context()
    #ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    # CLIENT LOOP STUFF GOES HERE

    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    #ctx.communication_task = asyncio.create_task(server_program_noninteractive(), name="communication loop")

    server = await asyncio.start_server(ctx.async_server, host, port)
    await server.start_serving()

    await ctx.exit_event.wait()
    await ctx.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
