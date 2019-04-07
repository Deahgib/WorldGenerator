from src.Dates import *
from src.Entities.Humanoid import Humanoid
from src.Utils import *
import random
from multiprocessing.dummy import Pool as ThreadPool
import gc
from src.simulator.SimulationRenderer import *

class Simulator:
    def __init__(self, state):
        self.state = state

        self.birth_rate = 0
        self.death_rate = 0
        self.pool = ThreadPool(THREAD_POOLS)
        self.renderer = SimuulationRrenderer()

    def age(self, simulation_years):
        self.renderer.setup(self.state)
        self.yearly_population = 0
        for y in range(simulation_years):
            self.yearly_births = set()
            self.yearly_deaths = set()
            for m in calendar['months']:
                self.simulate_month()
                self.renderer.update(self.state)
                self.state.date.inc_month()

                if len(self.state.humanoids) <= 0:
                    print("__ALL HUMANOIDS DIED")
                    return


            #build_table(self.state.date.month, self.state.date.year, self.state.humanoids, self.state.gods, self.state.cities)

            gc.collect()



    def simulate_month(self):
        self.pool.map(lambda c: c.actions(self.state), self.state.cities)
        self.pool.map(lambda h: h.actions(self.state), self.state.humanoids)
        self.state.end_frame(self.pool)









