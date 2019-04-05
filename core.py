import sys
from PyQt5.QtWidgets import QApplication
from GUI import App
from fighting_system import *
from database_values import buttons as buttons_dict


def update_stats():
    app.statlabel.setText(f'LVL: {player.lvl}\n'
                          f'EXP: {player.exp}\n'
                          f'ATK: {(player.attack + player.weapon[1])}\n'
                          f'DEF: {player.armor}\n'
                          f'ARM: {player.equip[0]}\n'
                          f'WPN: {player.weapon[0]}\n'
                          f'GOLD: {player.gold}')


def game_start():
    """ Hide start buttons and start mainloop """
    global player
    player = Player()

    app.label.setText('Now the Game begins!\n\n')
    app.switch_mode('main')


def load_clicked():
    global player
    player = Player()

    new_player = Player()
    new_player.wpninventory.clear()
    new_player.armorinventory.clear()
    new_player.weapon = []
    new_player.equip = []

    try:
        f = open('save.txt', 'r')
    except FileNotFoundError:
        app.label.setText('There is no saves!')
        return False

    try:
        for step in range(3):
            line = f.readline().replace('\n', '').split(' ')
            line.remove('')
            for x in line:
                x = int(x)
                if step == 0:
                    new_player.wpninventory.append(weapons[x])
                elif step == 1:
                    new_player.armorinventory.append(armors[x])
                elif step == 2:
                    new_player.garbageinv.append(loot[x])

        stats = f.readline().split(' ')
        new_player.exp = int(stats[0])
        new_player.armor = int(stats[1])
        new_player.gold = int(stats[2])
        new_player.weapon = weapons[int(stats[3])]
        new_player.equip = armors[int(stats[4])]
        new_player.lvl_up()
    except (ValueError, IndexError):
        app.label.setText('Save corrupted')
        return False

    player = new_player
    app.label.setText('Load successful')
    app.mode_switch('main')


def save_clicked():
    with open('save.txt', 'w') as f:
        for x in player.wpninventory:
            f.write('%s ' % x[5])
        f.write('\n')
        for x in player.armorinventory:
            f.write('%s ' % x[5])
        f.write('\n')
        for x in player.garbageinv:
            f.write('%s ' % x[3])
        f.write('\n')
        f.write('%s %s %s %s %s' % (player.exp, player.armor, player.gold, player.weapon[5], player.equip[5]))
        app.label.setText('Save successful')


def find_clicked():
    player.find_opponent()
    app.switch_mode('fight')
    app.label.setText('Your opponent is %s\n\n' % player.opponent.name)


def search_clicked():
    app.label.clear()
    if randint(1, 10) < 3:
        find_clicked()
    elif player.energy:
        x = player.search_treasure()
        app.label.insert_text('You found %s\n' % x)
        player.energy -= 1
    else:
        app.label.insert_text('No energy\n')


def inv_clicked():
    app.armorbox.clear()
    app.wpnbox.clear()
    app.label.setText('You weapon is %s\n' % player.weapon[0])
    app.label.insert_text('You armor is %s\n\n' % player.equip[0])
    for x in player.wpninventory:
        app.wpnbox.addItem(x[0])
    for x in player.armorinventory:
        app.armorbox.addItem(x[0])
    app.switch_mode('inventory')


def change_armor():
    for x in player.armorinventory:
        if x[0] == app.armorbox.currentText():
            player.equip = x
            player.armor = x[1]
            player.dodge = x[2]
            break
    app.label.insert_text('You armor is %s\n\n' % player.equip[0])


def change_weapon():
    for x in player.wpninventory:
        if x[0] == app.wpnbox.currentText():
            player.weapon = x
            player.crit = player.weapon[2]
            break
    app.label.insert_text('You weapon is %s\n\n' % player.weapon[0])


def win_check():
    if pobeditel(player):
        app.switch_mode('main')
        app.label.insert_text(win(player))
    elif pobeditel(player) is None:
        pass
    else:
        app.label.insert_text('You lose! Try again next time!')
        app.switch_mode('dead')


def atk_clicked():
    player_atk = attack(player)
    enemy_atk = attack(player.opponent)
    app.label.insert_text(vivod(player_atk) + vivod(enemy_atk) + '\n\n')
    win_check()


def heavy_atk_clicked():
    player_atk = heavy_attack(player)
    enemy_atk = attack(player.opponent)
    app.label.insert_text(vivod(player_atk) + vivod(enemy_atk) + '\n\n')
    win_check()


def esc_clicked():
    if pobeg(player):
        app.label.insert_text('You escaped c:\n\n')
        app.switch_mode('main')
    else:
        app.label.insert_text('Escape failed :c\nYou get %s damage\n\n' % player.opponent.attack)
        if player.health < 1:
            app.label.insert_text('You lose! Try again next time!')
            app.switch_mode('dead')


def map_clicked():
    app.mapbox.clear()
    app.label.setText('Your location is %s\n\n' % player.location[0])
    for loc in locations:
        app.mapbox.addItem(loc[0])
    app.switch_mode('map')


def change_loc():
    for loc in locations:
        if app.mapbox.currentText() == loc[0]:
            player.location = loc
            break
    app.label.insert_text('Your location is %s\n\n' % player.location[0])


def weapons_market():
    app.marketbox.clear()
    app.label.clear()
    for x in weapons:
        if x[3] in range(player.location[1], player.location[1] + 3):
            app.marketbox.addItem(x[0])
            app.label.insert_text('%s  ATK:%s  COST:%s\n' % (x[0], x[1], x[4]))
    app.label.insert_text('\n')


def armor_market():
    app.marketbox.clear()
    app.label.clear()
    for x in armors:
        if x[3] in range(player.location[1], player.location[1] + 3):
            app.marketbox.addItem(x[0])
            app.label.insert_text('%s  DEF:%s  COST:%s\n' % (x[0], x[1], x[4]))
    app.label.insert_text('\n')


def enter_market():
    app.switch_mode('market')
    weapons_market()


def buy_clicked():
    tab_indexes = {0: weapons, 1: armors}

    current_list = list(tab_indexes[app.markettab.currentIndex()])  # just making a copy
    current_list.pop(0)                     # removes Nothing
    current_list = list(filter(
        lambda x: x[3] in range(player.location[1], player.location[1] + 3),
        current_list))  # filter by location lvl

    item = current_list[app.marketbox.currentIndex()]
    if player.gold < item[4]:
        app.label.insert_text('Not enough gold.\n\n')
        return False

    elif item in player.wpninventory or item in player.armorinventory:
        app.label.insert_text('%s is already yours' % item[0])
        return False

    else:
        if app.markettab.currentIndex():
            player.wpninventory.append(item)
        else:
            player.armorinventory.append(item)
        player.gold -= item[4]
        app.label.insert_text('%s in now yours.\n' % item[0])
        return True


def sell_clicked():
    summa = 0
    if not player.garbageinv:
        app.label.insert_text('No garbage.\n\n')
        return False
    for x in range(len(player.garbageinv)):
        summa += player.garbageinv[0][1]
        player.garbageinv.pop(0)
    player.gold += summa
    app.label.insert_text('Garbage sold. You get %s gold.\n\n' % summa)


def change_market_mode():
    if app.markettab.currentIndex():
        armor_market()
    else:
        weapons_market()


def connect_buttons():
    """connect all buttons from GUI with functions"""

    for button in buttons_dict:
        exec(f'app.{button}.clicked.connect({buttons_dict[button].func})')
    app.markettab.currentChanged.connect(change_market_mode)
    app.label.textChanged.connect(update_stats)


if __name__ == '__main__':
    game = QApplication(sys.argv)
    app = App()

    connect_buttons()
    sys.exit(game.exec_())
