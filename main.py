import random
import time

class Item:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name} (Value: {self.value})"


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


class Potion(Item):

    def __init__(self, name, value, heal_amount):
        super().__init__(name, value)
        self.heal_amount = heal_amount

    def use(self, character):
        character.heal(self.heal_amount)
        print(f" > Drank {self.name}. Healed {self.heal_amount} HP.")


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


class Character:

    def __init__(self, name, hp, mp, strength):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.strength = strength
        self.experience = 0

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0: self.hp = 0
        print(f" - {self.name} takes {dmg} damage! (HP: {self.hp}/{self.max_hp})")

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp: self.hp = self.max_hp

    def gain_experience(self, exp):
        self.experience += exp
        print(f" + Gained {exp} XP (Total: {self.experience}/100)")
        if self.experience >= 100:
            print(f" *** LEVEL UP! {self.name} is stronger! ***")
            self.max_hp += 10
            self.hp = self.max_hp
            self.max_mp += 5
            self.mp = self.max_mp
            self.strength += 2
            self.experience -= 100


class Player(Character):

    def __init__(self, name):
        super().__init__(name, hp=100, mp=50, strength=10)
        self.inventory = Inventory()
        self.equipped_weapon = None
        self.spells = []

    def equip(self, weapon):
        if isinstance(weapon, Weapon):
            self.equipped_weapon = weapon
            print(f" > Equipped: {weapon.name}")

    def learn_spell(self, spell):
        self.spells.append(spell)
        print(f" + Learned spell: {spell.name}")

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
                backup = Weapon("Rusted Sword", 0, 5, 15)
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


class Enemy(Character):

    def __init__(self, name, hp, strength, exp_reward):
        super().__init__(name, hp, 0, strength)
        self.exp_reward = exp_reward

    def perform_action(self, player):
        dmg = random.randint(1, self.strength)
        print(f" ! {self.name} attacks you for {dmg}!")
        player.take_damage(dmg)



class BattleSystem:

    def __init__(self):
        self.turn_count = 0

    def start_battle(self, player, enemy):
        self.turn_count = 0
        print(f"\n--- BATTLE STARTED: {player.name} vs {enemy.name} ---")

        while player.is_alive() and enemy.is_alive():
            self.turn_count += 1
            print(f"\n--- Turn {self.turn_count} ---")
            print(f"[{player.name}: HP {player.hp}/{player.max_hp} | MP {player.mp}/{player.max_mp}]")
            print(f"[Enemy: {enemy.name} HP {enemy.hp}]")

            print("1. Attack (Regen 5 MP)")
            print("2. Magic")
            choice = input("Action: ")

            turn_ended = False

            match choice:
                case "1":
                    player.attack(enemy)
                    turn_ended = True

                case '2':
                    if not player.spells:
                        print("You don't know any spells!")
                    else:
                        player.show_spells()
                        try:
                            s_idx = int(input("Select spell (0 to cancel): "))
                            if 0 < s_idx <= len(player.spells):
                                success = player.spells[s_idx - 1].cast(player, enemy)
                                if success:
                                    turn_ended = True
                        except ValueError:
                            print("Invalid selection.")
                case _:
                    print("Invalid command.")

            if turn_ended:
                if enemy.is_alive():
                    time.sleep(0.5)
                    enemy.perform_action(player)
                else:
                    print(f"\n *** VICTORY! You defeated {enemy.name}! ***")
                    player.gain_experience(enemy.exp_reward)
                    player.check_weapon_status()

                    if random.choice([True, False]):

                        sword_type = random.choice([
                            ("Broadsword", 10, 10, 30),
                            ("Greatsword", 10, 25, 25),
                            ("Bloodhound's curved sword", 10, 20, 20),
                            ("Uchikatana", 10, 15, 20),
                            ("Axe", 10, 12, 20)
                        ])
                        sword = Weapon(sword_type[0], sword_type[1], sword_type[2], durability=sword_type[3])
                        player.inventory.add_item(sword)
                        print(f"You acquired: {sword.name}!")

                    return True

            if not player.is_alive():
                print("\n *** YOU DIED ***")
                return False
        return False


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
                ("Knight", 50, 7, 15),
                ("Rune Bear", 100, 10, 25),
                ("Skeleton", 25, 6, 10),
                ("Wolf", 20, 3, 10),
                ("Bell bearing hunter (Boss)", 200, 15, 100)
            ])

            if "Boss" in enemy_type[0]:
                if not self.did_boss_appear:
                    enemy = Enemy(enemy_type[0], enemy_type[1], enemy_type[2], enemy_type[3])
                    self.did_boss_appear = True
                    self.BattleSystem.start_battle(self.player, enemy)
                else:
                    std_enemy = random.choice([
                        ("Knight", 30, 4, 15),
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
                    item.use(self.player)
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


if __name__ == "__main__":
    game = Game()
    game.start()