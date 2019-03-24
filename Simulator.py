from Dates import *
from Utils import *
from Entities import *
from RandomRoll import Dice
from names import NameGenerator

import random
from multiprocessing.dummy import Pool as ThreadPool


class Simulator:
    def __init__(self, map, humanoids, cities, gods, animals = None, monesters = None):
        self.map = list(map)
        self.humanoids = set(humanoids)
        self.cities = set(cities)
        self.gods = set(gods)
        self.date = Date()
        self.dice = Dice()
        self.names = NameGenerator(primitives['races']['humanoid'], ["male", "female"])
        self.births = set()
        self.yearly_births = set()
        self.deaths = set()
        self.yearly_deaths = set()
        self.yearly_population = 0

        self.pool = ThreadPool(150) #number_of_threads(1)
        self.birth_rate = 0
        self.death_rate = 0

    def age(self, simulation_years):
        self.yearly_population = 0
        for y in range(simulation_years):
            self.yearly_births = set()
            self.yearly_deaths = set()
            for m in calendar['months']:
                self.simulate__month()
                self.yearly_population += len(self.humanoids)
                #self.yearly_births = self.yearly_births | self.births
                #self.yearly_deaths = self.yearly_deaths | self.deaths
                #build_table(self.date.month, self.date.year, self.humanoids, self.gods, self.cities)
                self.date.inc_month()
                print(">{}".format(self.date.month))

                if len(self.humanoids) <= 0:
                    print("__ALL HUMANOIDS DIED")
                    return

            self.birth_rate = round(len(self.yearly_births) / (self.yearly_population / len(calendar['months'])) * 1000, 2)
            self.death_rate = round(len(self.yearly_deaths) / (self.yearly_population / len(calendar['months'])) * 1000, 2)

            print(">Year {}, {} humanoids, {} birth rate {} death rate, {} index"
                  .format(self.date.year, len(self.humanoids), self.birth_rate,
                      self.death_rate, self.birth_rate - self.death_rate))




    def simulate__month(self):
        self.deaths = set()
        self.births = set()

        self.pool.map(self.humanoid_actions, self.humanoids)
        self.pool.map(self.humanoids.remove, self.deaths)
        self.humanoids = self.humanoids | self.births

        self.pool.map(self.city_actions, self.cities)
        self.pool.map(self.cities.remove, set([c for c in self.cities if c.population <= 0]))

        #print("_End of {} year {}, {} humanoids, {} births, {} deaths".format(self.date.month, self.date.year, len(self.humanoids), len(self.births), len(self.deaths)))

    def city_actions(self, city):
        population = [h for h in self.humanoids if h.home == city]
        city.population = len(population)
        if city.population <= 0:
            print("The city of {} has fallen to ruin!".format(city.name))
            return

        adults = [a for a in population if a.adult]
        births = [b for b in self.births if b.home == city.location]
        deaths = [d for d in self.deaths if d.home == city.location]
        city.birth_rate = 0 if len(adults) <= 0 else round(len(births) / len(adults) * 1000, 2)
        city.death_rate = 0 if len(adults) <= 0 else round(len(deaths) / len(adults) * 1000, 2)
        city.work = set()

        fc = food_cost(city.population)
        if city.food - 2*fc < 0:
            city.work.add("farm")
        else:
            city.work.add("farm")
            city.work.add("industry")

        #print(fc)
        #print(city.work)
        print("-- City FOOD {} POPULATION {} WEALTH {}".format(city.food, city.population, city.wealth))



    def do_job(self, humanoid):
        # Do work
        if humanoid.home.work.__len__() > 0:
            job = random.choice(list(humanoid.home.work))
            #print("{} has job {}".format(humanoid.name, job))
            if job == "farm":
                humanoid.home.food += HUMANOID_FARMS
            elif job == "industry":
                humanoid.home.wealth += 1

            humanoid.temperament = max(min(humanoid.temperament + 0.1, 1.0), -1.0)

    def birth_humanoid(self, father, mother):
        baby = Humanoid()

        dna = []
        for f, m in zip(mother.dna.split('-'), father.dna.split('-')):
            dna.append(f if self.dice.d2() == 1 else m)
        baby.dna = ('%s-%s-%s-%s-%s-%s-%s-%s-%s' % tuple(dna))

        genus, race, sex, str, dex, con, int, wis, cha = tuple(dna)
        baby.location = mother.location
        baby.home = mother.home
        baby.genus = genus
        baby.race = race
        baby.age = 0
        baby.sex = sex
        baby.adult = False
        baby.month_of_birth = self.date.month
        baby.attributes["str"] = str
        baby.attributes["dex"] = dex
        baby.attributes["con"] = con
        baby.attributes["int"] = int
        baby.attributes["wis"] = wis
        baby.attributes["cha"] = cha
        baby.fname = self.names.get_first_name(race='human', gender=baby.sex)
        baby.lname = mother.lname
        baby.name = baby.fname + " " + baby.lname
        baby.favorite_god = random.choice([g for g in self.gods if baby.race in g.worshiped_by])
        baby.favorite_god_name = baby.favorite_god.name
        baby.favorite_god_attributes = baby.favorite_god.divine_attributes
        baby.goodness =  max(min(random.gauss(baby.favorite_god.goodness, 0.2), 1.0), -1.0)
        baby.lawful = max(min(random.gauss(0.0, 0.5), 1.0), -1.0)
        baby.temperament = max(min(random.gauss(0.0, 0.1), 1.0), -1.0)
        baby.health = 1

        #print("The {} {}, is born to mother {} and father {}".format(baby.race, baby.name, mother.name, father.name))
        self.births.add(baby)

    def humanoid_actions(self, humanoid):
        desire = random.random()

        if humanoid.health > 0:
            if humanoid.home.food > 0:
                humanoid.home.food -= HUMANOID_CONSUMES
                humanoid.health = min(humanoid.health + 0.2, 1.0)
            else:
                print("{} is starving!".format(humanoid.name))
                humanoid.health = max(humanoid.health - 0.2, 0.0)

            if humanoid.adult:
                local = [r for r in self.humanoids if r.location == humanoid.location ]
                local_friends = [r for r in local if r.race == humanoid.race]

                humanoid.temperament = max(min(humanoid.temperament + random.gauss(0.0, 0.1), 1.0), -1.0)
                if humanoid.temperament < -0.5 and humanoid.lawful < -0.25 and humanoid.goodness < -0.25:
                    #print("{} is angry".format(humanoid.name))
                    # TODO Attack a closeby humanoid
                    humanoid.temperament += max(min(humanoid.temperament + 0.2, 1.0), -1.0)
                    victim = random.choice(local)
                    victim.health -= 0.3
                    victim.temperament = max(min(victim.temperament - 0.1, 1.0), -1.0)
                    #print('{} attacked {}'.format(humanoid.name, victim.name))
                    #if victim.health <= 0.1:
                        #print('{} killed {}'.format(humanoid.name, victim.name))
                else:
                    # TODO Do work
                    humanoid.temperament = max(min(humanoid.temperament + 0.1, 1.0), -1.0)

                    # Do Love
                    if desire > 0.7:
                        # print("{} wants a child".format(humanoid.name))
                        humanoid.desire = True
                        oposite_sex = [s for s in local_friends if s.sex != humanoid.sex and s.desire]
                        if len(oposite_sex) > 0:
                            partner = random.choice(oposite_sex)

                            # print("{} courts {}".format(humanoid.name, partner.name))

                            lust = random.random()
                            if lust > 0.1:
                                if partner.sex == 'male':
                                    self.birth_humanoid(partner, humanoid)
                                else:
                                    self.birth_humanoid(humanoid, partner)
                            else:
                                humanoid.temperament = max(min(humanoid.temperament - 0.1, 1.0), -1.0)

                    elif  desire < 0.1:
                        humanoid.desire = False

                    if humanoid.age < primitives['ages'][humanoid.race]["oldest"]:
                        self.job = self.do_job(humanoid)

        # if humanoid.health < 1:
        #     humanoid.health += max(min(humanoid.health + 0.1, 1.0), 0.0)

        # Age humanoid
        if humanoid.month_of_birth == self.date.month:
            humanoid.age += 1
            if humanoid.age == primitives['ages'][humanoid.race]['adult']:
                humanoid.adult = True
                #print('{} has become an adult'.format(humanoid.name))


        oldest = primitives['ages'][humanoid.race]['oldest']
        if humanoid.age >= (oldest):
            if random.random() < 0.1:
                humanoid.health = 0
                #print("{} is taken by old age".format(humanoid.name))

        if humanoid.health <= 0:
            self.deaths.add(humanoid)
            return
            #print("{} died".format(humanoid.name))


