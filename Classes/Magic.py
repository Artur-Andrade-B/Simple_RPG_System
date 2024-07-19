import random


class spell:
    def __init__(self, name, cost, dmg, type):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type

    def generate_damage(self):
        ldmg = self.dmg - 10
        hdmg = self.dmg + 20
        return random.randrange(ldmg, hdmg)
