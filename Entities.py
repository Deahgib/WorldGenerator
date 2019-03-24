
class Entity:
    def __init__(self):
        self.name = ""
        self.location = (0, 0)

class City(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.race = ''
        self.status = ''
        self.population = 0
        self.patron_god = ''
        self.patron_god_attributes = ''
        self.birth_rate = 0
        self.death_rate = 0
        self.food = 0
        self.work = set()
        self.wealth = 0

class Being(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.mortal = True
        self.goodness = 0


class Mortal(Being):
    def __init__(self):
        Being.__init__(self)
        self.mortal = True
        self.dna = ''
        self.genus = ""
        self.race = ""
        self.sex = 0
        self.age = 0

        self.home = None
        self.health = 1
        self.temperament = 0

        self.desire = False
        self.adult = False

        self.attributes = {
            "str": 0,
            "dex": 0,
            "con": 0,
            "int": 0,
            "wis": 0,
            "cha": 0
        }


class Humanoid(Mortal):
    def __init__(self):
        Mortal.__init__(self)
        self.fname = ''
        self.lname = ''
        self.favorite_job = ''
        self.favorite_god = ''
        self.favorite_god_attributes = ''
        self.lawful = 0
        self.month_of_birth = 0
        self.happiness = 0


class Animal(Mortal):
    def __init__(self):
        Mortal.__init__(self)

class Imortal(Being):
    def __init__(self):
        Being.__init__(self)
        self.mortal = False
        self.power = 0

class God(Imortal):
    def __init__(self):
        Imortal.__init__(self)
        self.divine_attributes = set()
        self.worshiped_by = set()