
import random

class Dice:
    def roll(self, size, rolls):
        assert rolls > 0, "Imposible number of rolls < 1 : N=" + str(rolls)
        if rolls == 1:
            return random.randint(1, size)
        else:
            vals = list()
            for r in range(rolls):
                vals.append(random.randint(1, size))

            return vals

    def d2(self, rolls = 1):
        return self.roll(2, rolls)

    def d4(self, rolls = 1):
        return self.roll(4, rolls)

    def d6(self, rolls = 1):
        return self.roll(6, rolls)

    def d8(self, rolls = 1):
        return self.roll(8, rolls)

    def d10(self, rolls = 1):
        return self.roll(10, rolls)

    def d12(self, rolls = 1):
        return self.roll(12, rolls)

    def d20(self, rolls = 1):
        return self.roll(20, rolls)

    def d100(self, rolls = 1):
        return self.roll(100, rolls)

