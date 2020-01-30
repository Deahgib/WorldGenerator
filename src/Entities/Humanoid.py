from src.Entities.Entities import Mortal
import random
from src.Utils import *

# class Belief():
#     def __init__(self):
#         self.hostile = False
#         self.love = False
#         self.happy = False
#         self.stress = False


class Humanoid(Mortal):
    def __init__(self):
        Mortal.__init__(self)
        self.id = self
        self.fname = ''
        self.lname = ''
        self.favorite_job = ''
        self.favorite_god = ''
        self.favorite_god_attributes = ''
        self.lawful = 0
        self.month_of_birth = 0
        self.happiness = 0
        self.beliefs_graph = {}
        self.desires_graph = {}
        self.is_blessed = False

    def is_alive(self):
        return self.health > 0

    def do_job(self):
        # Do work
        if self.home.work.__len__() > 0:
            if self.favorite_job in self.home.work.keys():
                job = self.favorite_job
                self.temperament = max(min(self.temperament + 0.1, 1.0), -1.0)
            else:
                if self.home.work["farm"] > 0:
                    job = "farm"
                    self.home.work["farm"] -= 1
                elif self.home.work["industry"] > 0:
                    job = "industry"
                    self.home.work["industry"] -= 1

            # print("{} has job {}".format(humanoid.name, job))
            if job == "farm":
                self.home.food += HUMANOID_FARMS
            elif job == "industry":
                self.home.wealth += 1

            self.temperament = max(min(self.temperament + 0.1, 1.0), -1.0)

    def percepts(self, state):
        pop, friends = state.get_local(self)
        return (pop, friends, self.home.work)

    def beliefs(self, state, percepts):
        local, friends, jobs = percepts
        beliefs_graph = {
            "people": len(friends) > 0,
            "worship": state.date.month in self.favorite_god.divine_attributes,
            "familly": random.random() > 0.9
        }
        return beliefs_graph

    def desires(self, state, percepts):
        local, friends, jobs = percepts
        self.temperament = max(min(self.temperament + random.gauss(0.0, 0.1), 1.0), -1.0)
        self.happiness = max(min(self.happiness + random.gauss(0.0, 0.1), 1.0), -1.0)
        desires_graph = {
            "love": random.random() > 0.9,
            "procreate": random.random() > 0.9,
            "happy": self.happiness > 0,
            "violent": self.happiness < 0 and self.goodness < 0 and self.temperament < 0
        }

        return desires_graph

    def reciprocate_love(self):
        return self.desires_graph['love']

    def actions(self, state):


        #desire = random.random()
        percepts = self.percepts(state)
        self.is_blessed = self.favorite_god.seek_blessing(self)
        self.beliefs_graph = self.beliefs(state, percepts)
        self.desires_graph = self.desires(state, percepts)
        local, friends, jobs = percepts

        #yield

        if self.health > 0:
            if self.home.food > 0:
                self.home.food -= HUMANOID_CONSUMES
                self.health = min(self.health + 2, self.max_health)
            else:
                #print("{} is starving!".format(self.name))
                self.health = max(self.health - 2, 0.0)

            if self.adult:
                if self.desires_graph['violent']:
                    #print("{} is angry".format(humanoid.name))
                    # TODO Attack a closeby humanoid
                    self.temperament += max(min(self.temperament + 0.2, 1.0), -1.0)
                    victim = random.choice(local)
                    victim.health -= 3
                    victim.temperament = max(min(victim.temperament - 0.1, 1.0), -1.0)
                    #print('{} attacked {}'.format(humanoid.name, victim.name))
                    #if victim.health <= 1:
                        #print('{} killed {}'.format(humanoid.name, victim.name))
                else:
                    # Do Love
                    if self.beliefs_graph['people'] and self.desires_graph['procreate']:
                        # print("{} wants a child".format(humanoid.name))
                        self.desire = True
                        oposite_sex = [s for s in friends if s.sex != self.sex and s.desire]
                        if len(oposite_sex) > 0:
                            partner = random.choice(oposite_sex)
                            if partner.reciprocate_love():
                                if partner.sex == 'male':
                                    self.birth_humanoid(state, partner, self)
                                else:
                                    self.birth_humanoid(state, self, partner)

                    else:
                        self.desire = False

                    if self.age < primitives['attributes'][self.race]["oldest"]:
                        state.job = self.do_job()

        # if humanoid.health < 1:
        #     humanoid.health += max(min(humanoid.health + 0.1, 1.0), 0.0)

        # Age humanoid
        if self.month_of_birth == state.date.month:
            self.age += 1
            if self.age == primitives['attributes'][self.race]['adult']:
                self.adult = True
                #print('{} has become an adult'.format(humanoid.name))


        oldest = primitives['attributes'][self.race]['oldest']
        if self.age >= (oldest):
            if random.random() < 0.1:
                self.health = 0
                return
                #print("{} is taken by old age".format(humanoid.name))

        if self.health <= 0:
            state.kill_humanoid(self)
            return
            #print("{} died".format(humanoid.name))

    def birth_humanoid(self, state, father, mother):
        baby = Humanoid()

        dna = []
        for f, m in zip(mother.dna.split('-'), father.dna.split('-')):
            dna.append(f if dice.d2() == 1 else m)
        baby.dna = ('%s-%s-%s-%s-%s-%s-%s-%s-%s' % tuple(dna))

        genus, race, sex, stre, dex, con, inte, wis, cha = tuple(dna)
        baby.armour_class = 14 + random.randint(-4, 4)
        baby.location = mother.location
        baby.home = mother.home
        baby.genus = genus
        baby.race = race
        baby.age = 0
        baby.sex = sex
        baby.adult = False
        baby.month_of_birth = state.date.month
        baby.attr_str = int(stre)
        baby.attr_agi = int(dex)
        baby.attr_con = int(con)
        baby.attr_int = int(inte)
        baby.attr_wis = int(wis)
        baby.attr_cha = int(cha)
        baby.fname = names.get_first_name(gender=baby.sex)
        baby.lname = mother.lname
        baby.name = baby.fname + " " + baby.lname
        baby.favorite_god = random.choice([g for g in state.gods if baby.race in g.worshiped_by])
        baby.favorite_god_name = baby.favorite_god.name
        baby.favorite_god_attributes = baby.favorite_god.divine_attributes
        baby.goodness = max(min(random.gauss(baby.favorite_god.goodness, 0.2), 1.0), -1.0)
        baby.lawful = max(min(random.gauss(0.0, 0.5), 1.0), -1.0)
        baby.temperament = max(min(random.gauss(0.0, 0.1), 1.0), -1.0)
        baby.max_health = 10 + random.randint(0, 10)
        baby.health = math.ceil(baby.max_health / 2)

        # print("The {} {}, is born to mother {} and father {}".format(baby.race, baby.name, mother.name, father.name))
        state.births.add(baby)
