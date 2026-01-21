from equipment.item import Item


class Weapon(Item):

    def __init__(self, name, rarity, damage, durability):
        super().__init__(name, rarity)
        self.damage = damage
        self.durability = durability


    def __str__(self):
        return f"{self.name} [Dmg: {self.damage}, Durability: {self.durability}]"


    def decrease_durability(self):
        self.durability -= 1


    def to_dict(self):
        return {
            "type": "Weapon",
            "name": self.name,
            "rarity": self.rarity,
            "damage": self.damage,
            "durability": self.durability
        }