from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from .world import Civ4World

def gated_techsanity(world) -> bool:
    return world.options.techsanity and world.options.techsanity_era_gates

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

def connect_regions(world: Civ4World) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
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

