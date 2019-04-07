
import pygame
import math
import random
from src.Utils import *

class SimuulationRrenderer:


    def __init__(self):
        self.win = pygame.display.set_mode((1000, 1000))

    def __del__(self):
        pygame.quit()

    def setup(self, state):
        pygame.display.set_caption("Territories")

    def update(self, state):
        pygame.time.delay(100)
        pygame.event.get()
        win_w, win_h = pygame.display.get_surface().get_size()
        height = math.floor(win_h / state.world_gen.map_height)
        width = math.floor(win_w / state.world_gen.map_width)
        for y in range(state.world_gen.map_width):
            off_y = y * height
            for x in range(state.world_gen.map_width):
                off_x = x * width
                colour = self.get_territory_colour(state, x, y)
                pygame.draw.rect(self.win, colour, ( off_x, off_y, width, height ))

                city = [c for c in state.cities if c.location == (x, y)]
                if city is not None and len(city) > 0:
                    for c in city:
                        city_colour = self.get_city_colour(state, c)
                        pygame.draw.circle(self.win, city_colour, ((off_x + math.floor(width/2)), (off_y + math.floor(height/2))), math.floor(width / 2) )
                        if not c.ruin:
                            race_colour = self.get_race_colour(c.race)
                            pygame.draw.circle(self.win, race_colour, ((off_x + math.floor(width/2)), (off_y + math.floor(height/2))), math.floor(width / 4) )

        pygame.display.update()

    def get_race_colour(self, race):
        colour_map = {
            "human": (153, 204, 255),
            "dwarf": (255, 153, 51),
            "elf": (255, 0, 255),
            "orc": (153, 102, 51)
        }
        return colour_map[race]

    def get_city_colour(self, state, city):
        if city.ruin:
            return (128,128,128)

        if city.population <= 0 or len(state.humanoids) <= 0:
            return (0, 0, 0)

        if city.population * HUMANOID_CONSUMES < city.food:
            return (255, 0, 0)

        if city.population * HUMANOID_CONSUMES * 4 > city.food:
            return (0, 255, 0)

        return (255, 255, 0)

        # pop_mod = min(city.population / len(state.humanoids), 1.0)
        # saturation = math.floor(pop_mod * 255)
        # #saturation = random.randint(0, 255)
        # #print(saturation)
        # return (saturation, saturation, saturation)

    def get_territory_colour(self, state, x, y):
        colour_map = {
            "wilderness": (67, 181, 41),
            "forest": (49, 109, 59),
            "crops": (188, 206, 53),
            "sea": (10, 126, 214)
        }
        return colour_map[state.world_gen.map[y * state.world_gen.map_width + x].type]