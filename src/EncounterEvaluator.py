from src.RandomRoll import Dice
from src.Utils import *

class EncounterEvaluator:
    def __init__(self, state, attacker_city, defender_city, attackers, defenders):
        self.state = state
        self.attacker = attacker_city
        self.defender = defender_city
        self.attackers = list(attackers)
        self.defenders = list(defenders)
        self.combat_state = "calm before the storm"

    def get_next_fighter(self, fighter, fighters):
        if fighter == None or fighter.health <= 0:
            if len(fighters) > 0:
                return fighters.pop()
            else:
                None
        else:
            return fighter

    def run_encounter(self):
        self.combat_state = "fighting"
        attackers = list(self.attackers)
        defenders = list(self.defenders)

        if len(defenders) > 0 and len(attackers) > 0:
            attacker = attackers.pop() if len(attackers) > 0 else None
            defender = defenders.pop() if len(defenders) > 0 else None

            # Every round is 6 seconds
            while(attacker != None and defender != None):
                attacker = self.get_next_fighter(attacker, attackers)
                defender = self.get_next_fighter(defender, defenders)
                self.combat_action(attacker, defender)

                attacker = self.get_next_fighter(attacker, attackers)
                defender = self.get_next_fighter(defender, defenders)
                self.combat_action(defender, attacker)


            tot_casualties = (len(self.attackers) - len(attackers)) + (len(self.defenders) - len(defenders))

            if len(attackers) <= 0:
                self.combat_state = "defeat"
                if ENABLE_CONSOLE:
                    print("The city of {} ({}) is DEFEATED in battle against the city of {} ({})!".format(self.attacker.name, self.attacker.race, self.defender.name, self.defender.race))
                if ENABLE_LOG:
                    log_event(self.state.date,
                              "The city of {} ({}) is DEFEATED in battle against the city of {} ({})!".format(self.attacker.name, self.attacker.race, self.defender.name, self.defender.race))

            else:
                self.combat_state = "victory"
                max_wealth_carry = len(attackers) * 10
                max_food_carry = len(attackers) * 5
                if self.defender.wealth > max_wealth_carry:
                    self.defender.wealth -= max_wealth_carry
                    self.attacker.wealth += max_wealth_carry
                else:
                    self.attacker.wealth += self.defender.wealth
                    self.defender.wealth = 0

                if self.defender.food > max_food_carry:
                    self.defender.food -= max_food_carry
                    self.attacker.food += max_food_carry
                else:
                    self.attacker.food += self.defender.food
                    self.defender.food = 0

                if ENABLE_CONSOLE:
                    print("The city of {} ({}) is VICTORIOUS in battle against the city of {} ({})!".format(self.attacker.name, self.attacker.race, self.defender.name, self.defender.race))
                if ENABLE_LOG:
                    log_event(self.state.date,
                              "The city of {} ({}) is VICTORIOUS in battle against the city of {} ({})!".format(self.attacker.name, self.attacker.race, self.defender.name, self.defender.race))

    def combat_action(self, attacker, defender):
        if attacker != None and defender != None:
            dice = Dice()
            proficiency = get_modifier(attacker.attr_str)
            proficiency += 4 if attacker.desires_graph["violent"] else 2
            roll_bonus = 1 if self.attacker.is_blessed else 0
            roll_bonus += 2 if attacker.is_blessed else 0

            if dice.d20() + proficiency + roll_bonus > defender.armour_class: # Is Hit ?
                dmg = dice.d6() + proficiency
                defender.health = max(defender.health - dmg, 0) # Do Damage

