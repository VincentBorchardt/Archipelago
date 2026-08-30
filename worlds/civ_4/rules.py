from __future__ import annotations

import math
from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule, HasGroup
from . import constants

if TYPE_CHECKING:
    from .world import Civ4World

def set_all_rules(world: Civ4World) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: Civ4World) -> None:
    # First, we need to actually grab our entrances. Luckily, there is a helper method for this.
    if world.options.gpsanity > 0:
        set_gp_rules(world)

    if world.options.techsanity and world.options.techsanity_era_gates > 0:
        set_techsanity_era_gates(world)

def set_all_location_rules(world: Civ4World) -> None:
    # Location rules work no differently from Entrance rules.
    # Thus, their logical requirements are covered by the Entrance rules of the Entrances that were required to
    # reach the region.
    # So, we need to set requirements on the Locations themselves.
    if world.options.techsanity:
        set_tech_rules(world)

    if world.options.world_wondersanity:
        set_world_wonder_rules(world)

    if world.options.national_wondersanity:
        set_national_wonder_rules(world)

def set_completion_condition(world: Civ4World) -> None:
    # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    # For this, we can use world.set_completion_rule.
    # You can just set a completion condition directly like any other condition, referencing items the player receives:
    world.set_completion_rule(Has("Victory"))

def set_tech_rules(world: Civ4World) -> None:
    world.set_rule(world.get_location("Archipelago Sailing"), Has("Fishing"))
    world.set_rule(world.get_location("Archipelago Pottery"), Has("The Wheel") & (Has("Fishing") | Has("Agriculture")))
    world.set_rule(world.get_location("Archipelago Animal Husbandry"), Has("Agriculture") | Has("Hunting"))
    world.set_rule(world.get_location("Archipelago Archery"), Has("Hunting"))
    world.set_rule(world.get_location("Archipelago Meditation"), Has("Mysticism"))
    world.set_rule(world.get_location("Archipelago Polytheism"), Has("Mysticism"))
    world.set_rule(world.get_location("Archipelago Masonry"), Has("Mysticism") | Has("Mining"))
    world.set_rule(world.get_location("Archipelago Horseback Riding"), Has("Animal Husbandry"))
    world.set_rule(world.get_location("Archipelago Priesthood"), Has("Meditation") | Has("Polytheism"))
    world.set_rule(world.get_location("Archipelago Monotheism"), Has("Masonry") & Has("Polytheism"))
    world.set_rule(world.get_location("Archipelago Bronze Working"), Has("Mining"))
    world.set_rule(world.get_location("Archipelago Writing"), Has("Pottery") | Has("Animal Husbandry") | Has("Priesthood"))
    world.set_rule(world.get_location("Archipelago Metal Casting"), Has("Pottery") & Has("Bronze Working"))
    world.set_rule(world.get_location("Archipelago Iron Working"), Has("Bronze Working"))
    world.set_rule(world.get_location("Archipelago Aesthetics"), Has("Writing"))
    world.set_rule(world.get_location("Archipelago Mathematics"), Has("Writing"))
    world.set_rule(world.get_location("Archipelago Alphabet"), Has("Writing"))
    world.set_rule(world.get_location("Archipelago Monarchy"), Has("Priesthood") | Has("Monotheism"))
    world.set_rule(world.get_location("Archipelago Compass"), Has("Sailing") & Has("Iron Working"))
    world.set_rule(world.get_location("Archipelago Literature"), Has("Sailing") & Has("Polytheism"))
    world.set_rule(world.get_location("Archipelago Calendar"), Has("Sailing") & Has("Mathematics"))
    world.set_rule(world.get_location("Archipelago Construction"), Has("Masonry") & Has("Mathematics"))
    world.set_rule(world.get_location("Archipelago Currency"), Has("Alphabet") | Has("Mathematics"))
    world.set_rule(world.get_location("Archipelago Machinery"), Has("Metal Casting"))
    world.set_rule(world.get_location("Archipelago Drama"), Has("Aesthetics"))
    world.set_rule(world.get_location("Archipelago Engineering"), Has("Construction") & Has("Machinery"))
    world.set_rule(world.get_location("Archipelago Code of Laws"), Has("Writing") & (Has("Priesthood") | Has("Currency")))
    world.set_rule(world.get_location("Archipelago Feudalism"), Has("Writing") & Has("Monarchy"))
    world.set_rule(world.get_location("Archipelago Optics"), Has("Machinery") & Has("Compass"))
    world.set_rule(world.get_location("Archipelago Music"), Has("Mathematics") & (Has("Literature") | Has("Drama")))
    world.set_rule(world.get_location("Archipelago Philosophy"), Has("Meditation") & (Has("Code of Laws") | Has("Drama")))
    world.set_rule(world.get_location("Archipelago Civil Service"), Has("Mathematics") & (Has("Feudalism") | Has("Code of Laws")))
    world.set_rule(world.get_location("Archipelago Theology"), Has("Writing") & Has("Monotheism"))
    world.set_rule(world.get_location("Archipelago Divine Right"), Has("Theology") & Has("Monarchy"))
    world.set_rule(world.get_location("Archipelago Paper"), Has("Theology") | Has("Civil Service"))
    world.set_rule(world.get_location("Archipelago Guilds"), Has("Machinery") & Has("Feudalism"))
    world.set_rule(world.get_location("Archipelago Nationalism"), Has("Civil Service") & (Has("Philosophy") | Has("Divine Right")))
    world.set_rule(world.get_location("Archipelago Printing Press"), Has("Alphabet") & Has("Machinery") & Has("Paper"))
    world.set_rule(world.get_location("Archipelago Education"), Has("Paper"))
    world.set_rule(world.get_location("Archipelago Banking"), Has("Currency") & Has("Guilds"))
    world.set_rule(world.get_location("Archipelago Constitution"), Has("Code of Laws") & Has("Nationalism"))
    world.set_rule(world.get_location("Archipelago Military Tradition"), Has("Nationalism") & Has("Music"))
    world.set_rule(world.get_location("Archipelago Replaceable Parts"), Has("Banking") & Has("Printing Press"))
    world.set_rule(world.get_location("Archipelago Liberalism"), Has("Philosophy") & Has("Education"))
    world.set_rule(world.get_location("Archipelago Economics"), Has("Banking") & Has("Education"))
    world.set_rule(world.get_location("Archipelago Gunpowder"), Has("Education") | Has("Guilds"))
    world.set_rule(world.get_location("Archipelago Democracy"), Has("Printing Press") & Has("Constitution"))
    world.set_rule(world.get_location("Archipelago Rifling"), Has("Replaceable Parts") & Has("Gunpowder"))
    world.set_rule(world.get_location("Archipelago Astronomy"), Has("Optics") & Has("Calendar"))
    world.set_rule(world.get_location("Archipelago Corporation"), Has("Constitution") & Has("Economics"))
    world.set_rule(world.get_location("Archipelago Chemistry"), Has("Engineering") & Has("Gunpowder"))
    world.set_rule(world.get_location("Archipelago Steam Power"), Has("Chemistry") & Has("Replaceable Parts"))
    world.set_rule(world.get_location("Archipelago Scientific Method"), Has("Printing Press") & (Has("Astronomy") | Has("Chemistry")))
    world.set_rule(world.get_location("Archipelago Military Science"), Has("Chemistry"))
    world.set_rule(world.get_location("Archipelago Steel"), Has("Iron Working") & Has("Chemistry"))
    world.set_rule(world.get_location("Archipelago Assembly Line"), Has("Corporation") & Has("Steam Power"))
    world.set_rule(world.get_location("Archipelago Communism"), Has("Liberalism") & Has("Scientific Method"))
    world.set_rule(world.get_location("Archipelago Physics"), Has("Astronomy") & Has("Scientific Method"))
    world.set_rule(world.get_location("Archipelago Biology"), Has("Chemistry") & Has("Scientific Method"))
    world.set_rule(world.get_location("Archipelago Railroad"), Has("Steam Power") & Has("Steel"))
    world.set_rule(world.get_location("Archipelago Flight"), Has("Combustion") & Has("Physics"))
    world.set_rule(world.get_location("Archipelago Artillery"), Has("Steel") & Has("Physics") & Has("Rifling"))
    world.set_rule(world.get_location("Archipelago Fascism"), Has("Nationalism") & Has("Assembly Line"))
    world.set_rule(world.get_location("Archipelago Electricity"), Has("Physics"))
    world.set_rule(world.get_location("Archipelago Medicine"), Has("Optics") & Has("Biology"))
    world.set_rule(world.get_location("Archipelago Combustion"), Has("Railroad"))
    world.set_rule(world.get_location("Archipelago Rocketry"), Has("Rifling") & (Has("Flight") | Has("Artillery")))
    world.set_rule(world.get_location("Archipelago Industrialism"), Has("Electricity") & Has("Assembly Line"))
    world.set_rule(world.get_location("Archipelago Fission"), Has("Electricity"))
    world.set_rule(world.get_location("Archipelago Radio"), Has("Electricity"))
    world.set_rule(world.get_location("Archipelago Refrigeration"), Has("Electricity") & Has("Biology"))
    world.set_rule(world.get_location("Archipelago Satellites"), Has("Radio") & Has("Rocketry"))
    world.set_rule(world.get_location("Archipelago Plastics"), Has("Combustion") & Has("Industrialism"))
    world.set_rule(world.get_location("Archipelago Mass Media"), Has("Radio"))
    world.set_rule(world.get_location("Archipelago Computers"), Has("Plastics") & Has("Radio"))
    world.set_rule(world.get_location("Archipelago Advanced Flight"), Has("Satellites") & Has("Flight"))
    world.set_rule(world.get_location("Archipelago Laser"), Has("Satellites") & Has("Plastics"))
    world.set_rule(world.get_location("Archipelago Composites"), Has("Satellites") & Has("Plastics"))
    world.set_rule(world.get_location("Archipelago Ecology"), Has("Biology") & (Has("Fission") | Has("Plastics")))
    world.set_rule(world.get_location("Archipelago Superconductors"), Has("Computers") | Has("Refrigeration"))
    world.set_rule(world.get_location("Archipelago Stealth"), Has("Composites") & Has("Advanced Flight"))
    world.set_rule(world.get_location("Archipelago Fiber Optics"), Has("Laser") | Has("Computers"))
    world.set_rule(world.get_location("Archipelago Robotics"), Has("Computers"))
    world.set_rule(world.get_location("Archipelago Genetics"), Has("Medicine") & Has("Superconductors"))
    world.set_rule(world.get_location("Archipelago Fusion"), Has("Fission") & Has("Fiber Optics"))
    world.set_rule(world.get_location("Archipelago Future Tech"), Has("Stealth") & Has("Genetics"))

def set_world_wonder_rules(world:Civ4World) -> None:
    world.set_rule(world.get_location("Angkor Wat"), Has("Philosophy"))
    world.set_rule(world.get_location("Broadway"), Has("Electricity"))
    world.set_rule(world.get_location("Chichen Itza"), Has("Code of Laws"))
    world.set_rule(world.get_location("Cristo Redentor"), Has("Radio"))
    world.set_rule(world.get_location("Hollywood"), Has("Mass Media"))
    world.set_rule(world.get_location("Mausoleum of Maussollos"), Has("Calendar"))
    world.set_rule(world.get_location("Notre Dame"), Has("Engineering"))
    world.set_rule(world.get_location("Rock 'n' Roll"), Has("Radio"))
    world.set_rule(world.get_location("Shwedagon Paya"), Has("Meditation") & Has("Aesthetics"))
    world.set_rule(world.get_location("Stonehenge"), Has("Mysticism"))
    world.set_rule(world.get_location("The Apostolic Palace"), Has("Theology")) # Requires Diplo Victory
    world.set_rule(world.get_location("The Colossus"), Has("Metal Casting"))
    world.set_rule(world.get_location("The Eiffel Tower"), Has("Metal Casting") & Has("Radio"))
    world.set_rule(world.get_location("The Great Library"), Has("Writing") & Has("Literature"))
    world.set_rule(world.get_location("The Great Lighthouse"), Has("Sailing") & Has("Masonry"))
    world.set_rule(world.get_location("The Great Wall"), Has("Masonry"))
    world.set_rule(world.get_location("The Hagia Sophia"), Has("Theology"))
    world.set_rule(world.get_location("The Hanging Gardens"), Has("Mathematics") & Has("Masonry"))
    world.set_rule(world.get_location("The Kremlin"), Has("Communism"))
    world.set_rule(world.get_location("The Oracle"), Has("Priesthood"))
    world.set_rule(world.get_location("The Parthenon"), Has("Polytheism") & Has("Aesthetics"))
    world.set_rule(world.get_location("The Pentagon"), Has("Assembly Line"))
    world.set_rule(world.get_location("The Pyramids"), Has("Masonry"))
    world.set_rule(world.get_location("The Sistine Chapel"), Has("Music"))
    world.set_rule(world.get_location("The Space Elevator"), Has("Satellites") & Has("Robotics"))
    world.set_rule(world.get_location("The Spiral Minaret"), Has("Divine Right"))
    world.set_rule(world.get_location("The Statue of Liberty"), Has("Democracy") & Has("Metal Casting"))
    world.set_rule(world.get_location("The Statue of Zeus"), Has("Aesthetics") & Has("Mysticism"))
    world.set_rule(world.get_location("The Taj Mahal"), Has("Nationalism"))
    world.set_rule(world.get_location("The Temple of Artemis"), Has("Polytheism"))
    world.set_rule(world.get_location("The Three Gorges Dam"), Has("Plastics"))
    world.set_rule(world.get_location("The United Nations"), Has("Mass Media")) # Requires Diplo Victory
    world.set_rule(world.get_location("University of Sankore"), Has("Paper"))
    world.set_rule(world.get_location("Versailles"), Has("Divine Right"))

def set_national_wonder_rules(world: Civ4World) -> None:
    world.set_rule(world.get_location("Forbidden Palace"), Has("Code of Laws"))
    world.set_rule(world.get_location("Globe Theatre"), Has("Drama"))
    world.set_rule(world.get_location("Hermitage"), Has("Nationalism"))
    world.set_rule(world.get_location("Heroic Epic"), Has("Literature"))
    world.set_rule(world.get_location("Ironworks"), Has("Metal Casting") & Has("Steel"))
    world.set_rule(world.get_location("Moai Statues"), Has("Sailing"))
    world.set_rule(world.get_location("Mt. Rushmore"), Has("Fascism"))
    world.set_rule(world.get_location("National Epic"), Has("Writing") & Has("Literature"))
    world.set_rule(world.get_location("National Park"), Has("Biology"))
    world.set_rule(world.get_location("Oxford University"), Has("Writing") & Has("Education"))
    world.set_rule(world.get_location("Red Cross"), Has("Medicine"))
    world.set_rule(world.get_location("Wall Street"), Has("Banking") & Has("Corporation"))
    world.set_rule(world.get_location("West Point"), Has("Military Tradition"))

def set_gp_rules(world: Civ4World) -> None:
    # TODO figure out how to limit this further, probably with more regions
    scientist_access = world.get_entrance("Can Produce Great Scientist")
    artist_access = world.get_entrance("Can Produce Great Artist")
    spy_access = world.get_entrance("Can Produce Great Spy")
    general_access = world.get_entrance("Can Produce Great General")
    prophet_access = world.get_entrance("Can Produce Great Prophet")
    engineer_access = world.get_entrance("Can Produce Great Engineer")
    merchant_access = world.get_entrance("Can Produce Great Merchant")
    world.set_rule(scientist_access, Has("Writing"))
    world.set_rule(artist_access, Has("Drama"))
    world.set_rule(spy_access, Has("Code of Laws"))
    world.set_rule(general_access, Has("Rifling"))
    world.set_rule(prophet_access, Has("Priesthood"))
    world.set_rule(engineer_access, Has("Metal Casting"))
    world.set_rule(merchant_access, Has("Currency"))

def set_techsanity_era_gates(world):
    classical_access = world.get_entrance("Ancient to Classical")
    medieval_access = world.get_entrance("Classical to Medieval")
    renaissance_access = world.get_entrance("Medieval to Renaissance")
    industrial_access = world.get_entrance("Renaissance to Industrial")
    modern_access = world.get_entrance("Industrial to Modern")
    future_access = world.get_entrance("Modern to Future")
    required_percentage = world.options.techsanity_era_gates / 100.0
    required_ancient = math.ceil(len(constants.ANCIENT_TECHS) * required_percentage)
    world.set_rule(classical_access, HasGroup("Ancient Techs", required_ancient))
    required_classical = math.ceil(len(constants.CLASSICAL_TECHS) * required_percentage)
    world.set_rule(medieval_access, HasGroup("Classical Techs", required_classical))
    required_medieval = math.ceil(len(constants.MEDIEVAL_TECHS) * required_percentage)
    world.set_rule(renaissance_access, HasGroup("Medieval Techs", required_medieval))
    required_renaissance = math.ceil(len(constants.RENAISSANCE_TECHS) * required_percentage)
    world.set_rule(industrial_access, HasGroup("Renaissance Techs", required_renaissance))
    required_industrial = math.ceil(len(constants.INDUSTRIAL_TECHS) * required_percentage)
    world.set_rule(modern_access, HasGroup("Industrial Techs", required_industrial))
    required_modern = math.ceil(len(constants.MODERN_TECHS) * required_percentage)
    world.set_rule(future_access, HasGroup("Modern Techs", required_modern))