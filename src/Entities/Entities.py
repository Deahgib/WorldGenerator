
class Entity:
    def __init__(self):
        self.name = ""
        self.location = (0, 0)


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
        self.id = self
        self.divine_attributes = set()
        self.worshiped_by = set()