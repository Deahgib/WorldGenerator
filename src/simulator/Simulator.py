from src.Dates import *
from src.Entities.Humanoid import Humanoid
from src.Utils import *
import random
from multiprocessing.dummy import Pool as ThreadPool
import gc

class Simulator:
    def __init__(self, state):
        self.state = state

        #self.map = list(map)
        # self.humanoids = set(humanoids)
        # self.cities = set(cities)
        # self.gods = set(gods)
        #self.dice = Dice()
        #self.names = NameGenerator(primitives['races']['humanoid'], ["male", "female"])
        #self.births = set()
        #self.yearly_births = set()
        #self.deaths = set()
        #self.yearly_deaths = set()
        #self.yearly_population = 0

         #number_of_threads(1)
        self.birth_rate = 0
        self.death_rate = 0
        self.pool = ThreadPool(THREAD_POOLS)

    def age(self, simulation_years):
        self.yearly_population = 0
        for y in range(simulation_years):
            self.yearly_births = set()
            self.yearly_deaths = set()
            for m in calendar['months']:
                self.simulate_month()
                #self.yearly_population += len(self.humanoids)
                #self.yearly_births = self.yearly_births | self.births
                #self.yearly_deaths = self.yearly_deaths | self.deaths
                #build_table(self.date.month, self.date.year, self.humanoids, self.gods, self.cities)
                self.state.date.inc_month()
                #print("Month of {}".format(self.state.date.month))

                if len(self.state.humanoids) <= 0:
                    print("__ALL HUMANOIDS DIED")
                    return

            #self.birth_rate = round(len(self.yearly_births) / (self.yearly_population / len(calendar['months'])) * 1000, 2)
            #self.death_rate = round(len(self.yearly_deaths) / (self.yearly_population / len(calendar['months'])) * 1000, 2)

            build_table(self.state.date.month, self.state.date.year, self.state.humanoids,
                        self.state.gods, self.state.cities)

            # print(">Year {}, {} humanoids, {} birth rate {} death rate, {} index"
            #       .format(self.date.year, len(self.humanoids), self.birth_rate,
            #           self.death_rate, self.birth_rate - self.death_rate))

            gc.collect()



    def simulate_month(self):
        self.pool.map(lambda c: c.actions(self.state), self.state.cities)
        self.pool.map(lambda h: h.actions(self.state), self.state.humanoids)
        #self.pool.map(lambda h: h.actions(self.state), self.state.humanoids)
        self.state.end_frame(self.pool)

        #self.pool.close()
        #self.pool.join()

        #print("_End of {} year {}, {} humanoids, {} births, {} deaths".format(self.date.month, self.date.year, len(self.humanoids), len(self.births), len(self.deaths)))









