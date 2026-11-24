from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from .world import Civ4World

def gated_techsanity(world) -> bool:
    return world.options.techsanity and world.options.techsanity_era_gates > 0

def create_and_connect_regions(world: Civ4World) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: Civ4World) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    initial = Region("Initial", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [initial]

    if gated_techsanity(world):
        tech_regions = create_tech_regions(world)
        regions += tech_regions

    if world.options.gpsanity > 0:
        gp_regions = create_gp_regions(world)
        regions += gp_regions

    if world.options.resourcesanity:
        resource_regions = create_resource_regions(world)
        regions += resource_regions

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def create_tech_regions(world: Civ4World) -> list[Region]:
    classical_access = Region("Classical Tech Access", world.player, world.multiworld)
    medieval_access = Region("Medieval Tech Access", world.player, world.multiworld)
    renaissance_access = Region("Renaissance Tech Access", world.player, world.multiworld)
    industrial_access = Region("Industrial Tech Access", world.player, world.multiworld)
    modern_access = Region("Modern Tech Access", world.player, world.multiworld)
    future_access = Region("Future Tech Access", world.player, world.multiworld)

    regions = [
        classical_access,
        medieval_access,
        renaissance_access,
        industrial_access,
        modern_access,
        future_access
    ]

    return regions

def create_gp_regions(world: Civ4World) -> list[Region]:
    great_scientist_access = Region("Great Scientist Access", world.player, world.multiworld)
    great_artist_access = Region("Great Artist Access", world.player, world.multiworld)
    great_merchant_access = Region("Great Merchant Access", world.player, world.multiworld)
    great_spy_access = Region("Great Spy Access", world.player, world.multiworld)
    great_general_access = Region("Great General Access", world.player, world.multiworld)
    great_prophet_access = Region("Great Prophet Access", world.player, world.multiworld)
    great_engineer_access = Region("Great Engineer Access", world.player, world.multiworld)

    regions = [
        great_scientist_access,
        great_artist_access,
        great_merchant_access,
        great_spy_access,
        great_general_access,
        great_prophet_access,
        great_engineer_access
    ]

    return regions

def create_resource_regions(world: Civ4World) -> list[Region]:
    road_access = Region("Road Access", world.player, world.multiworld)
    mining_access = Region("Mining Access", world.player, world.multiworld)
    farming_access = Region("Farming Access", world.player, world.multiworld)
    calendar_access = Region("Calendar Access", world.player, world.multiworld)
    hunting_access = Region("Hunting Access", world.player, world.multiworld)
    fishing_access = Region("Fishing Access", world.player, world.multiworld)
    animal_access = Region("Animal Access", world.player, world.multiworld)
    masonry_access = Region("Masonry Access", world.player, world.multiworld)
    winery_access = Region("Winery Access", world.player, world.multiworld)
    oil_access = Region("Oil Access", world.player, world.multiworld)

    regions = [
        road_access,
        mining_access,
        farming_access,
        calendar_access,
        hunting_access,
        fishing_access,
        animal_access,
        masonry_access,
        winery_access,
        oil_access,
    ]

    return regions

def connect_regions(world: Civ4World) -> None:
    # We have regions now, but still need to connect them to each other.
    # Once you've submitted your regions to multiworld.regions, you can get them at any time using world.get_region(...).
    initial = world.get_region("Initial")

    if gated_techsanity(world):
        classical = world.get_region("Classical Tech Access")
        medieval = world.get_region("Medieval Tech Access")
        renaissance = world.get_region("Renaissance Tech Access")
        industrial = world.get_region("Industrial Tech Access")
        modern = world.get_region("Modern Tech Access")
        future = world.get_region("Future Tech Access")
        initial.connect(classical, "Ancient to Classical")
        classical.connect(medieval, "Classical to Medieval")
        medieval.connect(renaissance, "Medieval to Renaissance")
        renaissance.connect(industrial, "Renaissance to Industrial")
        industrial.connect(modern, "Industrial to Modern")
        modern.connect(future, "Modern to Future")

    if world.options.gpsanity > 0:
        great_scientist = world.get_region("Great Scientist Access")
        great_artist = world.get_region("Great Artist Access")
        great_spy = world.get_region("Great Spy Access")
        great_general = world.get_region("Great General Access")
        great_prophet = world.get_region("Great Prophet Access")
        great_engineer = world.get_region("Great Engineer Access")
        great_merchant = world.get_region("Great Merchant Access")
        initial.connect(great_scientist, "Can Produce Great Scientist")
        initial.connect(great_artist, "Can Produce Great Artist")
        initial.connect(great_spy, "Can Produce Great Spy")
        initial.connect(great_general, "Can Produce Great General")
        initial.connect(great_prophet, "Can Produce Great Prophet")
        initial.connect(great_engineer, "Can Produce Great Engineer")
        initial.connect(great_merchant, "Can Produce Great Merchant")

    if world.options.resourcesanity:
        roads = world.get_region("Road Access")
        mining = world.get_region("Mining Access")
        farming = world.get_region("Farming Access")
        calendar = world.get_region("Calendar Access")
        hunting = world.get_region("Hunting Access")
        fishing = world.get_region("Fishing Access")
        animal = world.get_region("Animal Access")
        masonry = world.get_region("Masonry Access")
        winery = world.get_region("Winery Access")
        oil = world.get_region("Oil Access")
        initial.connect(roads, "Can Produce Roads")
        roads.connect(mining, "Can Connect Mining Resources")
        roads.connect(farming, "Can Connect Farming Resources")
        roads.connect(calendar, "Can Connect Calendar Resources")
        roads.connect(hunting, "Can Connect Hunting Resources")
        initial.connect(fishing, "Can Connect Fishing Resources")
        roads.connect(animal, "Can Connect Animal Resources")
        roads.connect(masonry, "Can Connect Masonry Resources")
        roads.connect(winery, "Can Connect Winery Resources")
        roads.connect(oil, "Can Connect Oil Resources")


