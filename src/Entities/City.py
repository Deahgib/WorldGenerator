from src.Entities.Entities import Entity
from src.Utils import *

class City(Entity):
    def __init__(self):
        Entity.__init__(self)
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


    def actions(self, state):
        population = [h for h in state.humanoids if h.home == self]
        self.population = len(population)
        if self.population <= 0:
            print("The city of {} has fallen to ruin!".format(self.name))
            return

        #adults = [a for a in population if a.adult]
        #births = [b for b in self.births if b.home == city.location]
        #deaths = [d for d in self.deaths if d.home == city.location]
        #city.birth_rate = 0 if len(adults) <= 0 else round(len(births) / len(adults) * 1000, 2)
        #city.death_rate = 0 if len(adults) <= 0 else round(len(deaths) / len(adults) * 1000, 2)
        self.work = set()

        fc = food_cost(self.population)
        if self.food - 2*fc < 0:
            self.work.add("farm")
        else:
            self.work.add("farm")
            self.work.add("industry")

        #print(fc)
        #print(city.work)
        print("-- City FOOD {} POPULATION {} WEALTH {} WORK {!r}".format(self.food, self.population, self.wealth, self.work))