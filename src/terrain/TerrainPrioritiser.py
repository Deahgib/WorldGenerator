import sys
from noise import pnoise2, snoise2
from src.Utils import primitives
import random, math

x_offset = random.randint(-10000, 10000)
y_offset = random.randint(-10000, 10000)

class Terrain:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.height_octaves = math.floor(math.log2(height) * math.log2(height))
        self.height_freq = 3.0 * self.height_octaves

        self.moisture_octaves = math.floor( math.log2(height) * math.log2(height) )
        self.moisture_freq = 5.0 * self.height_octaves

        self.sea_octaves = math.floor( math.log2(height) * math.log2(height) )
        self.sea_freq = 4.0 * self.height_octaves

        self.square_gradient = self.generate_square_gradient(width, height)
        self.height_map = self.normalise_map(self.generate_height_map(width, height))
        self.moisture_map = self.normalise_map(self.generate_moisture_map(width, height))
        self.sea_map = self.generate_sea_map(width, height)
        self.island = self.normalise_map(self.subtract_map(self.height_map, self.square_gradient))
        self.island = self.normalise_map(self.subtract_map(self.island, self.sea_map))


    def generate_square_gradient(self, width, height):
        square_gradient = list()
        halfWidth = width / 2
        halfHeight = height / 2
        for i in range(width):
            square_gradient.append(list())
            for j in range(height):
                x = i
                y = j
                val = 0
                x = width - x if x > halfWidth else x
                y = height - y if y > halfHeight else y
                smaller = x if x < y else y
                val = smaller / halfWidth
                val = 1 - val
                val *= val * val
                square_gradient[i].append(val)

        return square_gradient

    def generate_height_map(self, width, height):
        height_map = list()
        for i in range(width):
            height_map.append(list())
            for j in range(height):
                height_map[i].append((snoise2((x_offset+i) / self.height_freq, (y_offset + j) / self.height_freq, self.height_octaves) + 1) / 2)

        return height_map


    def generate_moisture_map(self, width, height):
        moisture_map = list()
        for i in range(width):
            moisture_map.append(list())
            for j in range(height):
                moisture_map[i].append((snoise2((i - x_offset) / self.moisture_freq, (j - y_offset) / self.moisture_freq, self.moisture_octaves) + 1) / 2)

        return moisture_map

    def generate_sea_map(self, width, height):
        moisture_map = list()
        for i in range(width):
            moisture_map.append(list())
            for j in range(height):
                moisture_map[i].append((snoise2((i + x_offset) / self.sea_freq, (j - y_offset) / self.sea_freq, self.sea_octaves) + 1) / 4)

        return moisture_map


    def subtract_map(self, a, b):
        new_map = list()
        for i in range(self.width):
            new_map.append(list())
            for j in range(self.height):
                new_map[i].append( max(min(a[i][j] - b[i][j], 1), 0) )

        return new_map

    def generate_tile(self, x, y):
        humidity = self.moisture_map[x][y]
        height = self.island[x][y]
        if height < 0.01:
            return "sea"
        elif height > 0.7:
            return "mountain"
        else:
            if humidity < 0.4:
                return "sand"
            elif humidity > 0.5:
                return "forest"
            else:
                return "wilderness"

    def normalise_map(self, map):
        lowest = 1
        highest = 0
        for i in range(self.width):
            for j in range(self.height):
                if map[i][j] < lowest:
                    lowest = map[i][j]
                if map[i][j] > highest:
                    highest = map[i][j]

        factor = 1 / (highest-lowest)
        for i in range(self.width):
            for j in range(self.height):
                val = map[i][j] - lowest
                val *= factor
                map[i][j] = val

        return map


    def invert_map(self, map):
        for i in range(self.width):
            for j in range(self.height):
                map[i][j] = 1 - map[i][j]

        return map

    def create_map_images(self):
        self.build_png("gradient.png", self.square_gradient)
        self.build_png("height_map.png", self.height_map)
        self.build_png("moisture_map.png", self.moisture_map)
        self.build_png("sea_map.png", self.sea_map)
        self.build_png("island.png", self.island)


    def build_png(self, file_name, map):
        f = open(file_name, 'wt')
        f.write('P2\n')
        f.write('{} {}\n'.format(self.width, self.height))
        f.write('255\n')
        for y in range(self.height):
            for x in range(self.width):
                f.write("%s\n" % round(map[x][y] * 255))
        f.close()



# def get_terrain_type(val):
#     if val < terrain_thresholds["sea"]:
#         return "sea"
#     elif val < terrain_thresholds["beach"]:
#         return "sand"
#     elif val < terrain_thresholds["grassland"]:
#         return "wilderness"
#     elif val < terrain_thresholds["forest"]:
#         return "forest"
#     else:
#         return "mountain"


# def generate_tile(x, y):
#     tile = get_terrain_type_snoise(x, y)
#
#     tile2 = get_terrain_type_snoise(x_offset+x, y_offset+y)
#
#     if tile != "sea":
#         if tile2 != "sea" and tile2 != "sand":
#             tile = "mountain"
#
#     return tile

# def get_terrain_type_snoise(x, y):
#     val = snoise2((x_offset+x) / freq, (y_offset+y) / freq, octaves)
#     return get_terrain_type(val)
#
# def get_terrain_type_pnoise(x, y):
#     val = pnoise2((x_offset+x) / freq, (y_offset+y) / freq, octaves)
#     return get_terrain_type(val)