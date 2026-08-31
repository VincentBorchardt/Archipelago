from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from .constants import *
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
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

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
        ancient_techs = get_location_names_with_ids(ARCHIPELAGO_ANCIENT_TECHS)
        classical_techs = get_location_names_with_ids(ARCHIPELAGO_CLASSICAL_TECHS)
        medieval_techs = get_location_names_with_ids(ARCHIPELAGO_MEDIEVAL_TECHS)
        renaissance_techs = get_location_names_with_ids(ARCHIPELAGO_RENAISSANCE_TECHS)
        industrial_techs = get_location_names_with_ids(ARCHIPELAGO_INDUSTRIAL_TECHS)
        modern_techs = get_location_names_with_ids(ARCHIPELAGO_MODERN_TECHS)
        future_techs = get_location_names_with_ids(ARCHIPELAGO_FUTURE_TECHS)

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
    else:
        # TODO make events for each tech if techsanity isn't on
        for item in FULL_TECH_ARRAY:
            location = item + " Location"
            initial.add_event(location, item, location_type=Civ4Location, item_type=Civ4Item)

    gpsanity_amount = world.options.gpsanity
    if gpsanity_amount > 0:
        scientist_region = world.get_region("Great Scientist Access")
        scientist_locations = get_location_names_with_ids(GREAT_SCIENTIST_LOCATIONS[0:gpsanity_amount])
        scientist_region.add_locations(scientist_locations, Civ4Location)

        artist_region = world.get_region("Great Artist Access")
        artist_locations = get_location_names_with_ids(GREAT_ARTIST_LOCATIONS[0:gpsanity_amount])
        artist_region.add_locations(artist_locations, Civ4Location)

        engineer_region = world.get_region("Great Engineer Access")
        engineer_locations = get_location_names_with_ids(GREAT_ENGINEER_LOCATIONS[0:gpsanity_amount])
        engineer_region.add_locations(engineer_locations, Civ4Location)

        merchant_region = world.get_region("Great Merchant Access")
        merchant_locations = get_location_names_with_ids(GREAT_MERCHANT_LOCATIONS[0:gpsanity_amount])
        merchant_region.add_locations(merchant_locations, Civ4Location)

        prophet_region = world.get_region("Great Prophet Access")
        prophet_locations = get_location_names_with_ids(GREAT_PROPHET_LOCATIONS[0:gpsanity_amount])
        prophet_region.add_locations(prophet_locations, Civ4Location)

        general_region = world.get_region("Great General Access")
        general_locations = get_location_names_with_ids(GREAT_GENERAL_LOCATIONS[0:gpsanity_amount])
        general_region.add_locations(general_locations, Civ4Location)

        spy_region = world.get_region("Great Spy Access")
        spy_locations = get_location_names_with_ids(GREAT_SPY_LOCATIONS[0:gpsanity_amount])
        spy_region.add_locations(spy_locations, Civ4Location)

    if world.options.world_wondersanity:
        world_wonders = get_location_names_with_ids(WORLD_WONDER_LOCATIONS)
        initial.add_locations(world_wonders, Civ4Location)

    if world.options.national_wondersanity:
        national_wonders = get_location_names_with_ids(NATIONAL_WONDER_LOCATIONS)
        initial.add_locations(national_wonders, Civ4Location)



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
    # TODO This also doesn't appear to mean anything yet
    initial.add_event("Conquest Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
    initial.add_event("Domination Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
    initial.add_event("Cultural Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
    initial.add_event("Spaceship Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
    initial.add_event("Diplomatic Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
    initial.add_event("Time Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
    initial.add_event("Score Victory", "Victory", location_type=Civ4Location, item_type=Civ4Item)
