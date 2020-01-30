
class Entity:
    def __init__(self):
        self.name = ""


class Faction(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.members = []

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)

    def add_member(self, member):
        if member not in self.members:
            self.members.append(member)

class Physical(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.location = (0, 0)

class Group(Physical):
    def __init__(self):
        Physical.__init__(self)
        self.faction = None


class Being(Physical):
    def __init__(self):
        Physical.__init__(self)
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
        self.max_health = 10
        self.health = 10
        self.temperament = 0

        self.desire = False
        self.adult = False


        self.armour_class = 10
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


