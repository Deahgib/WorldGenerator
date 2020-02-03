import sys
from noise import pnoise2, snoise2
from src.Utils import primitives
import random

terrain_thresholds = {
    "sea": 0.2,
    "beach": 0.3,
    "grassland": 0.5,
    "forest": 0.7,
    "mountain": 1.0
}

# octaves = 8
# freq = 4.0 * octaves

x_offset = random.randint(0, 10000)
y_offset = random.randint(0, 10000)

def get_terrain_type(val):
    if val < terrain_thresholds["sea"]:
        return "sea"
    # elif val < terrain_thresholds["beach"]:
    #     return "sand"
    # elif val < terrain_thresholds["grassland"]:
    #     return "wilderness"
    # elif val < terrain_thresholds["forest"]:
    #     return "forest"
    # else:
    #     return "mountain"


def generate_tile(x, y):
    height_map = get_terrain_type_snoise(x, y, 32, 8)
    mountain_chains_map = get_terrain_type_snoise(x_offset+x, y_offset+y, 8, 1)

    humidity_map = get_terrain_type_snoise(x_offset+x, x_offset-y, 32, 2)
    fertility_map = get_terrain_type_snoise(x_offset-x, x_offset-y, 32, 2)

    if height_map < terrain_thresholds["sea"]:
        return "sea"
    else:
        if mountain_chains_map < 0.1:
            return "mountain"
        elif humidity_map < 0.2:
            return "forest"
        elif fertility_map < 0.4:
            return "wilderness"

    return "sand"

def get_terrain_type_snoise(x, y, freq, octaves):
    val = snoise2((x_offset+x) / freq, (y_offset+y) / freq, octaves)
    return val

def get_terrain_type_pnoise(x, y, freq, octaves):
    val = pnoise2((x_offset+x) / freq, (y_offset+y) / freq, octaves)
    return get_terrain_type(val)