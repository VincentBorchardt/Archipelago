import asyncio
import sys
from argparse import Namespace
from enum import Enum
import typing
from typing import TYPE_CHECKING, Any

from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop
from NetUtils import ClientStatus, NetworkItem, HintStatus
from Utils import gui_enabled

import socket
import select
import json

# TODO NEED TO WRITE A SAFE UNPICKLER!!!
import pickle

server_for_civ_4 = None
civ_4_writer = None

status_names: typing.Dict[HintStatus, str] = {
    HintStatus.HINT_FOUND: "Found",
    HintStatus.HINT_UNSPECIFIED: "Unspecified",
    HintStatus.HINT_NO_PRIORITY: "No Priority",
    HintStatus.HINT_AVOID: "Avoid",
    HintStatus.HINT_PRIORITY: "Priority",
}
status_colors: typing.Dict[HintStatus, str] = {
    HintStatus.HINT_FOUND: "green",
    HintStatus.HINT_UNSPECIFIED: "white",
    HintStatus.HINT_NO_PRIORITY: "cyan",
    HintStatus.HINT_AVOID: "salmon",
    HintStatus.HINT_PRIORITY: "plum",
}

# APQuest overrides ClientCommandProcessor, I don't think I need to, at least not yet

class Civ4Context(CommonContext):
    game = "Civilization IV"
    items_handling = 0b111  # full remote

    # TODO force the client closed and/or reset this when the game is closed
    send_index = 0

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
            if converted_data["type"] == "Connect":
                self.server_address = converted_data["server"]
                self.auth = converted_data["username"]
                self.password = converted_data["password"]
                self.server_task = asyncio.create_task(server_loop(self), name="server loop")
            # TODO Put a "connect" here that doesn't send anything back unless things break
            elif converted_data["type"] == "LocationChecks":
                locations = converted_data["locations"]
                await self.check_locations(locations)
            elif converted_data["type"] == "ReceiveItems":
                items = []
                print(self.items_received)
                while self.send_index < len(self.items_received):
                    transfer_item: NetworkItem = self.items_received[self.send_index]
                    item_id = transfer_item.item
                    player_name = self.player_names[transfer_item.player]
                    item_name = self.item_names.lookup_in_game(item_id)
                    item_dict = {"item_id": item_id, "player": player_name, "name": item_name, "index": self.send_index}
                    items.append(item_dict)
                    self.send_index += 1
                self.send_message_to_civ_4("ReceiveItems", {"items": items})
            elif converted_data["type"] == "GetHints":
                print(str(self.stored_data))
                hints_tuples = self.stored_data.get(f"_read_hints_{self.team}_{self.slot}", [])
                print(str(hints_tuples))
                data = []
                for hint in hints_tuples:
                    data.append(self.parse_hint(hint))
                print(data)
                hint_dict = {"hints" : data}
                self.send_message_to_civ_4("GetHints", hint_dict)
            elif converted_data["type"] == "Victory":
                # TODO check the type to see if it's valid in the settings
                status_dict = {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}
                await self.send_msgs([status_dict])

            elif converted_data["type"] == "GetSettings":
                pass
            elif converted_data["type"] == "Command":
                command = converted_data["cmd"]
                if command:
                    commandprocessor = self.command_processor(self)
                    commandprocessor(command)

            print("from connected user: " + str(converted_data))

    def parse_hint(self, hint):
        if not hint.get("status"):  # Allows connecting to old servers
            hint["status"] = HintStatus.HINT_FOUND if hint["found"] else HintStatus.HINT_UNSPECIFIED
        result_dict = {
            "receiving_player": self.player_names[hint["receiving_player"]],
            "item": self.item_names.lookup_in_slot(hint["item"], hint["receiving_player"]),
            "item_type": self.parse_flags(hint["item_flags"]),
            "finding_player": self.player_names[hint["finding_player"]],
            "location": self.location_names.lookup_in_slot(hint["location"], hint["finding_player"]),
            "entrance": hint["entrance"] if hint["entrance"] else "Vanilla",
            "status": status_names.get(hint["status"], "Unknown"),
            }
        return result_dict

    def parse_flags(self, flags):
        # TODO Figure out how combinations of flags work (Progression + Useful, etc)
        if flags == 0:
            return "Filler"
        elif flags & 0b001:  # advancement
            return "Progression"
        elif flags & 0b010:  # useful
            return "Useful"
        elif flags & 0b100:  # trap
            return "Trap"
        else:
            return "Filler"

    def send_message_to_civ_4(self, cmd: str, args: dict[str, Any]) -> None:
        if civ_4_writer is None:
            print(f"Cannot send '{cmd}': Civilization 4 client is not connected yet.")
            return
        print(str(args))
        message_dict = {"cmd": cmd}
        # TODO make this more general without putting something in the pickle Civ4 will choke on
        if args and cmd == "Connected":
            slot_data = args.get("slot_data")
            print(str(slot_data))
            if slot_data:
                message_dict["techsanity"] = slot_data.get("techsanity")
                message_dict["techsanity_era_gates"] = slot_data.get("techsanity_era_gates")
                message_dict["gpsanity"] = slot_data.get("gpsanity")
                message_dict["world_wondersanity"] = slot_data.get("world_wondersanity")
        if args and cmd == "ReceiveItems":
            message_dict = args | message_dict
        if args and cmd == "GetHints":
            message_dict = args | message_dict
        print(str(message_dict))
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
        if cmd == "PrintJSON":
            pass
            # TODO make this batch data in a list, so it can be specifically requested later
            #print(args.get("data"))

    def handle_connection_loss(self, msg: str) -> None:
        super().handle_connection_loss(msg)
        # I think this might break stuff with the new format
        #self.send_message_to_civ_4("ConnectionLoss", {"msg": msg})


# DELETED 'args: Namespace' FROM THIS SINCE IT WOULDN'T RUN
async def main(*args) -> None:
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
