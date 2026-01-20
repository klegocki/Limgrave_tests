from equipment.weapon import Weapon


class Inventory:

    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f" + Added to inventory: {item.name}")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def get_any_weapon(self):
        for item in self.items:
            if isinstance(item, Weapon) and item.durability > 0:
                return item
        return None

    def show(self):
        if not self.items:
            print(" [Inventory is empty]")
        else:
            print(" --- Inventory ---")
            for idx, item in enumerate(self.items):
                print(f" {idx + 1}. {item}")