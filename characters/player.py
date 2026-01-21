import random

from characters.character import Character
from equipment.inventory import Inventory
from equipment.weapon import Weapon


class Player(Character):

    def __init__(self, name, hp=100, mp=50, strength=10, max_mp=50, max_hp=100, experience=0):
        super().__init__(name, hp=hp, mp=mp, strength=strength, max_mp=max_mp, max_hp=max_hp, experience=experience)
        self.inventory = Inventory()
        self.equipped_weapon = None
        self.spells = []

    def equip(self, weapon):

        if isinstance(weapon, Weapon):
            self.equipped_weapon = weapon
            print(f" > Equipped: {weapon.name}")

    def learn_spell(self, spell):
        if not spell in self.spells:
            self.spells.append(spell)
            print(f" + Learned spell: {spell.name}")
        else:
            print(f" > Spell already taught: {spell.name}")

    def show_spells(self):
        if not self.spells:
            print(" [Spellbook is empty]")
        else:
            print(" --- Spellbook ---")
            for idx, spell in enumerate(self.spells):
                print(f"{idx + 1}. {spell.name} (Cost: {spell.cost} MP, Dmg: ~{spell.damage})")

    def check_weapon_status(self):
        if self.equipped_weapon and self.equipped_weapon.durability <= 0:
            print(f" !!! Your {self.equipped_weapon.name} shattered into pieces! !!!")
            self.inventory.remove_item(self.equipped_weapon)
            self.equipped_weapon = None

            new_weapon = self.inventory.get_any_weapon()
            if new_weapon:
                self.equip(new_weapon)
            else:
                print(" > You have no weapons left! You found a backup Rusted Sword.")
                backup = Weapon("Rusted Sword", 1, 6, 20)
                self.inventory.add_item(backup)
                self.equip(backup)

    def attack(self, target):
        base_dmg = random.randint(1, self.strength)
        weapon_dmg = 0

        if self.equipped_weapon:
            if self.equipped_weapon.durability > 0:
                weapon_dmg = self.equipped_weapon.damage
                self.equipped_weapon.decrease_durability()
            else:
                print(f" ! Your {self.equipped_weapon.name} is broken and useless!")

        total_dmg = base_dmg + weapon_dmg
        print(f" > You attack {target.name} for {total_dmg} damage!")
        target.take_damage(total_dmg)
        self.mp = min(self.max_mp, self.mp + 5)
