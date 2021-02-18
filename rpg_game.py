import sys
import time
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, hp, mp, atk, df, magic):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.action = ["attack", "magic"]

    def gen_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
            return self.hp

    def heal(self, dmg):
        self.hp += dmg

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("Actions")
        for item in self.actions:
            print(str(i) + ":", item)
            i += 1


    def choose_magic(self):
        i = 1
        print("________________________")
        print(bcolors.OKBLUE + bcolors.BOLD + "Magic" + bcolors.ENDC +
        " (" + bcolors.FAIL + bcolors.BOLD + "RED" + bcolors.ENDC + " = damage spells;" + bcolors.OKGREEN + bcolors.BOLD +
        " YELLOW" + bcolors.ENDC + " = cure spells;" + bcolors.OKBLUE + bcolors.BOLD + " BLUE" + bcolors.ENDC + " special spells)\n")

        for spell in self.magic:

            if spell.type == "black":
                print(str(i) + ": " + bcolors.FAIL + str(spell.name) + bcolors.ENDC + str(" (Cost: " + str(spell.cost) + ", " + "damage: " + str(spell.dmg) + ")\n"))
                i += 1

            if spell.name == "balance":
                print(str(i) + ": " + bcolors.OKGREEN + str(spell.name) + bcolors.ENDC + str(
                    " (Cost: " + str(spell.cost) + ", " + "Ability: enemies HP = Players HP, effectiveness varies)\n"))
                i += 1

            if spell.name == "trade":
                print(str(i) + ": " + bcolors.OKGREEN + str(spell.name) + bcolors.ENDC + str(
                    " (Cost: " + str(spell.cost) + ", " + "Ability: trade 80 HP for 30 MP)\n"))
                i += 1

            if spell.type == "white":
                print(str(i) + ": " + bcolors.OKBLUE + str(spell.name) + bcolors.ENDC + str(
                    " (Cost: " + str(spell.cost) + ", " + "Heal: " + str(spell.dmg) + ")\n"))
                i += 1


class spell:
    def __init__(self, name, cost, dmg, type):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type

    def generate_dmg(self):
        low = self.dmg - 15
        high = self.dmg + 15
        return random.randrange(low, high)

def sprint(str):
    for c in str + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(5. / 100)

blizzard = spell("blizzard", 8, 75, "black")
fire = spell("fire", 10, 110, "black")
thunder = spell("thunder", 15, 160, "black")
quake = spell("quake", 14, 132, "black")
meteor = spell("meteor", 20, 205, "black")
gravity = spell("gravity", 35, 340, "black")

balance = spell("balance", 40, 0, "special")
trade = spell("trade", 0, 0, "special")

cure = spell("cure", 12, 120, "white")
cura = spell("cura", 18, 200, "white")


running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "An enemy attacks !!!" + bcolors.ENDC)

level = int(input("choose difficulty: easy - 1, medium - 2, hard - 3"))

if level == 1:
    player = Person(550, 65, 55, 40, [fire, thunder, blizzard, meteor, quake, gravity, balance, trade, cure, cura])
    enemy = Person(1000, 65, 65, 45, [])

if level == 2:
    player = Person(500, 50, 60, 30, [fire, thunder, blizzard, meteor, quake, gravity, balance, trade, cure, cura])
    enemy = Person(1100, 70, 70, 65, [])

if level == 3:
    player = Person(450, 35, 50, 10, [fire, thunder, blizzard, meteor, quake, gravity, balance, trade, cure, cura])
    enemy = Person(1300, 100, 90, 70, [])

while running:
    sprint("==============")
    sprint(bcolors.OKBLUE + "Actions" + bcolors.ENDC)
    sprint("1: attack")
    sprint("2: magic")
    choice = input("choose action:")
    index = int(choice) - 1
    enemy_choice = random.randint(1, 2)
    enemy_dmg = enemy.gen_damage()


    if index == 0:
       dmg = player.gen_damage()
       enemy.take_dmg(dmg)
       print(bcolors.OKBLUE + "\nyou attacked for", dmg, "points of damage, Enemy HP:", enemy.get_hp(), bcolors.ENDC)
       player.take_dmg(enemy_dmg)
       print(bcolors.FAIL + "\nEnemy attacks for", enemy_dmg,
             "points of damage" + ", player hp:", player.get_hp(), bcolors.ENDC)

    elif index == 1:
        player.choose_magic()

        magic_choice = int(input("Choose Magic:")) - 1
        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_dmg()
        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_dmg()
        current_mp = player.get_mp()

        if spell.cost > current_mp:
            sprint(bcolors.FAIL + '\n Not Enough MP' + bcolors.ENDC)
            continue

        player.reduce_mp(spell.cost)

        if spell.type == "white":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            player.take_dmg(enemy_dmg)
            print(bcolors.FAIL + "\nEnemy attacks for", enemy_dmg,
                  "points of damage" + ", player hp:", player.get_hp(), bcolors.ENDC)

        elif spell.type == "black":
            enemy.take_dmg(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)
            player.take_dmg(enemy_dmg)
            print(bcolors.FAIL + "\nEnemy attacks for", enemy_dmg,
                  "points of damage" + ", player hp:", player.get_hp(), bcolors.ENDC)

        elif spell.name == "balance":
            enemy.hp = player.get_hp()
            player.hp = player.hp - random.randint(0, 15)
            effic = round((player.hp / enemy.hp) * 100)
            print(bcolors.OKBLUE + "\n" + spell.name +
                  " has equilibrated both yours and enemies HP, balance spell effectiveness = " + str(effic) + "%" + bcolors.ENDC)

        elif spell.name == "trade":
            player.hp -= 80
            player.mp += 30
            print(bcolors.OKBLUE + "\n" + spell.name + " has taken 80 HP in return for 30 MP" + bcolors.ENDC)
            player.take_dmg(enemy_dmg)
            print(bcolors.FAIL + "\nEnemy attacks for", enemy_dmg,
                  "points of damage" + ", player hp:", player.get_hp(), bcolors.ENDC)


    print("----------------------------------------------------------")
    print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC + "\n")
    print("Your HP:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC + "\n")
    print("Your MP:", bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_mp()) + bcolors.ENDC + "\n")

    if player.get_hp() == 0 and enemy.get_hp() == 0:
        sprint(bcolors.OKGREEN + 'TIE' + bcolors.ENDC)
        running = False

    elif enemy.get_hp() == 0:
        sprint(bcolors.OKBLUE + 'YOU WIN' + bcolors.ENDC)
        running = False

    elif player.get_hp() == 0:
        sprint(bcolors.FAIL + 'YOU LOSE' + bcolors.ENDC)
        running = False




