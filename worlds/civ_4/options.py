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
    range_end = 100
    default = 75

class GPsanity(Range):
    """
    Turns great person bulbs into locations in the multiworld.
    This also includes Great Generals and Great Spies
    Change to 0 to fully disable GPsanity
    Warning: Currently not biased towards lower numbers, so be careful with high numbers.
    """

    display_name = "GPsanity"

    range_start = 0
    range_end = 10
    default = 3

@dataclass
class Civ4Options(PerGameCommonOptions):
    techsanity: Techsanity
    techsanity_era_gates: TechsanityEraGates
    gpsanity: GPsanity
