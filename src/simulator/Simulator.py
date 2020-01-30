from src.Dates import *
from src.Entities.Humanoid import Humanoid
from src.Utils import *
import random
from multiprocessing.dummy import Pool as ThreadPool
import gc
from src.simulator.SimulationRenderer import *

class Simulator:
    def __init__(self, state, simulation_years):
        self.state = state
        self.simulation_years = simulation_years
        self.birth_rate = 0
        self.death_rate = 0
        self.pool = ThreadPool(THREAD_POOLS)
        #self.renderer = SimuulationRrenderer()

    def run_year(self):
        self.yearly_births = set()
        self.yearly_deaths = set()
        for m in calendar['months']:
            try:
                self.run_month()
            except AllHumanoidsDied:
                raise AllHumanoidsDied


    def run_month(self):
        self.simulate_month()
        # self.renderer.update(self.state)
        self.state.date.inc_month()
        build_table(self.state.date, self.state.humanoids, self.state.gods, self.state.cities)
        if len(self.state.humanoids) <= 0:
            #print("__ALL HUMANOIDS DIED")
            raise AllHumanoidsDied


    def age(self):
        #self.renderer.setup(self.state)
        self.yearly_population = 0
        for y in range(self.simulation_years):
            self.yearly_births = set()
            self.yearly_deaths = set()
            try:
                self.run_year()
            except AllHumanoidsDied:
                print("__ All Humanoids Died !")
                gc.collect()
                return
            gc.collect()
            yield



    def simulate_month(self):
        self.pool.map(lambda c: c.actions(self.state), self.state.cities)
        self.pool.map(lambda h: h.actions(self.state), self.state.humanoids)
        self.pool.map(lambda e: e.run_encounter(), self.state.encounters)
        self.state.end_frame(self.pool)
        print("{} Humanoids roam the world.".format(len(self.state.humanoids)))








