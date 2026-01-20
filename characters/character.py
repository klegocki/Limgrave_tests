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
