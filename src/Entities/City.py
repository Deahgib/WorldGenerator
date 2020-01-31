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
        fed_people = self.food / HUMANOID_CONSUMES
        unfed_people = self.population - fed_people
        needed_food_workers = max(math.ceil(unfed_people) , 0)

        obj = {
            "farm": needed_food_workers,
            "industry": 0,
            "millitary": 0
        }

        available_workers = len(adults) - needed_food_workers
        if available_workers > 0:
            if self.wealth > math.floor(available_workers / 2):
                obj["millitary"] = math.floor(available_workers / 2)
                obj["industry"] = available_workers - obj["millitary"]
            elif self.wealth > math.floor(available_workers / 4):
                obj["millitary"] = math.floor(available_workers / 4)
                obj["industry"] = available_workers - obj["millitary"]
            else:
                obj["industry"] = available_workers

        self.work = obj


    def fall_to_ruin(self, state):
        self.ruin = True
        #if ENABLE_LOG:
        log_event(state.date, "The city of {} has fallen to ruin!".format(self.name))
        #print("The city of {} has fallen to ruin!".format(self.name))

    def assign_millitary(self, adults):
        self.millitary = []
        if self.work["millitary"] < len(adults):
            for i in range(self.work["millitary"]):
                self.millitary.append(adults[i])



    def go_to_war(self, state):
        enemies = [enemy for enemy in state.cities if enemy.race != self.race]
        chosen_enemy, dist = get_closest(self, enemies)

        cost_of_war = math.floor(dist*50)
        if self.wealth > cost_of_war and self.wealth < chosen_enemy.wealth:
            self.wealth -= cost_of_war
            encounter = EncounterEvaluator(state, self, chosen_enemy)
            state.add_battle(encounter)

    def generate_settler_migrants(self, adults):
        dice - Dice()
        number_of_settlers = dice.d20() + dice.d20() + 5


    def found_new_city(self):
        # Do city stuff
        city = City()
        city.population = random.randint(10, 50)
        city.food = food_cost(city.population) * 2
        city.wealth = city.population
        city.name = rword.generate_random_words(1).capitalize()
        city.race = random.choice(primitives['races']["humanoid"])
        god = random.choice(list(self.gods))
        god.worshiped_by.add(city.race)
        city.patron_god = god
        city.patron_god_attributes = god.divine_attributes

        possible_locations = [tile for tile in self.world_gen.map if tile.type != "sea"]
        city.location = random.choice(possible_locations).location

    def actions(self, state):
        if not self.ruin:
            population = [h for h in state.humanoids if h.home == self]
            adults = [a for a in population if a.adult]
            self.population = len(population)
            if self.population <= 0:
                self.fall_to_ruin(state)
                return

            self.is_blessed = self.patron_god.seek_blessing(self)

            self.build_work(adults)
            self.assign_millitary(adults)

            if not self.is_blessed and self.population > 100 and self.wealth < self.food:
                self.generate_settler_migrants(adults)

            if self.wealth > self.food and len(self.millitary) > 0:
                self.go_to_war(state)

            if ENABLE_LOG:
                log_city_status(state.date, "{},{},{},{},{},{!r}".format(self.name, self.population, len(adults), self.food, self.wealth, self.work))

            if ENABLE_CONSOLE:
                print("Year {} month {} | City {} - FOOD {} | POPULATION {} adults: {} | WEALTH {} | WORK {}".format(state.date.year, state.date.month,  self.name, self.food, self.population, len(adults), self.wealth, self.work))