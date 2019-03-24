from src.Entities.Entities import *

class Building(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.cost = 0

class Farm(Building):
    def __init__(self):
        Building.__init__(self)
        self.name = "Farm"
        self.cost = 50
        self.crop_count = 50