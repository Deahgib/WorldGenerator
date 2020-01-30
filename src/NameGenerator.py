from __future__ import unicode_literals
from os.path import abspath, join, dirname
import random


__title__ = 'names'
__version__ = '0.3.0'
__author__ = 'Trey Hunner'
__license__ = 'MIT'


full_path = lambda filename: abspath(join(dirname(__file__), filename))
FILES = {
    'first:male': full_path('names/dist.male.first'),
    'first:female': full_path('names/dist.female.first'),
    'last': full_path('names/dist.all.last'),
}

class NameGenerator:

    def get_name(self, filename):
        selected = random.random() * 90
        with open(filename) as name_file:
            for line in name_file:
                name, _, cummulative, _ = line.split()
                if float(cummulative) > selected:
                    return name
        return ""  # Return empty string if file is empty


    def get_first_name(self, gender=None):
        if gender not in ('male', 'female'):
            gender = random.choice(('male', 'female'))
        return self.get_name(FILES['first:%s' % gender]).capitalize()


    def get_last_name(self):
        return self.get_name(FILES['last']).capitalize()


    def get_full_name(self, gender=None):
        return "{0} {1}".format(self.get_first_name(gender), self.get_last_name())
