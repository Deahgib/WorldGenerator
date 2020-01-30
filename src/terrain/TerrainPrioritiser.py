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

octaves = 1
freq = 16.0 * octaves

x_offset = random.randint(0, 10000)
y_offset = random.randint(0, 10000)

def get_terrain_type(val):
    if val < terrain_thresholds["sea"]:
        return "sea"
    elif val < terrain_thresholds["beach"]:
        return "sand"
    elif val < terrain_thresholds["grassland"]:
        return "wilderness"
    elif val < terrain_thresholds["forest"]:
        return "forest"
    else:
        return "mountain"


def generate_tile(x, y):
    tile = get_terrain_type_snoise(x, y)

    tile2 = get_terrain_type_snoise(x_offset+x, y_offset+y)

    if tile != "sea":
        if tile2 != "sea" and tile2 != "sand":
            tile = "mountain"

    return tile

def get_terrain_type_snoise(x, y):
    val = snoise2((x_offset+x) / freq, (y_offset+y) / freq, octaves)
    return get_terrain_type(val)

def get_terrain_type_pnoise(x, y):
    val = pnoise2((x_offset+x) / freq, (y_offset+y) / freq, octaves)
    return get_terrain_type(val)