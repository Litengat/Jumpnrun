import json
import os
from os.path import join
from block import Block
from fire import Fire

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
                objects.append(Block(x, y, size,type))
        
        # Load fire traps
        if "fires" in level_data:
            for fire_data in level_data["fires"]:
                x = fire_data["x"]
                y = fire_data["y"]
                width = fire_data.get("width", 16)
                height = fire_data.get("height", 32)
                fire = Fire(x, y, width, height)
                fire.on()
                objects.append(fire)
        
        return objects
    except FileNotFoundError:
        print(f"Level file '{level_name}.json' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error parsing level file '{level_name}.json'. Invalid JSON format.")
        return []