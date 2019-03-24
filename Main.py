import pandas as pd
import random

from Utils import *
from Dates import *
from Generator import Generator
from Simulator import Simulator

import time

#random.seed('a')
if __name__ == "__main__":
    purge_tables()

    worldgen = Generator()
    print('Generating world')
    worldgen.generate((5, 5))

    start = time.time()
    simulator = Simulator(worldgen.world_gen.map, worldgen.humanoids, worldgen.cities, worldgen.gods)
    simulator.age(50)
    end = time.time()
    build_table(simulator.date.month, simulator.date.year, simulator.humanoids, simulator.gods, simulator.cities)

    print("____SIMULATION OVER____ Took {} seconds - Lasted {} months and {} years".format(end - start, simulator.date.year * len(calendar['months']), simulator.date.year))

    print("# ----------- #")
    print("Building Tables")
    # start = time.time()
    # h = [h.__dict__ for h in simulator.humanoids]
    # g = [h.__dict__ for h in simulator.gods]
    # c = [h.__dict__ for h in simulator.cities]
    # hdf = pd.DataFrame(h)
    # hdf.to_csv('humanoids.csv')
    # hdf = pd.DataFrame(g)
    # hdf.to_csv('gods.csv')
    # hdf = pd.DataFrame(c)
    # hdf.to_csv('cities.csv')
    # hdf = pd.DataFrame(h+g+c)
    # hdf.to_csv('entities.csv')

    # for god in worldgen.humanoids:
    #     print('{}'.format(god.__dict__))
    #
    # for god in worldgen.gods:
    #     print('{}'.format(god.__dict__))
    #
    # for god in worldgen.cities:
    #     print('{}'.format(god.__dict__))

    end = time.time()

    print("Tables took {} seconds".format(end-start))