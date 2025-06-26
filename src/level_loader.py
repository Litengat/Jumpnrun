import json
import os
from os.path import join
from block import Block
from fire import Fire
from finish import Finish
from traps.FallingPlatform import FallingPlatform
from traps.Fan import Fan
from traps.Saw import Saw

def load_level(level_name):
    """Load a level from a JSON file and return a list of game objects."""
    path = join("levels", f"{level_name}.json")
    print(path)
    try:
        with open(path, "r") as f:
            level_data = json.load(f)
        
        print(level_data)
        objects = []

        # Load blocks
        if "blocks" in level_data:
            for block_data in level_data["blocks"]:
                type = block_data["type"]
                x = block_data["x"]
                y = block_data["y"]
                size = block_data.get("size", 96)  # Default size is 96
                objects.append(Block(x, y,type))
        if "objects" in level_data: 
            for object in level_data["objects"]:
                type = object["type"]
                x = object["x"]
                y = object["y"]
                if(type == "Fan"):
                    objects.append(Fan(x,y))
                if(type == "Saw"):
                    objects.append(Saw(x,y))
                if(type == "FallingPlatform"):
                    objects.append(FallingPlatform(x,y))
                if(type == "Finish"):
                    objects.append(Finish(x,y))
        return objects
    except FileNotFoundError:
        print(f"Level file '{level_name}.json' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error parsing level file '{level_name}.json'. Invalid JSON format.")
        return []

