
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

        self.attr_str = 10
        self.attr_agi = 10
        self.attr_con = 10
        self.attr_int = 10
        self.attr_wis = 10
        self.attr_cha = 10


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