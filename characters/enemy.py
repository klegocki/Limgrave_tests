import random

from characters.character import Character


class Enemy(Character):

    def __init__(self, name, hp, strength, exp_reward):
        super().__init__(name, hp, 0, strength)
        self.exp_reward = exp_reward

    def perform_action(self, player):
        dmg = random.randint(1, self.strength)
        print(f" ! {self.name} attacks you for {dmg}!")
        player.take_damage(dmg)