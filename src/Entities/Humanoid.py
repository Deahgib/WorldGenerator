from src.Entities.Entities import Mortal
from src.JobManager import *
import random
from src.Utils import *

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

    def actions(self, state):
        desire = random.random()

        if self.health > 0:
            if self.home.food > 0:
                self.home.food -= HUMANOID_CONSUMES
                self.health = min(self.health + 0.2, 1.0)
            else:
                #print("{} is starving!".format(self.name))
                self.health = max(self.health - 0.2, 0.0)

            if self.adult:
                local = [r for r in state.humanoids if r.location == self.location]
                local_friends = [r for r in local if r.race == self.race]

                self.temperament = max(min(self.temperament + random.gauss(0.0, 0.1), 1.0), -1.0)
                if self.temperament < -0.5 and self.lawful < -0.25 and self.goodness < -0.25:
                    #print("{} is angry".format(humanoid.name))
                    # TODO Attack a closeby humanoid
                    self.temperament += max(min(self.temperament + 0.2, 1.0), -1.0)
                    victim = random.choice(local)
                    victim.health -= 0.3
                    victim.temperament = max(min(victim.temperament - 0.1, 1.0), -1.0)
                    #print('{} attacked {}'.format(humanoid.name, victim.name))
                    #if victim.health <= 0.1:
                        #print('{} killed {}'.format(humanoid.name, victim.name))
                else:
                    # TODO Do work
                    self.temperament = max(min(self.temperament + 0.1, 1.0), -1.0)

                    # Do Love
                    if desire > 0.7:
                        # print("{} wants a child".format(humanoid.name))
                        self.desire = True
                        oposite_sex = [s for s in local_friends if s.sex != self.sex and s.desire]
                        if len(oposite_sex) > 0:
                            partner = random.choice(oposite_sex)

                            # print("{} courts {}".format(humanoid.name, partner.name))

                            lust = random.random()
                            if lust > 0.1:
                                if partner.sex == 'male':
                                    self.birth_humanoid(state, partner, self)
                                else:
                                    self.birth_humanoid(state, self, partner)
                            else:
                                self.temperament = max(min(self.temperament - 0.1, 1.0), -1.0)

                    elif  desire < 0.1:
                        self.desire = False

                    if self.age < primitives['ages'][self.race]["oldest"]:
                        state.job = do_job(self)

        # if humanoid.health < 1:
        #     humanoid.health += max(min(humanoid.health + 0.1, 1.0), 0.0)

        # Age humanoid
        if self.month_of_birth == state.date.month:
            self.age += 1
            if self.age == primitives['ages'][self.race]['adult']:
                self.adult = True
                #print('{} has become an adult'.format(humanoid.name))


        oldest = primitives['ages'][self.race]['oldest']
        if self.age >= (oldest):
            if random.random() < 0.1:
                self.health = 0
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

        genus, race, sex, str, dex, con, int, wis, cha = tuple(dna)
        baby.location = mother.location
        baby.home = mother.home
        baby.genus = genus
        baby.race = race
        baby.age = 0
        baby.sex = sex
        baby.adult = False
        baby.month_of_birth = state.date.month
        baby.attributes["str"] = str
        baby.attributes["dex"] = dex
        baby.attributes["con"] = con
        baby.attributes["int"] = int
        baby.attributes["wis"] = wis
        baby.attributes["cha"] = cha
        baby.fname = names.get_first_name(race='human', gender=baby.sex)
        baby.lname = mother.lname
        baby.name = baby.fname + " " + baby.lname
        baby.favorite_god = random.choice([g for g in state.gods if baby.race in g.worshiped_by])
        baby.favorite_god_name = baby.favorite_god.name
        baby.favorite_god_attributes = baby.favorite_god.divine_attributes
        baby.goodness = max(min(random.gauss(baby.favorite_god.goodness, 0.2), 1.0), -1.0)
        baby.lawful = max(min(random.gauss(0.0, 0.5), 1.0), -1.0)
        baby.temperament = max(min(random.gauss(0.0, 0.1), 1.0), -1.0)
        baby.health = 1

        # print("The {} {}, is born to mother {} and father {}".format(baby.race, baby.name, mother.name, father.name))
        state.births.add(baby)
