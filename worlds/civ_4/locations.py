from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import Civ4World

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
LOCATION_NAME_TO_ID = {
    # --- Technology Locations (IDs 1 - 92) ---
    "Archipelago The Wheel": 1,
    "Archipelago Agriculture": 2,
    "Archipelago Animal Husbandry": 3,
    "Archipelago Fishing": 4,
    "Archipelago Hunting": 5,
    "Archipelago Mysticism": 6,
    "Archipelago Archery": 7,
    "Archipelago Pottery": 8,
    "Archipelago Writing": 9,
    "Archipelago Sailing": 10,
    "Archipelago Masonry": 11,
    "Archipelago Mining": 12,
    "Archipelago Priesthood": 13,
    "Archipelago Bronze Working": 14,
    "Archipelago Polytheism": 15,
    "Archipelago Monotheism": 16,
    "Archipelago Meditation": 17,
    "Archipelago Monarchy": 18,
    "Archipelago Alphabet": 19,
    "Archipelago Mathematics": 20,
    "Archipelago Construction": 21,
    "Archipelago Code Of Laws": 22,
    "Archipelago Metal Casting": 23,
    "Archipelago Compass": 24,
    "Archipelago Currency": 25,
    "Archipelago Horseback Riding": 26,
    "Archipelago Drama": 27,
    "Archipelago Calendar": 28,
    "Archipelago Iron Working": 29,
    "Archipelago Literature": 30,
    "Archipelago Aesthetics": 31,
    "Archipelago Banking": 32,
    "Archipelago Engineering": 33,
    "Archipelago Guilds": 34,
    "Archipelago Feudalism": 35,
    "Archipelago Machinery": 36,
    "Archipelago Civil Service": 37,
    "Archipelago Philosophy": 38,
    "Archipelago Optics": 39,
    "Archipelago Theology": 40,
    "Archipelago Paper": 41,
    "Archipelago Music": 42,
    "Archipelago Divine Right": 43,
    "Archipelago Economics": 44,
    "Archipelago Constitution": 45,
    "Archipelago Astronomy": 46,
    "Archipelago Democracy": 47,
    "Archipelago Education": 48,
    "Archipelago Chemistry": 49,
    "Archipelago Corporation": 50,
    "Archipelago Replaceable Parts": 51,
    "Archipelago Gunpowder": 52,
    "Archipelago Rifling": 53,
    "Archipelago Printing Press": 54,
    "Archipelago Nationalism": 55,
    "Archipelago Military Science": 56,
    "Archipelago Military Tradition": 57,
    "Archipelago Liberalism": 58,
    "Archipelago Railroad": 59,
    "Archipelago Electricity": 60,
    "Archipelago Assembly Line": 61,
    "Archipelago Steel": 62,
    "Archipelago Medicine": 63,
    "Archipelago Industrialism": 64,
    "Archipelago Communism": 65,
    "Archipelago Scientific Method": 66,
    "Archipelago Steam Power": 67,
    "Archipelago Fission": 68,
    "Archipelago Combustion": 69,
    "Archipelago Biology": 70,
    "Archipelago Physics": 71,
    "Archipelago Fascism": 72,
    "Archipelago Artillery": 73,
    "Archipelago Radio": 74,
    "Archipelago Flight": 75,
    "Archipelago Mass Media": 76,
    "Archipelago Plastics": 77,
    "Archipelago Computers": 78,
    "Archipelago Ecology": 79,
    "Archipelago Refrigeration": 80,
    "Archipelago Rocketry": 81,
    "Archipelago Robotics": 82,
    "Archipelago Satellites": 83,
    "Archipelago Laser": 84,
    "Archipelago Fiber Optics": 85,
    "Archipelago Advanced Flight": 86,
    "Archipelago Superconductors": 87,
    "Archipelago Composites": 88,
    "Archipelago Fusion": 89,
    "Archipelago Genetics": 90,
    "Archipelago Stealth": 91,
    "Archipelago Future Tech": 92,

    # --- Great Person Sanity Locations (IDs 101 - 170) ---
    "Great Scientist Check 1": 101,
    "Great Scientist Check 2": 102,
    "Great Scientist Check 3": 103,
    "Great Scientist Check 4": 104,
    "Great Scientist Check 5": 105,
    "Great Scientist Check 6": 106,
    "Great Scientist Check 7": 107,
    "Great Scientist Check 8": 108,
    "Great Scientist Check 9": 109,
    "Great Scientist Check 10": 110,

    "Great Engineer Check 1": 111,
    "Great Engineer Check 2": 112,
    "Great Engineer Check 3": 113,
    "Great Engineer Check 4": 114,
    "Great Engineer Check 5": 115,
    "Great Engineer Check 6": 116,
    "Great Engineer Check 7": 117,
    "Great Engineer Check 8": 118,
    "Great Engineer Check 9": 119,
    "Great Engineer Check 10": 120,

    "Great Prophet Check 1": 121,
    "Great Prophet Check 2": 122,
    "Great Prophet Check 3": 123,
    "Great Prophet Check 4": 124,
    "Great Prophet Check 5": 125,
    "Great Prophet Check 6": 126,
    "Great Prophet Check 7": 127,
    "Great Prophet Check 8": 128,
    "Great Prophet Check 9": 129,
    "Great Prophet Check 10": 130,

    "Great Artist Check 1": 131,
    "Great Artist Check 2": 132,
    "Great Artist Check 3": 133,
    "Great Artist Check 4": 134,
    "Great Artist Check 5": 135,
    "Great Artist Check 6": 136,
    "Great Artist Check 7": 137,
    "Great Artist Check 8": 138,
    "Great Artist Check 9": 139,
    "Great Artist Check 10": 140,

    "Great Merchant Check 1": 141,
    "Great Merchant Check 2": 142,
    "Great Merchant Check 3": 143,
    "Great Merchant Check 4": 144,
    "Great Merchant Check 5": 145,
    "Great Merchant Check 6": 146,
    "Great Merchant Check 7": 147,
    "Great Merchant Check 8": 148,
    "Great Merchant Check 9": 149,
    "Great Merchant Check 10": 150,

    "Great General Check 1": 151,
    "Great General Check 2": 152,
    "Great General Check 3": 153,
    "Great General Check 4": 154,
    "Great General Check 5": 155,
    "Great General Check 6": 156,
    "Great General Check 7": 157,
    "Great General Check 8": 158,
    "Great General Check 9": 159,
    "Great General Check 10": 160,

    "Great Spy Check 1": 161,
    "Great Spy Check 2": 162,
    "Great Spy Check 3": 163,
    "Great Spy Check 4": 164,
    "Great Spy Check 5": 165,
    "Great Spy Check 6": 166,
    "Great Spy Check 7": 167,
    "Great Spy Check 8": 168,
    "Great Spy Check 9": 169,
    "Great Spy Check 10": 170,
}

class Civ4Location(Location):
    game = "Civilization IV"

# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: Civ4World) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: Civ4World) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    initial = world.get_region("Initial")

    # One way to create locations is by just creating them directly via their constructor.
    ap_tech_1 = Civ4Location(
        world.player, "Archipelago Tech 1", world.location_name_to_id["Archipelago Tech 1"], initial
    )

    # You can then add them to the region.
    initial.locations.append(ap_tech_1)

    # A simpler way to do this is by using the region.add_locations helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # Aha! So that's why we made that "get_location_names_with_ids" helper method earlier.
    # You also need to pass your overridden Location class.


def create_events(world: Civ4World) -> None:
    # Sometimes, the player may perform in-game actions that allow them to progress which are not related to Items.
    # In our case, the player must press a button in the top left room to open the final boss door.
    # AP has something for this purpose: "Event locations" and "Event items".
    # An event location is no different than a regular location, except it has the address "None".
    # It is treated during generation like any other location, but then it is discarded.
    # This location cannot be "sent" and its item cannot be "received", but the item can be used in logic rules.
    # Since we are creating more locations and adding them to regions, we need to grab those regions again first.
    pass
