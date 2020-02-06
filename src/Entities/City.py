from src.Entities.Entities import Group
from src.Utils import *
from src.EncounterEvaluator import EncounterEvaluator

import logging
import math
import random
from randomwordgenerator import randomwordgenerator as rword

class City(Group):
    def __init__(self):
        Group.__init__(self)
        self.id = self
        self.race = ''
        self.status = ''
        self.population = 0
        self.patron_god = ''
        self.is_blessed = False
        self.patron_god_attributes = ''
        self.birth_rate = 0
        self.death_rate = 0
        self.food = 0
        self.work = set()
        self.wealth = 0
        self.ruin = False
        self.millitary = []
        self.buildings = {}

    def build_work(self, adults):
        self.work = list()

        # Feed the population
        fc = food_cost(self.population)
        fed_people = math.floor(self.food / HUMANOID_CONSUMES)
        unfed_people = max(self.population - fed_people, 0)
        needed_food_workers = math.ceil(self.population / HUMANOID_CONSUMES * 1.5)
        available_workers = max(len(adults) - needed_food_workers, 0)

        obj = {
            "farm": needed_food_workers,
            "industry": 0,
            "millitary": 0
        }

        if available_workers > 0:
            if self.wealth > math.floor(available_workers / 2):
                obj["millitary"] = math.floor(available_workers / 2)
                obj["industry"] = available_workers - obj["millitary"]
            elif self.wealth > math.floor(available_workers / 4):
                obj["millitary"] = math.floor(available_workers / 4)
                obj["industry"] = available_workers - obj["millitary"]
            else:
                obj["industry"] = available_workers

        self.wealth -= obj["millitary"]
        self.work = obj


    def fall_to_ruin(self, state):
        self.ruin = True
        if ENABLE_LOG:
            log_event(state.date, "The city of {} has fallen to ruin!".format(self.name))

        if ENABLE_CONSOLE:
            print("The city of {} has fallen to ruin!".format(self.name))

    def assign_millitary(self, adults):
        self.millitary = []
        if self.work["millitary"] < len(adults):
            for i in range(self.work["millitary"]):
                self.millitary.append(adults[i])



    def go_to_war(self, state):
        enemies = [enemy for enemy in state.cities if enemy.race != self.race]
        chosen_enemy, dist = get_closest(self, enemies)

        cost_of_war = math.ceil(dist*len(self.millitary))
        if self.wealth >= cost_of_war:
            self.wealth -= cost_of_war
            encounter = EncounterEvaluator(state, self, chosen_enemy)
            state.add_battle(encounter)

    def generate_settler_migrants(self, state,  adults):
        dice = Dice()
        number_of_settlers = dice.d20() + dice.d20() + 5
        if len(adults) > number_of_settlers:
            settlers = random.choices(adults, k=number_of_settlers)
            city = self.found_new_city(state, settlers)
            if city != None:
                state.cities.add(city)
                city.population = len(settlers)
                if ENABLE_LOG:
                    log_event(state.date, "The city of {} has been founded by {} settlers from {}!".format(city.name, number_of_settlers, self.name))

                if ENABLE_CONSOLE:
                    print("The city of {} has been founded by {} settlers from {}!".format(city.name, number_of_settlers, self.name))

    def found_new_city(self, state, settlers):
        # Do city stuff
        city = City()
        city.food = food_cost(len(settlers)) * 2
        city.wealth = city.population
        city.race = self.race
        city.name = names.get_city_name(city.race)
        god = self.patron_god
        god.worshiped_by.add(city.race)
        city.patron_god = god
        city.patron_god_attributes = god.divine_attributes

        city_locations = [city.location for city in state.cities if not city.ruin]
        possible_locations = [tile for tile in state.world_gen.map if tile.type != "sea" and get_distance(tile, self) <= 5 and tile.location not in city_locations]
        if city.race == "dwarf":
            possible_locations = [tile for tile in possible_locations if tile.type == "mountain"]
        elif city.race == "elf":
            possible_locations = [tile for tile in possible_locations if tile.type == "forest"]
        elif city.race == "human" or city.race == "orc":
            possible_locations = [tile for tile in possible_locations if tile.type == "forest" or tile.type == "sand" or tile.type == "wilderness"]
        if len(possible_locations) > 0:
            city.location = random.choice(possible_locations).location

            for s in settlers:
                s.home = city
                s.location = city.location

            return city

        return None

    def actions(self, state):
        if not self.ruin:
            population = [h for h in state.humanoids if h.home == self]
            adults = [a for a in population if a.adult]
            visiting_gods = [g for g in state.gods if g.location == self.location]
            self.population = len(population)
            if self.population <= 0:
                self.fall_to_ruin(state)
                return



            if len(visiting_gods)>0 and not self.is_blessed:
                blessing = False
                for g in visiting_gods:
                    if g.seek_blessing(self):
                        self.is_blessed = True
            elif len(visiting_gods)<=0 and self.is_blessed:
                self.is_blessed = False

            self.build_work(adults)
            self.assign_millitary(adults)

            if not self.is_blessed and self.population > 100 and self.wealth < self.population * 20:
                self.generate_settler_migrants(state, adults)

            if self.wealth > self.food and len(self.millitary) > 0:
                self.go_to_war(state)

            if ENABLE_LOG:
                log_city_status(state.date, "{},{},{},{},{},{!r}".format(self.name, self.population, len(adults), self.food, self.wealth, self.work))

            if ENABLE_CONSOLE:
                print("Year {} month {} | City {} - FOOD {} | POPULATION {} adults: {} | WEALTH {} | WORK {}".format(state.date.year, state.date.month,  self.name, self.food, self.population, len(adults), self.wealth, self.work))