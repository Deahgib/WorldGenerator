from src.Dates import *
from src.Entities.Humanoid import Humanoid
from src.Utils import *
import random
from multiprocessing.dummy import Pool as ThreadPool
import gc
from src.simulator.SimulationRenderer import *

class Simulator:
    def __init__(self, state, simulation_years):
        self.simulation_over = False
        self.state = state
        self.simulation_years = simulation_years
        self.birth_rate = 0
        self.death_rate = 0
        self.pool = ThreadPool(THREAD_POOLS)
        #self.renderer = SimuulationRrenderer()

    def age(self):
        #self.renderer.setup(self.state)
        try:
            try:
                self.run_month()
                if self.state.date.year > self.simulation_years:
                    self.simulation_over = True
                if self.state.date.month_num == len(calendar['months'])-1:
                    gc.collect()
                yield
            except AllHumanoidsDied:
                raise AllHumanoidsDied
        except AllHumanoidsDied:
            print("__ All Humanoids Died !")
            self.state.simulation_over = True
            gc.collect()
            return


    def run_month(self):
        self.simulate_month()
        # self.renderer.update(self.state)
        self.state.date.inc_month()
        build_table(self.state.date, self.state.humanoids, self.state.gods, self.state.cities)
        if len(self.state.humanoids) <= 0:
            #print("__ALL HUMANOIDS DIED")
            raise AllHumanoidsDied


    def simulate_month(self):
        self.pool.map(lambda g: g.actions(self.state), self.state.gods)
        self.pool.map(lambda c: c.actions(self.state), self.state.cities)
        self.pool.map(lambda h: h.actions(self.state), self.state.humanoids)
        self.pool.map(lambda e: e.run_encounter(), self.state.encounters)
        self.state.end_frame(self.pool)
        if ENABLE_CONSOLE:
            print("{} Humanoids roam the world.".format(len(self.state.humanoids)))








