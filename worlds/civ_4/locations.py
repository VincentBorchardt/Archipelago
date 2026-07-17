from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import constants
from .items import Civ4Item

if TYPE_CHECKING:
    from .world import Civ4World

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.

class Civ4Location(Location):
    game = "Civilization IV"

# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: constants.LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: Civ4World) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: Civ4World) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    initial = world.get_region("Initial")

    # A simpler way to do this is by using the region.add_locations helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # Aha! So that's why we made that "get_location_names_with_ids" helper method earlier.
    # You also need to pass your overridden Location class.

    if world.options.techsanity:
        ancient_techs = get_location_names_with_ids(constants.ARCHIPELAGO_ANCIENT_TECHS)
        classical_techs = get_location_names_with_ids(constants.ARCHIPELAGO_CLASSICAL_TECHS)
        medieval_techs = get_location_names_with_ids(constants.ARCHIPELAGO_MEDIEVAL_TECHS)
        renaissance_techs = get_location_names_with_ids(constants.ARCHIPELAGO_RENAISSANCE_TECHS)
        industrial_techs = get_location_names_with_ids(constants.ARCHIPELAGO_INDUSTRIAL_TECHS)
        modern_techs = get_location_names_with_ids(constants.ARCHIPELAGO_MODERN_TECHS)
        future_techs = get_location_names_with_ids(constants.ARCHIPELAGO_FUTURE_TECHS)

        initial.add_locations(ancient_techs, Civ4Location)

        if world.options.techsanity_era_gates:
            classical_era = world.get_region("Classical Tech Access")
            medieval_era = world.get_region("Medieval Tech Access")
            renaissance_era = world.get_region("Renaissance Tech Access")
            industrial_era = world.get_region("Industrial Tech Access")
            modern_era = world.get_region("Modern Tech Access")
            future_era = world.get_region("Future Tech Access")
            classical_era.add_locations(classical_techs, Civ4Location)
            medieval_era.add_locations(medieval_techs, Civ4Location)
            renaissance_era.add_locations(renaissance_techs, Civ4Location)
            industrial_era.add_locations(industrial_techs, Civ4Location)
            modern_era.add_locations(modern_techs, Civ4Location)
            future_era.add_locations(future_techs, Civ4Location)
        else:
            initial.add_locations(classical_techs, Civ4Location)
            initial.add_locations(medieval_techs, Civ4Location)
            initial.add_locations(renaissance_techs, Civ4Location)
            initial.add_locations(industrial_techs, Civ4Location)
            initial.add_locations(modern_techs, Civ4Location)
            initial.add_locations(future_techs, Civ4Location)




def create_events(world: Civ4World) -> None:
    # Sometimes, the player may perform in-game actions that allow them to progress which are not related to Items.
    # In our case, the player must press a button in the top left room to open the final boss door.
    # AP has something for this purpose: "Event locations" and "Event items".
    # An event location is no different than a regular location, except it has the address "None".
    # It is treated during generation like any other location, but then it is discarded.
    # This location cannot be "sent" and its item cannot be "received", but the item can be used in logic rules.
    # Since we are creating more locations and adding them to regions, we need to grab those regions again first.
    initial = world.get_region("Initial")
    # TODO add filters for different types of victory (both limiting the normal types and adding faster ones)
    initial.add_event("Conquest Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
    initial.add_event("Domination Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
    initial.add_event("Cultural Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
    initial.add_event("Spaceship Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
    initial.add_event("Diplomatic Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
    initial.add_event("Time Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
