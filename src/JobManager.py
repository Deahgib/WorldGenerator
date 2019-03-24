from src.Utils import *
import random



def do_job(humanoid):
    # Do work
    if humanoid.home.work.__len__() > 0:
        job = random.choice(list(humanoid.home.work))
        # print("{} has job {}".format(humanoid.name, job))
        if job == "farm":
            humanoid.home.food += HUMANOID_FARMS
        elif job == "industry":
            humanoid.home.wealth += 1

        humanoid.temperament = max(min(humanoid.temperament + 0.1, 1.0), -1.0)