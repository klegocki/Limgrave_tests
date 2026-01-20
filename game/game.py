import random
import time

from characters.enemy import Enemy
from characters.player import Player
from equipment.potion import Potion
from equipment.spell import Spell
from equipment.weapon import Weapon
from game.battle_system import BattleSystem


class Game:

    def __init__(self):
        self.BattleSystem = BattleSystem()
        self.player = None
        self.running = True
        self.did_boss_appear = False

    def start(self):
        print("Welcome to Limgrave!")
        name = input("Enter your character's name: ")
        self.player = Player(name)

        sword = Weapon("Rusted Sword", 10, 6, durability=20)
        self.player.inventory.add_item(sword)
        self.player.equip(sword)
        self.player.inventory.add_item(Potion("Flask of Crimson Tears", 5, 30))

        fireball = Spell("Fireball", cost=15, damage=25)
        self.player.learn_spell(fireball)

        while self.running and self.player.is_alive():
            self.main_menu()

    def main_menu(self):
        print("\n--- MAIN MENU ---")
        print("1. Explore")
        print("2. Manage Inventory")
        print("3. Show Spellbook")
        print("4. Character Stats")
        print("5. Quit Game")

        choice = input("Choice: ")

        match choice:
            case "1":
                self.explore()

            case "2":
                self.manage_inventory()

            case "3":
                self.player.show_spells()

            case "4":
                p = self.player
                w = p.equipped_weapon.name if p.equipped_weapon else "None"
                print(
                    f"\n[Name: {p.name}]\n[HP: {p.hp}/{p.max_hp}]\n[MP: {p.mp}/{p.max_mp}]\n[XP: {p.experience}/100]\n[Weapon: {w}]")

            case "5":
                print("Farewell, Tarnished!")
                self.running = False

            case _:
                print("Unknown command.")

    def explore(self):
        print("\nYou venture into the mist...")
        time.sleep(1)

        if random.randint(1, 10) > 3:
            enemy_type = random.choice([
                ("Soldier of Godrick", 50, 7, 15),
                ("Rune Bear", 100, 10, 25),
                ("Skeleton", 25, 6, 10),
                ("Wolf", 20, 3, 10),
                ("Bell bearing hunter (Boss)", 200, 20, 100)
            ])

            if "Boss" in enemy_type[0]:
                if not self.did_boss_appear:
                    enemy = Enemy(enemy_type[0], enemy_type[1], enemy_type[2], enemy_type[3])
                    self.did_boss_appear = True
                    self.BattleSystem.start_battle(self.player, enemy)
                else:
                    std_enemy = random.choice([
                        ("Soldier of Godrick", 30, 4, 15),
                        ("Rune Bear", 60, 10, 25),
                        ("Skeleton", 25, 5, 10),
                        ("Wolf", 20, 5, 10),
                    ])
                    enemy = Enemy(std_enemy[0], std_enemy[1], std_enemy[2], std_enemy[3])
                    self.BattleSystem.start_battle(self.player, enemy)
            else:
                enemy = Enemy(enemy_type[0], enemy_type[1], enemy_type[2], enemy_type[3])
                self.BattleSystem.start_battle(self.player, enemy)
        else:
            print("You found a Site of Grace. You rest for a moment.")
            if random.randint(1, 10) > 7:
                spell_chosen = False
                while len(self.player.spells) < 6 and not spell_chosen :
                    spell_to_add = random.choice([
                        Spell("Glintstone Pebble", 5, 12),
                        Spell("Lightning Strike", 25, 45),
                        Spell("Black Flame", 22, 38),
                        Spell("Briars of Sin", 20, 35),
                        Spell("Holy Light", 15, 22),
                    ])
                    known_spells = [s.name for s in self.player.spells]

                    if spell_to_add.name in known_spells:
                        continue
                    else:
                        self.player.spells.append(spell_to_add)
                        print(f"You found a spell called {spell_to_add.name}!")
                        spell_chosen = True

            self.player.hp = self.player.max_hp
            self.player.mp = self.player.max_mp
            crimson_flask_in_inventory = False

            for item in self.player.inventory.items:
                if isinstance(item, Potion) and item.name == "Flask of Crimson Tears":
                    crimson_flask_in_inventory = True
                    break

            if not crimson_flask_in_inventory:
                self.player.inventory.add_item(Potion("Flask of Crimson Tears", 5, 30))

    def manage_inventory(self):

        self.player.inventory.show()
        print("Press 'p' for potion, 'e' to equip weapon, or Enter to go back.")
        dec = input("Choice: ")

        if dec.lower() == 'p':
            for item in self.player.inventory.items:
                if isinstance(item, Potion):
                    item.use_potion(self.player)
                    self.player.inventory.remove_item(item)
                    return
            print("No potions!")

        elif dec.lower() == 'e':
            idx = int(input("Item number: ")) - 1
            if 0 <= idx < len(self.player.inventory.items):
                if not self.player.equipped_weapon == self.player.inventory.items[idx] and not isinstance(self.player.inventory.items[idx], Potion):
                    self.player.equip(self.player.inventory.items[idx])
                else:
                    print("You can't equip that or you already equipped.!")