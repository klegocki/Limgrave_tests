import random
import time

from equipment.weapon import Weapon
from game.database import Database


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
                            ("Broadsword", 3, 10, 30),
                            ("Greatsword", 5, 25, 25),
                            ("Bloodhound's curved sword", 6, 20, 20),
                            ("Uchikatana", 4, 15, 20),
                            ("Axe", 2, 12, 20)
                        ])
                        sword = Weapon(sword_type[0], sword_type[1], sword_type[2], sword_type[3])
                        player.inventory.add_item(sword)
                        print(f"You acquired: {sword.name}!")

                    return True

            if not player.is_alive():
                with Database("player_save.db") as db:
                    db.delete_save_file(player.name)

                print("\n *** YOU DIED ***")
                return False
        return False
