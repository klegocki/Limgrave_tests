class Item:

    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity

    def __str__(self):
        return f"{self.name} (Rarity: {self.rarity})"

    def to_dict(self):
        return {"type": "Item", "name": self.name, "rarity": self.rarity}