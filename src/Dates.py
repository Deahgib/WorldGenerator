calendar = {
    'months':["stone", '', 'Winter', 'Spring']
}

class Date:
    def __init__(self):
        self.month = calendar['months'][0]
        self.year = 0

    def inc_month(self):
        v = calendar['months'].index(self.month)
        v += 1
        if v >= len(calendar['months']):
            v = 0
            self.year += 1

        self.month = calendar['months'][v]