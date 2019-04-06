from src.Utils import *
from src.Dates import *
from src.Generator import Generator
from src.simulator.Simulator import Simulator

import time

#random.seed('a')
if __name__ == "__main__":
    purge_tables()

    worldgen = Generator()
    print('Generating world')
    state = worldgen.generate((5, 5))

    start = time.time()
    simulator = Simulator(state)
    simulator.age(200)
    end = time.time()
    print("____SIMULATION OVER____ Took {} seconds - Lasted {} months and {} years".format(end - start, simulator.state.date.year * len(calendar['months']), simulator.state.date.year))

    print("# ----------- #")
    print("Building Tables")
    start = time.time()
    build_table(simulator.state.date.month, simulator.state.date.year, simulator.state.humanoids, simulator.state.gods, simulator.state.cities)
    end = time.time()
    print("Tables took {} seconds".format(end-start))