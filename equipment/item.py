class Item:

    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity

    def __str__(self):
        return f"{self.name} (Rarity: {self.rarity})"