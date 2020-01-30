
from src.Entities.City import City
from src.Entities.Humanoid import Humanoid
from src.RandomRoll import Dice
from src.Entities.Entities import Imortal

class God(Imortal):
    def __init__(self):
        Imortal.__init__(self)
        self.id = self
        self.divine_attributes = set()
        self.worshiped_by = set()

    def seek_blessing(self, entity):
        if isinstance(entity, City):
            dice = Dice()
            if dice.d100() > 85:
                return True

        if isinstance(entity, Humanoid):
            dice = Dice()
            if dice.d20() > entity.attr_wis:
                return True

        return False