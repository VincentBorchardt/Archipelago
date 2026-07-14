from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

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
    pass

def set_all_location_rules(world: Civ4World) -> None:
    # Location rules work no differently from Entrance rules.
    # Most of our locations are chests that can simply be opened by walking up to them.
    # Thus, their logical requirements are covered by the Entrance rules of the Entrances that were required to
    # reach the region that the chest sits in.
    # However, our two enemies work differently.
    # Entering the room with the enemy is not enough, you also need to have enough combat items to be able to defeat it.
    # So, we need to set requirements on the Locations themselves.
    set_tech_rules(world)

def set_completion_condition(world: Civ4World) -> None:
    # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    # For this, we can use world.set_completion_rule.
    # You can just set a completion condition directly like any other condition, referencing items the player receives:
    world.set_completion_rule(Has("Agriculture"))

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

def set_gp_rules(world: Civ4World) -> None:
    pass