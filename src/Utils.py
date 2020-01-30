import pandas as pd
import os
import shutil
from src.NameGenerator import NameGenerator
from src.RandomRoll import Dice
import math
import logging
import threading
lock = threading.Lock()

ENABLE_LOG = True
ENABLE_CONSOLE = False
ENABLE_UI = True

THREAD_POOLS = 32

HUMANOID_CONSUMES = 1
HUMANOID_FARMS = 3
HUMANOID_FORAGES = 2


class AllHumanoidsDied(Exception):
   pass

primitives = {
    'territories': ['sea', 'wilderness','forest', 'crops', "sand", "mountain"],
    'divine_attributes': ['harvest', 'war', 'thunder', 'lore', 'harmony', 'time', 'fertility', 'chaos', 'magic', 'hunt', 'necromancy'],
    'attribute_names': ["str", "dex", "con", "int", "wis", "cha"],

    "attributes":{
        'human': {
            'oldest': 83,
            'adult': 14,
            'roll': 4,
            'take': 3
        },
        'dwarf': {
            'oldest': 140,
            'adult': 18,
            'roll': 4,
            'take': 3
        },
        'elf': {
            'oldest': 500,
            'adult': 45,
            'roll': 5,
            'take': 3
        },
        'orc': {
            'oldest': 40,
            'adult': 9,
            'roll': 6,
            'take': 2
        }
    },

    'jobs': ["farm", "industry"],
    'races':{
        'humanoid': ['human', 'dwarf', 'elf', 'orc'],
        'animal': []
    },
    'geni': ["humanoid"]
}

names = NameGenerator()
dice = Dice()


def setup_log():
    if os.path.exists('./logs'):
        shutil.rmtree('./logs')

    os.mkdir('./logs')

    f = open("event.log", "w+")
    f.close()
    f = open("logs/city_status.csv", "w+")
    f.close()

def log_event(date, message):
    if ENABLE_LOG:
        lock.acquire()
        f = open("logs/event.csv", "a+")
        f.write("{},{},event,{}\n".format(date.year, date.month, message))
        f.close()
        lock.release()

def log_city_status(date, message):
    if ENABLE_LOG:
        lock.acquire()
        f = open("logs/city_status.csv", "a+")
        f.write("{},{},city_status,{}\n".format(date.year, date.month, message))
        f.close()
        lock.release()

def nlargest(in_list, N):
    assert in_list is not None, "Input list is None"
    assert len(in_list) > 0, "Input list is empty"
    assert len(in_list) > N, "Input list to small for sample size list={} N={}".format(in_list, N)
    assert N > 0, "Sample size is not a positive integer N=" + str(N)
    list1 = list(in_list)
    largest = list()
    for i in range(N):
        maxv = max(list1)
        list1.remove(maxv)
        largest.append(maxv)

    return largest


def number_of_threads(size, max_per_thread = 100):
    assert size > 0 and max_per_thread > 0, "Container size must be >0 and max_per_thread must be >0"
    return int(size / max_per_thread) + 1

def purge_tables():
    if os.path.exists('./history'):
        shutil.rmtree('./history')

    os.mkdir('./history')

def build_table(date, hum, god, cit, include_datestamp = True):
    h = [h.__dict__ for h in hum]
    g = [h.__dict__ for h in god]
    c = [h.__dict__ for h in cit]
    # hdf = pd.DataFrame(h)
    # hdf.to_csv('humanoids.csv')
    # hdf = pd.DataFrame(g)
    # hdf.to_csv('gods.csv')
    # hdf = pd.DataFrame(c)
    # hdf.to_csv('cities.csv')
    rows = g+c+h
    if include_datestamp:
        for r in rows:
            r['datestamp'] = "{}-{}".format(date.year, date.month_num)

    hdf = pd.DataFrame(rows)

    # century = math.floor(date.year/100) + 1

    # if not os.path.exists('./history/century{}'.format(century)):
    #     os.mkdir('./history/century{}'.format(century))
    # if not os.path.exists('./history/century{}/year{}'.format(century, date.year)):
    #     os.mkdir('./history/century{}/year{}'.format(century, date.year))
    #
    # hdf.to_csv('history/century{}/year{}-{}.csv'.format(century, date.year, date.month))

    hdf.to_csv('history/{}-{} ({}).csv'.format(date.year, date.month_num, date.month), index_label=False)


def get_modifier(attribute):
    return math.floor((attribute - 10) / 2)

def food_cost(population):
    return population * HUMANOID_CONSUMES

