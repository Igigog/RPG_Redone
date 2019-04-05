from random import randint
from lists import weapons, opponents, locations, armors, loot


class Mob:
    def __init__(self, self_list):
        self.weapon = weapons[0]
        self.equip = armors[0]
        self.name = self_list[0]
        self.starthealth = self_list[1]
        self.health = self_list[1]
        self.attack = self_list[2]
        self.armor = self_list[3]
        self.lvl = self_list[4]
        self.gold = self_list[5]
        self.crit = 1
        self.dodge = 1
        self.energy = 5

    def crit(self):
        critical = randint(1, 1000)
        if self.crit * 100.0 >= critical:
            return True
        else:
            return False

    def dodge(self):
        dodge_try = randint(1, 1000)
        if self.dodge * 100.0 >= dodge_try:
            return True
        else:
            return False

    def armor_stat(self, damage):
        if damage * 2 <= self.armor:
            return 0
        elif damage >= self.armor * 4:
            return damage - (self.armor // 2)
        else:
            return damage // 2 + 1


class Player(Mob):
    def __init__(self):
        self_list = ['player', 20, 1, 0, 1, 0]
        super().__init__(self_list)
        self.weapon = weapons[0]
        self.equip = armors[0]
        self.exp = 0
        self.wpninventory = [self.weapon]
        self.armorinventory = [self.equip]
        self.location = locations[0]
        self.garbageinv = []

    @classmethod
    def fibonacci(cls):
        x = 2
        y = 1
        while True:
            x, y = y, x+y
            yield y

    def search_treasure(self):
        summa = 0
        for x in range(1, len(loot) + 1):   # search for triangle num
            summa += x
        rand_ch = randint(1, summa)
        start_stat = 1
        for step in range(2, summa):           # summa = 1+2+3+4+...+n n=len(weapons)
            if rand_ch > start_stat:           # drop chance of last element = 1/summa etc.
                start_stat += step             # drop chance of reversed n'th element = n'th term/sum
            else:
                n = len(loot) - (step - 1)  # step starts from 2 therefore we need to subtract 1
                break
        self.garbageinv.append(loot[n])
        return loot[n][0]

    def find_opponent(self):
        enemy_list = []
        for x in opponents:
            if x[4] in range(self.location[1], self.location[1] + 2):
                enemy_list.append(x)
        num = randint(0, len(enemy_list) - 1)
        self.opponent = Mob(enemy_list[num])
        self.opponent.opponent = self

    def lvl_up(self):
        lvl = 1
        for x in self.fibonacci():
            if self.exp >= x:
                lvl += 1
            else:
                break
        self.lvl = lvl


def vivod(result):
    main_text = ''
    if not result:
        return 'Dodge! No damage dealt.\n'
    else:
        if result[2]:
            main_text += 'Critical strike! Damage doubled.\n'
        main_text += '%s deal %s damage to %s. %s is on %s hp.\n' % (
            result[0].name.title(), result[3], result[1].name, result[1].name.title(), result[1].health)
        return main_text


def attack(player):
    enemy = player.opponent
    player_damage = player.attack + player.weapon[1]

    if dodge(player):
        return False
    else:
        if crit(player):
            player_crit = True
            player_damage *= 2
        else:
            player_damage = armor_stat(enemy, player_damage)
            player_crit = False
        enemy.health -= player_damage
        if enemy.health < 1:
            enemy.health = 0
        return [player, enemy, player_crit, player_damage]


def pobeditel(player):
    if player.opponent.health < 1:
        return True
    elif player.health < 1:
        return False


def pobeg(player):
    if randint(1, 4) == 1:
        player.health = player.starthealth
        player.opponent = ''
        return True
    else:
        player.health -= player.opponent.attack
        return False


def win(player):
    startlvl = player.lvl
    win_text = 'Congratulations! You win!\nHealth restored\nExp +1\nGold + %s\n\n' % player.opponent.gold
    player.health = player.starthealth
    player.exp += 1
    player.energy = 5
    player.gold += player.opponent.gold
    player.opponent = ''
    player.lvl_up()
    if player.lvl > startlvl:
        win_text += 'Level up! Your lvl is now %s\n' % player.lvl
    return win_text
