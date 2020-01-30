from src.Dates import Date
from src.EncounterEvaluator import EncounterEvaluator


class State:
    def __init__(self, map, humanoids, cities, gods):
        """ Named arguments, map, humanoids, cities, gods """
        self.world_gen = None
        self.humanoids = set()
        self.factions = set()
        self.cities = set()
        self.gods = set()
        self.deaths = set()
        self.births = set()
        self.encounters = list()
        self.date = Date()
        self.population_count = 0
        self.force_state(map=map, humanoids=humanoids, cities=cities, gods=gods)

    def force_state(self, **kwargs):
        if kwargs['map'] is not None:
            self.world_gen = kwargs['map']
        if kwargs['humanoids'] is not None:
            self.humanoids = set(kwargs['humanoids'])
        if kwargs['cities'] is not None:
            self.cities = set(kwargs['cities'])
        if kwargs['gods'] is not None:
            self.gods = set(kwargs['gods'])

    def add_battle(self, encounter):
        if isinstance(encounter, EncounterEvaluator):
            self.encounters.append(encounter)

    def get_local(self, humanoid):
        population = [r for r in self.humanoids if r.location == humanoid.location ]
        friends = [r for r in population if r.race == humanoid.race]
        return population, friends

    def kill_humanoid(self, humanoid):
        self.deaths.add(humanoid)

    def end_frame(self, threadPool):
        self.population_count += len(self.humanoids)
        threadPool.map(self.humanoids.remove, self.deaths)
        self.humanoids = self.humanoids | self.births

        #threadPool.map(self.cities.remove, set([c for c in self.cities if c.population <= 0]))

        self.deaths = set()
        self.births = set()
        self.encounters = list()
