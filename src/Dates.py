from src.Utils import *

calendar = {
    'seasons':["Spring", 'Summer', 'Autumn', 'Winter']
}

class Date:
    def __init__(self):
        self.month_num = 0
        self.month = calendar['months'][self.month_num]
        self.year = 0

    def inc_month(self):
        self.month_num += 1
        if self.month_num >= len(calendar['months']):
            self.month_num = 0

            log_event(self, "New Years Eve")
            print("New Years Eve {}".format(self.year))
            self.year += 1

        self.month = calendar['months'][self.month_num]


        # self.season =
