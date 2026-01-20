from equipment.item import Item


class Potion(Item):

    def __init__(self, name, value, heal_amount):
        super().__init__(name, value)
        self.heal_amount = heal_amount

    def use(self, character):
        character.heal(self.heal_amount)
        print(f" > Drank {self.name}. Healed {self.heal_amount} HP.")