
from src.Entities.City import City
from src.Entities.Humanoid import Humanoid
from src.RandomRoll import Dice
import random
import math
from src.Utils import *
from src.Entities.Entities import Imortal

class God(Imortal):
    def __init__(self):
        Imortal.__init__(self)
        self.id = self
        self.divine_attributes = set()
        self.worshiped_by = set()
        self.wealth = 0

        self.find_destination = False
        self.destination = None

    def seek_blessing(self, entity):
        if isinstance(entity, City):
            dice = Dice()
            if dice.d100() > 85:
                return True

        if isinstance(entity, Humanoid):
            dice = Dice()
            if dice.d20() > entity.attr_wis:
                return True

        return False

    def cast_judgement(self, state):
        if isinstance(self.destination, City):
            race_humanoids = [h for h in state.humanoids if h.race == self.destination.race]
            citizens = [c for c in race_humanoids if c.home == self.destination]
            if len(race_humanoids) > (len(list(state.humanoids))/20)*11: # Too powerfull purge them

                self.wealth += self.destination.wealth
                self.destination.wealth = 0
                number_to_purge = math.floor(len(citizens)/2)
                i = 0
                for c in citizens:
                    if i < number_to_purge:
                        c.health = 0
                        state.kill_humanoid(c)
                        i+=1
                    c.temperament = max(c.temperament - 0.5, -1.0)

                if ENABLE_LOG:
                    log_event(state.date, "The god {} SMITES the city of {} killing {} citizens.".format(self.name, self.destination.name, number_to_purge))

            elif len(race_humanoids) < len(list(state.humanoids))/8: # Too weak help them
                citizens = [c for c in race_humanoids if c.home == self.destination]
                self.destination.wealth += self.wealth
                self.wealth = 0
                for c in citizens:
                    c.health = c.max_health
                    c.temperament = min(c.temperament + 0.5, 1.0)

                if ENABLE_LOG:
                    log_event(state.date, "The god {} SAVES the city of {} helping {} citizens.".format(self.name, self.destination.name, len(citizens)))

            else:
                log_event(state.date,
                          "The god {} blesses the city of {} with their presence.".format(self.name, self.destination.name))


    def actions(self, state):
        if self.find_destination:
            if self.destination != None:
                dx = 0
                if self.location[0] < self.destination.location[0]:
                    dx = 1
                elif self.location[0] > self.destination.location[0]:
                    dx = -1

                dy = 0
                if self.location[1] < self.destination.location[1]:
                    dy = 1
                elif self.location[1] > self.destination.location[1]:
                    dy = -1

                self.location = (self.location[0] + dx, self.location[1] + dy)
                if dx == 0 and dy == 0:
                    self.find_destination = False
                    self.cast_judgement(state)

        else:
            dice = Dice()
            if dice.d100() == 100:
                if dice.d2() == 1:
                    # Choose new destination
                    if len(self.worshiped_by) > 0:
                        race = random.choice(list(self.worshiped_by))
                        options = [c for c in state.cities if c.race == race and not c.ruin]
                        if len(options) > 0:
                            city = random.choice(options)
                            self.destination = city
                            self.find_destination = True
                else:
                    self.destination = random.choice(state.world_gen.map)
                    self.find_destination = True
