from src.Entities.Entities import Group
from src.Utils import *
from src.EncounterEvaluator import EncounterEvaluator

import logging
import math

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
        self.buildings = {}




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


    def fall_to_ruin(self, state):
        self.ruin = True
        #if ENABLE_LOG:
        log_event(state.date, "The city of {} has fallen to ruin!".format(self.name))
        #print("The city of {} has fallen to ruin!".format(self.name))

    def go_to_war(self, state, adults):
        enemies = [enemy for enemy in state.cities if enemy.race != self.race]
        chosen_enemy = None
        dist = 999999
        for e in enemies:
            e_x, e_y = e.location
            s_x, s_y = self.location
            chk_dist = math.sqrt(math.pow(e_x - s_x, 2) + math.pow(e_y - s_y,2))
            if chk_dist < dist:
                chosen_enemy = e
                dist = chk_dist


        cost_of_war = math.floor(dist*50)
        if self.wealth > cost_of_war and self.wealth < chosen_enemy.wealth:
            self.wealth -= cost_of_war

            e_population = [h for h in state.humanoids if h.home == chosen_enemy]
            e_adults = [a for a in e_population if a.adult]
            encounter = EncounterEvaluator(state, self, chosen_enemy, adults, e_adults)
            state.add_battle(encounter)

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

            if self.food > len(adults) * 2 and self.wealth > self.food:
                self.go_to_war(state, adults)

            if ENABLE_LOG:
                log_city_status(state.date, "{},{},{},{},{},{!r}".format(self.name, self.population, len(adults), self.food, self.wealth, self.work))

            if ENABLE_CONSOLE:
                print("Year {} month {} | City {} - FOOD {} | POPULATION {} adults: {} | WEALTH {} | WORK {}".format(state.date.year, state.date.month,  self.name, self.food, self.population, len(adults), self.wealth, self.work))