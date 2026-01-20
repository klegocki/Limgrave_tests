from equipment.item import Item


class Weapon(Item):

    def __init__(self, name, value, damage, durability):
        super().__init__(name, value)
        self.damage = damage
        self.durability = durability

    def __str__(self):
        return f"{self.name} [Dmg: {self.damage}, Durability: {self.durability}]"

    def decrease_durability(self):
        self.durability -= 1
        if self.durability < 0: self.durability = 0