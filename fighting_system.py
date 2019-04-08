from collections import namedtuple
from random import randint
from database_values import weapons, enemies, locations, armors, loots


class Mob:
    def __init__(self, self_list):
        self._weapon = weapons['Nothing']
        self._equip = armors['Nothing']
        self.name = self_list[0]
        self.starthealth = self_list[1]
        self._health = self_list[1]
        self.attack_stat = self_list[2]
        self.armor_stat = self_list[3]
        self.lvl = self_list[4]
        self.gold = self_list[5]
        self.crit_chance = 1
        self.dodge_chance = 1
        self.energy = 5

    # SETTING PROPERTIES

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value < 1:
            self._health = 0
        self._health = value

    @property
    def equip(self):
        return self._equip

    @equip.setter
    def equip(self, value):
        self._equip = value
        self.dodge_chance = value.dodge
        self.armor_stat = value.main_stat

    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, value):
        self._weapon = value
        self.crit_chance = 1 + value.crit

    # FIGHT FUNCTIONS

    def crit(self):
        critical = randint(1, 1000)
        if self.crit_chance * 100.0 >= critical:
            return True
        else:
            return False

    def dodge(self):
        dodge_try = randint(1, 1000)
        if self.dodge_chance * 100.0 >= dodge_try:
            return True
        else:
            return False

    def armor_resist(self, damage):
        if damage * 2 <= self.armor_stat:
            return 0
        elif damage >= self.armor_stat * 4:
            return damage - (self.armor_stat // 2)
        else:
            return damage // 2 + 1


class Player(Mob):
    def __init__(self):
        self_list = ['player', 20, 1, 0, 1, 0]
        super().__init__(self_list)
        self.exp = 0
        self.wpninventory = [self.weapon]
        self.armorinventory = [self.equip]
        self.location = locations['Starting Village']
        self.garbageinv = []

    # makes new player
    def reset(self):
        self.__init__()

    # for lvl checks
    @staticmethod
    def fibonacci(n):
        x = 2
        y = 1
        for _ in range(n-1):
            x, y = y, x+y
        return y

    def search_treasure(self):
        item_rarity = randint(0, 1000)
        rarity_relations = {0: 1,
                            301: 2,
                            601: 3,
                            801: 4,
                            951: 5,
                            }

        for k in rarity_relations.keys():
            if item_rarity > k:
                rarity = rarity_relations[k]

        items = tuple(filter(
            lambda x: x.rarity == rarity,
            loots.values()))
        item = items[randint(0, len(items)-1)]

        self.garbageinv.append(item)
        return item.name

    # FIGHT FUNCTIONS

    def find_opponent(self):

        enemy_list = []
        for enemy in enemies.values():
            if enemy.lvl in range(self.location.lvl, self.location.lvl + 2):
                enemy_list.append(enemy)

        num = randint(0, len(enemy_list) - 1)
        return Mob(enemy_list[num])

    def eat_opponent(self, opponent):
        self.health = self.starthealth
        self.exp += 1
        self.energy = 5
        self.gold += opponent.gold
        self.lvl_up()

    def lvl_up(self):
        if self.fibonacci(self.lvl + 1) <= self.exp:
            print(self.fibonacci(self.lvl + 1), ': ', self.exp)
            self.lvl += 1
            self.lvl_up()
            return True
        else:
            return False


class Fight:
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent
        self.Result = namedtuple(
            'Result', 'attacker defender dodge player_crit player_damage')

    # MAIN FIGHT FUNCTION
    def fight_step(self):
        """ Do every fight activities and return result text """
        outcome = ''

        fight_result = self.Result(*self.attack(self.player, self.opponent))
        outcome += self.vivod(fight_result)

        fight_result = self.Result(*self.attack(self.opponent, self.player))
        outcome += self.vivod(fight_result) + '\n\n'

        if self.is_won():
            outcome += self.win_activities()
        return outcome

    # FUNCTIONS USED BY fight_step()

    def attack(self, attacker, defender):
        player_damage = self.player.attack_stat + self.player.weapon.main_stat
        dodge = False
        if defender.dodge():
            dodge = True
            player_damage = 0

        if attacker.crit():
            player_crit = True
            player_damage *= 2
        else:
            player_damage = self.opponent.armor_resist(player_damage)
            player_crit = False

        defender.health -= player_damage
        if defender.health < 1:
            defender.health = 0

        statist = (attacker, defender, dodge, player_crit, player_damage)
        return statist

    def escape(self):
        if randint(1, 4) == 1:
            self.player.health = self.player.starthealth
            return True
        else:
            self.player.health -= self.opponent.attack_stat
            return False

    @staticmethod
    def vivod(fight_result):
        """ Return text of one attack """
        main_text = ''
        if fight_result.dodge:
            return 'Dodge! No damage dealt.\n'
        else:
            if fight_result.player_crit:
                main_text += 'Critical strike! Damage doubled.\n'
            main_text += f'{fight_result.attacker.name.title()} ' \
                f'deal {fight_result.player_damage} damage ' \
                f'to {fight_result.defender.name}. ' \
                f'{fight_result.defender.name.title()} is ' \
                f'on {fight_result.defender.health} hp.\n'
            return main_text

    def is_won(self):
        if self.opponent.health < 1:
            return True
        elif self.player.health < 1:
            return False

    def win_activities(self):
        """ Do everything needed to end fight """
        self.player.eat_opponent(self.opponent)
        win_text = f'Congratulations! You win!\n' \
                   f'Health restored\nExp +1\n' \
                   f'Gold + {self.opponent.gold}\n\n'
        if self.player.lvl_up():
            win_text += f'Level up! Your lvl is now {self.player.lvl}\n'
        return win_text
