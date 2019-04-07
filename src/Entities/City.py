from src.Entities.Entities import Entity
from src.Utils import *

import math

class City(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.id = self
        self.race = ''
        self.status = ''
        self.population = 0
        self.patron_god = ''
        self.patron_god_attributes = ''
        self.birth_rate = 0
        self.death_rate = 0
        self.food = 0
        self.work = set()
        self.wealth = 0


    def build_work(self, adults):
        self.work = list()

        # Feed the population
        fc = food_cost(self.population)
        fed_people = self.food / HUMANOID_CONSUMES
        unfed_people = self.population - fed_people
        needed_food_workers = max(math.ceil(unfed_people) , 0)

        obj = {
            "farm": needed_food_workers
        }

        available_workers = len(adults) - needed_food_workers
        if available_workers > 0:
            obj["industry"] = available_workers

        self.work = obj


    def actions(self, state):
        population = [h for h in state.humanoids if h.home == self]
        adults = [a for a in population if a.adult]
        self.population = len(population)
        if self.population <= 0:
            print("The city of {} has fallen to ruin!".format(self.name))
            return

        self.build_work(adults)

        print("Year {} month {} | City {} - FOOD {} | POPULATION {} adults: {} | WEALTH {} | WORK {}".format(state.date.year, state.date.month,  self.name, self.food, self.population, len(adults), self.wealth, self.work))