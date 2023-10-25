from .level import Level
from geometry.vector import Vector
from geometry.rectangle import Rectangle

from json import load


def load_levels(levels_file_path, levels_order_file_path):
    # Get a list of levels in the form of dictionaries
    with open(levels_file_path, "r", encoding="utf-8") as f:
        level_dicts = load(f)

    # Create a list of level objects from the list of level dictionaries
    levels = []
    for level_dict in level_dicts:
        # Create all the rectangle and vectors
        start_pos = Vector(level_dict["start_pos"]["x"], level_dict["start_pos"]["y"])
        target = Rectangle(
            level_dict["target"]["x"],
            level_dict["target"]["y"],
            level_dict["target"]["hw"],
            level_dict["target"]["hh"],
        )
        bounds = Rectangle(
            level_dict["bounds"]["x"],
            level_dict["bounds"]["y"],
            level_dict["bounds"]["hw"],
            level_dict["bounds"]["hh"],
        )
        # Create the platforms (a list of rectangles)
        platforms = []
        for platform_dict in level_dict["platforms"]:
            platform = Rectangle(
                platform_dict["x"],
                platform_dict["y"],
                platform_dict["hw"],
                platform_dict["hh"],
            )
            platforms.append(platform)
        # Create the kill boxes (a list of rectangles)
        kill_boxes = []
        for platform_dict in level_dict["kill_boxes"]:
            kill_box = Rectangle(
                platform_dict["x"],
                platform_dict["y"],
                platform_dict["hw"],
                platform_dict["hh"],
            )
            kill_boxes.append(kill_box)
        # Create and add each level to the list
        level = Level(
            level_dict["level_id"],
            start_pos,
            target,
            bounds,
            platforms,
            kill_boxes
        )
        levels.append(level)

    with open(levels_order_file_path, "r", encoding="utf-8") as f:
        levels_order = load(f)

    ordered_levels = []
    for level_id in levels_order:
        for level in levels:
            if level.level_id == level_id:
                ordered_levels.append(level)
                break

    return ordered_levels