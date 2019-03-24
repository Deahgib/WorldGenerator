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
    simulator.age(50)
    end = time.time()
    build_table(simulator.state.date.month, simulator.state.date.year, simulator.state.humanoids, simulator.state.gods, simulator.state.cities)

    print("____SIMULATION OVER____ Took {} seconds - Lasted {} months and {} years".format(end - start, simulator.state.date.year * len(calendar['months']), simulator.state.date.year))

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