from src.Utils import *
from src.Dates import *
from src.Generator import Generator
from src.simulator.Simulator import Simulator
from src.simulator.SimulationRenderer import *

import time

#random.seed('a')
if __name__ == "__main__":
    purge_tables()
    setup_log()

    worldgen = Generator()
    print('Generating world')
    state = worldgen.generate((WORLD_SIZE, WORLD_SIZE))

    start = time.time()
    simulator = Simulator(state, AGE)
    if ENABLE_UI:
        renderer = SimuulationRrenderer(simulator)

    while not simulator.simulation_over:
        next(simulator.age())

        if ENABLE_UI:
            renderer.update()

    end = time.time()
    print("____SIMULATION OVER____ Took {} seconds - Lasted {} months and {} years".format(end - start, simulator.state.date.year * len(calendar['months']), simulator.state.date.year))

    print("# ----------- #")
    print("Building Tables")
    start = time.time()
    build_table(simulator.state.date, simulator.state.humanoids, simulator.state.gods, simulator.state.cities)
    end = time.time()
    print("Tables took {} seconds".format(end-start))