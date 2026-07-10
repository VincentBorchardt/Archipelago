from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import Civ4World

ANCIENT_TECHS = [
    "The Wheel",
    "Agriculture",
    "Animal Husbandry",
    "Fishing",
    "Hunting",
    "Mysticism",
    "Archery",
    "Pottery",
    "Writing",
    "Sailing",
    "Masonry",
    "Mining",
    "Priesthood",
    "Bronze Working",
    "Polytheism",
    "Meditation",
    "Monotheism",
]

CLASSICAL_TECHS = [
    "Calendar",
    "Monarchy",
    "Alphabet",
    "Mathematics",
    "Construction",
    "Code of Laws",
    "Metal Casting",
    "Compass",
    "Currency",
    "Horseback Riding",
    "Iron Working",
    "Literature",
    "Aesthetics",
    "Drama",
]

MEDIEVAL_TECHS = [
    "Feudalism",
    "Machinery",
    "Civil Service",
    "Guilds",
    "Philosophy",
    "Optics",
    "Theology",
    "Paper",
    "Music",
    "Divine Right",
    "Banking",
    "Engineering"
]

RENAISSANCE_TECHS = [
    "Economics",
    "Constitution",
    "Astronomy",
    "Democracy",
    "Education",
    "Chemistry",
    "Corporation",
    "Replaceable Parts",
    "Gunpowder",
    "Rifling",
    "Printing Press",
    "Nationalism",
    "Military Science",
    "Military Tradition",
    "Liberalism"
]

INDUSTRIAL_TECHS = [
    "Railroad",
    "Electricity",
    "Assembly Line",
    "Steel",
    "Medicine",
    "Industrialism",
    "Communism",
    "Scientific Method",
    "Steam Power",
    "Fission",
    "Combustion",
    "Biology",
    "Physics",
    "Fascism",
    "Artillery"
]

MODERN_TECHS = [
    "Radio",
    "Flight",
    "Mass Media",
    "Plastics",
    "Computers",
    "Ecology",
    "Refrigeration",
    "Rocketry",
    "Robotics",
    "Satellites",
    "Laser",
    "Fiber Optics",
    "Advanced Flight",
    "Superconductors",
    "Composites"
]

FUTURE_TECHS = [
    "Fusion",
    "Genetics",
    "Stealth",
    "Future Tech"
]



def create_and_connect_regions(world: Civ4World) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: Civ4World) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    initial = Region("Initial", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [initial]

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions

def connect_regions(world: Civ4World) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    initial = world.get_region("Initial")

    # ENTRANCE STUFF GOES HERE
