from src.Entities.City import City
from src.Entities.Entities import *
from src.Entities.Humanoid import Humanoid
from src.Utils import *
import random
from src.Dates import *
from names import NameGenerator
from multiprocessing.dummy import Pool as ThreadPool
from src.simulator.State import State

import time

import math

from randomwordgenerator import randomwordgenerator as rword


class WorldGen:
    def __init__(self):
        self.map_height = 1
        self.map_width = 1
        self.map = []

    def gen_territories(self, w, h):
        self.map_height = w
        self.map_width = h
        self.map = []
        for y in range(self.map_height):
            for x in range(self.map_width):
                self.map.append(self.gen_territory())

    def gen_territory(self):
        t = Territory()
        t.type = random.choice(primitives['territories'])
        return t

class Territory():
    def __init__(self):
        self.type = primitives['territories'][0]

class Generator:
    def __init__(self):
        self.dice = Dice()
        self.gods = set()
        self.humanoids = set()
        self.cities = set()
        self.world_gen = WorldGen()
        self.names = NameGenerator(primitives['races']['humanoid'], ['male', 'female'])

    def generate(self, size=(25,25)):
        self.pool = ThreadPool(THREAD_POOLS)

        start = time.time()
        x, y = size
        avg = int(round(math.sqrt(x * y)))
        dampner = random.uniform(0, 1)
        nb_gods = math.ceil(random.randint(int(avg / 2), avg) * dampner)
        self.generate_gods(nb_gods)
        end = time.time()
        print("{} gods | ({} seconds)".format(len(self.gods), end - start))
        attrs = set()
        calendar['months'] = []
        for g in self.gods:
            for a in g.divine_attributes:
                attrs.add(a)
            #calendar['months'].append(g.name)

        for a in attrs:
            calendar['months'].append(a.capitalize())
        print('Calendar months {}'.format(calendar['months']))

        start = time.time()
        self.world_gen.gen_territories(x, y)
        print("{} territories | ({} seconds)".format(len(self.world_gen.map), end - start))

        start = time.time()
        ideal_max = math.ceil((x * y) / 200)

        tot_cities = math.ceil( ideal_max + random.randint(-math.ceil(ideal_max * 0.2), math.ceil(ideal_max * 0.2) ) )
        tot_cities = 1 if tot_cities <= 0 else tot_cities
        self.gen_cities(tot_cities)
        end = time.time()
        print("{} cities | Ideal max cities {} | Mod {} | ({} seconds)".format(len(self.cities), ideal_max, math.ceil(ideal_max * 0.2), end - start))

        start = time.time()
        self.generate_humanoids()
        end = time.time()
        print("{} humanoids | ({} seconds)".format(len(self.humanoids), end - start))
        # print("Map --- ")
        # for y in range(self.world_gen.map_height):
        #     line = ''
        #     for x in range(self.world_gen.map_width):
        #         line = line + self.world_gen.map[self.world_gen.map_width * y + x].type[0]
        #
        #     print (line)
        self.pool.close()
        self.pool.join()

        return State(self.world_gen, self.humanoids, self.cities, self.gods)

    def generate_gods(self, max):
        self.gods = set()
        self.pool.map(lambda x: self.gods.add(self.gen_god()), range(max))

    def generate_humanoids(self):
        self.humanoids = set()
        for city in self.cities:
            self.pool.map(lambda x: self.humanoids.add(self.gen_humanoid(city.race, city)), range(city.population))
            # for i in range(city.population):
            #     self.humanoids.add(self.gen_humanoid(city.race, city.location))

        # for i in range(amount):
        #     self.humanoids.add(self.gen_humanoid())

    def gen_cities(self, max):
        self.cities = set()
        self.pool.map(lambda x: self.cities.add(self.gen_city(max)), range(max))

        # for i in range(max):
        #     self.cities.add(self.gen_city(max))

    def gen_city(self, pop_mod):
        city = City()
        city.population = random.randint(20, 60)
        city.food = food_cost(city.population) * 2
        city.wealth = city.population
        city.location = (random.randint(0,self.world_gen.map_width), random.randint(0,self.world_gen.map_height))
        city.name = rword.generate_random_words(1).capitalize()
        city.race = random.choice(primitives['races']["humanoid"])
        god = random.choice(list(self.gods))
        god.worshiped_by.add(city.race)
        city.patron_god = god
        city.patron_god_attributes = god.divine_attributes
        return city

    def gen_god(self):
        god = God()
        god.location = (random.randint(0,self.world_gen.map_width), random.randint(0,self.world_gen.map_height))
        god.name = self.names.get_last_name(race= 'human')
        god.power = random.randint(21, 100)
        god.divine_attributes = random.sample(primitives['divine_attributes'], random.randint(int(len(primitives['divine_attributes'])/4), int(len(primitives['divine_attributes'])/2)))
        god.goodness = random.uniform(-1, 1)
        return god

    def gen_humanoid(self, race = None, location = None):
        e = Humanoid()
        e.location = (random.randint(0, self.world_gen.map_width), random.randint(0, self.world_gen.map_height)) if location is None else location
        e.home = e.location
        e.home_name = (c.name for c in self.cities)
        e.health = 1
        e.genus = random.choice(primitives['geni'])
        e.race = random.choice(primitives['races'][e.genus]) if race is None else race
        e.age = random.randint(0, primitives['attributes'][e.race]['oldest'])
        e.sex = 'male' if self.dice.d2() == 1 else 'female'
        e.adult = e.age >= primitives['attributes'][e.race]['adult']
        e.month_of_birth = calendar['months'][random.randint(0, len(calendar['months'])-1)]
        e.attr_str, e.attr_agi, e.attr_con, e.attr_int, e.attr_wis, e.attr_cha = self.roll_attributes(primitives['attributes'][e.race]['roll'], primitives['attributes'][e.race]['take'])
        e.fname = self.names.get_first_name(race='human' ,gender=e.sex)
        e.lname = self.names.get_last_name(race= 'human')
        e.name = e.fname + " " + e.lname
        e.favorite_job = random.choice(primitives["jobs"])
        e.favorite_god = random.choice([g for g in self.gods if e.race in g.worshiped_by])
        e.favorite_god_name = e.favorite_god.name
        e.favorite_god_attributes = e.favorite_god.divine_attributes
        e.goodness =  max(min(random.gauss(e.favorite_god.goodness, 0.2), 1.0), -1.0)
        e.lawful = max(min(random.gauss(0.0, 0.5), 1.0), -1.0)
        e.temperament = max(min(random.gauss(0.0, 0.1), 1.0), -1.0)
        e.dna = "{}-{}-{}-{}-{}-{}-{}-{}-{}".format(e.genus, e.race, e.sex, e.attr_str, e.attr_agi, e.attr_con, e.attr_int, e.attr_wis, e.attr_cha)
        return e

    def roll_attributes(self, roll=4, take=3):
        return( sum(nlargest(self.dice.d6(roll), take)), sum(nlargest(self.dice.d6(roll), take)), sum(nlargest(self.dice.d6(roll), take)), sum(nlargest(self.dice.d6(roll), take)), sum(nlargest(self.dice.d6(roll), take)), sum(nlargest(self.dice.d6(roll), take)) )


        obj = {}
        for attribute in primitives['attribute_names']:
            rolls = self.dice.d6(roll)
            largest = sum(nlargest(rolls, take))
            obj[attribute] = sum(largest)

        return obj

