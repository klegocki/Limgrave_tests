import random


class Spell:

    def __init__(self, name, cost, damage):
        self.name = name
        self.cost = cost
        self.damage = damage

    def cast(self, caster, target):
        if caster.mp >= self.cost:
            caster.mp -= self.cost
            dmg = random.randint(self.damage - 2, self.damage + 2)
            print(f" *** {caster.name} casts {self.name}! (Dmg: {dmg}) ***")
            target.take_damage(dmg)
            return True
        else:
            print(f" ! Not enough MP for {self.name}! (Cost: {self.cost}, You have: {caster.mp})")
            return False