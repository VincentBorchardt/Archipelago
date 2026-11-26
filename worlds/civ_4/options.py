from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, DefaultOnToggle


class Techsanity(DefaultOnToggle):
    """
    Shuffles technologies into the multiworld.
    You need the real techs to research the locations corresponding to the technologies that require them.
    """

    display_name = "Techsanity"

class TechsanityEraGates(Range):
    """
    Requires you to have a certain percentage of technologies in a given era before the next era's locations are in logic.
    Prevents you from needing to research extremely expensive technologies early, before you have the infrastructure.
    Currently requires all previous eras to reach the threshold.
    """

    display_name = "Gate Technology Locations by Era"

    range_start = 0
    range_end = 80
    default = 50

class GPsanity(Range):
    """
    Turns great person bulbs into locations in the multiworld.
    This also includes Great Generals and Great Spies.
    Change to 0 to fully disable GPsanity.
    Warning: Currently not biased towards lower numbers, so be careful with high numbers.
    """

    display_name = "GPsanity"

    range_start = 0
    range_end = 10
    default = 3

class WorldWondersanity(DefaultOnToggle):
    """
    Turns completed World Wonders into locations in the multiworld.
    Warning: As wonders are still limited to one in the world, you may need to start a new game to realistically build them.
    """

    display_name = "World Wonders"

class NationalWondersanity(DefaultOnToggle):
    """
    Turns completed National Wonders into locations in the multiworld.
    """

    display_name = "National Wonders"

class Resourcesanity(DefaultOnToggle):
    """
    Turns connected resources into locations in the multiworld.
    Only counts resources connected to the capital.
    """

    display_name = "Resources"

class UniqueUnitItems(DefaultOnToggle):
    """
    Adds the ability to build unique units to the item pool.
    May not add every item if there aren't enough locations to fill.
    """

    display_name = "Unique Units"

class UniqueBuildingItems(Toggle):
    """
    Adds the ability to build unique buildings to the item pool.
    May not add every item if there aren't enough locations to fill.
    Warning: Can cause in-game lag on entering city screens and breaks with non-AP World Civilizations.
    """

    display_name = "Unique Buildings"

class PeekableLocations(Choice):
    """
    Lets you see what items are on various locations.
    Great People lets you see what's on a GP "bulb" like you would a technology.
    All also adds peeks to wonders and techs (currently not implemented).
    """
    display_name = "Peekable Locations"
    option_none = 0
    option_great_people = 1
    option_all = 2

@dataclass
class Civ4Options(PerGameCommonOptions):
    techsanity: Techsanity
    techsanity_era_gates: TechsanityEraGates
    gpsanity: GPsanity
    world_wondersanity: WorldWondersanity
    national_wondersanity: NationalWondersanity
    resourcesanity: Resourcesanity
    unique_units: UniqueUnitItems
    unique_buildings: UniqueBuildingItems
    peekable_locations: PeekableLocations

option_groups = [
    OptionGroup(
        "Techsanity Options",
        [Techsanity, TechsanityEraGates]
    ),
    OptionGroup(
        "Wondersanity Options",
        [WorldWondersanity, NationalWondersanity],
    ),
]

