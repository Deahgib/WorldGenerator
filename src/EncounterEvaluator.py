from src.RandomRoll import Dice
from src.Utils import *

class EncounterEvaluator:
    def __init__(self, state, attacker_city, defender_city):
        self.state = state
        self.attacker_group = attacker_city
        self.defender_group = defender_city
        self.combat_state = "calm before the storm"
        self.tot_casualties = 0

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
        attackers = list(self.attacker_group.millitary)
        defenders = list(self.defender_group.millitary)

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


            self.tot_casualties = (len(self.attacker_group.millitary) - len(attackers)) + (len(self.defender_group.millitary) - len(defenders))

            if len(attackers) <= 0:
                self.combat_state = "defeat"
                self.modify_cities_temperament(self.attacker_group, -0.2)
                self.modify_cities_temperament(self.defender_group, 0.2)
            else:
                self.combat_state = "victory"
                self.modify_cities_temperament(self.defender_group, -0.2)
                self.modify_cities_temperament(self.attacker_group, 0.2)
                max_wealth_carry = len(attackers) * 10
                max_food_carry = len(attackers) * 5
                if self.defender_group.wealth > max_wealth_carry:
                    self.defender_group.wealth -= max_wealth_carry
                    self.attacker_group.wealth += max_wealth_carry
                else:
                    self.attacker_group.wealth += self.defender_group.wealth
                    self.defender_group.wealth = 0

                if self.defender_group.food > max_food_carry:
                    self.defender_group.food -= max_food_carry
                    self.attacker_group.food += max_food_carry
                else:
                    self.attacker_group.food += self.defender_group.food
                    self.defender_group.food = 0
        else:

            self.combat_state = "pillage"
            self.modify_cities_temperament(self.defender_group, -0.2)
            self.modify_cities_temperament(self.attacker_group, 0.2)
            max_wealth_carry = len(attackers) * 10
            max_food_carry = len(attackers) * 5
            if self.defender_group.wealth > max_wealth_carry:
                self.defender_group.wealth -= max_wealth_carry
                self.attacker_group.wealth += max_wealth_carry
            else:
                self.attacker_group.wealth += self.defender_group.wealth
                self.defender_group.wealth = 0

            if self.defender_group.food > max_food_carry:
                self.defender_group.food -= max_food_carry
                self.attacker_group.food += max_food_carry
            else:
                self.attacker_group.food += self.defender_group.food
                self.defender_group.food = 0

        self.log_encounter()

    def modify_cities_temperament(self, city, modifier=-0.3):
        citizens = [c for c in self.state.humanoids if c.home == city]
        for citizen in citizens:
            citizen.temperament = min(max(citizen.temperament + modifier, -1.0), 1.0)

    def log_encounter(self):
        if self.combat_state == "pillage":
            if ENABLE_CONSOLE:
                print("The city of {} ({}) PILLAGED the city of {} ({})!".format(
                    self.attacker_group.name, self.attacker_group.race, self.defender_group.name,
                    self.defender_group.race))
            if ENABLE_LOG:
                log_event(self.state.date,
                          "The city of {} ({}) PILLAGED the city of {} ({})!".format(
                              self.attacker_group.name, self.attacker_group.race, self.defender_group.name,
                              self.defender_group.race))


        elif self.combat_state == "victory":
            if ENABLE_CONSOLE:
                print("The city of {} ({}) is VICTORIOUS in battle against the city of {} ({}) - {} total casualties!".format(
                    self.attacker_group.name, self.attacker_group.race, self.defender_group.name,
                    self.defender_group.race, self.tot_casualties))
            if ENABLE_LOG:
                log_event(self.state.date,
                          "The city of {} ({}) is VICTORIOUS in battle against the city of {} ({}) - {} total casualties!".format(
                              self.attacker_group.name, self.attacker_group.race, self.defender_group.name,
                              self.defender_group.race, self.tot_casualties))
        elif self.combat_state == "defeat":
            if ENABLE_CONSOLE:
                print("The city of {} ({}) is DEFEATED in battle against the city of {} ({}) - {} total casualties!".format(
                    self.attacker_group.name, self.attacker_group.race, self.defender_group.name,
                    self.defender_group.race, self.tot_casualties))
            if ENABLE_LOG:
                log_event(self.state.date,
                          "The city of {} ({}) is DEFEATED in battle against the city of {} ({}) - {} total casualties!".format(
                              self.attacker_group.name, self.attacker_group.race, self.defender_group.name,
                              self.defender_group.race, self.tot_casualties))

    def combat_action(self, attacker, defender):
        if attacker != None and defender != None:
            dice = Dice()
            proficiency = get_modifier(attacker.attr_str)
            proficiency += 4 if attacker.desires_graph["violent"] else 2
            roll_bonus = 1 if self.attacker_group.is_blessed else 0
            roll_bonus += 2 if attacker.is_blessed else 0

            if dice.d20() + proficiency + roll_bonus > defender.armour_class: # Is Hit ?
                dmg = dice.d6() + proficiency
                defender.health = max(defender.health - dmg, 0) # Do Damage

