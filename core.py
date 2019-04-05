import sys
import pickle
from PyQt5.QtWidgets import QApplication
from GUI import App
from fighting_system import *
from database_values import buttons as buttons_dict

class Game:

    def __init__(self):
        global app
        app = App()
        self.game = QApplication(sys.argv)

        global player
        player = Player()

        global buttons
        buttons = app.elements

    def connect_buttons(self):
        """connect all buttons from GUI with functions"""

        for button in buttons_dict:
            if buttons_dict[button].func[:6] == 'lambda':
                exec(f'app.{button}.clicked.connect({buttons_dict[button].func})')
        app.markettab.currentChanged.connect(self.change_market_mode)
        app.label.textChanged.connect(self.update_stats)

    @staticmethod
    def update_stats():
        app.statlabel.setText(f'LVL: {player.lvl}\n'
                              f'EXP: {player.exp}\n'
                              f'ATK: {(player.attack + player.weapon[1])}\n'
                              f'DEF: {player.armor}\n'
                              f'ARM: {player.equip[0]}\n'
                              f'WPN: {player.weapon[0]}\n'
                              f'GOLD: {player.gold}')

    def start(self):
        self.connect_buttons()
        sys.exit(self.game.exec_())

    @App.buttonfunction(buttons['loadbtn'])
    def load_clicked():
        player.reset()

        try:
            with open('database/save.pickle', 'rb') as player_savefile:
                global player
                player = pickle.load(player_savefile)
        except EnvironmentError:
            app.label.setText('Save corrupted\n\n')
            return
        else:
            app.label.setText('Load successful')
            app.mode_switch('main')

    @App.buttonfunction(buttons['savebtn'])
    def save_clicked():
        try:
            with open('database/save.pickle', 'wb') as savefile:
                pickle.dump(player, savefile)
        except EnvironmentError:
            app.main_label.setText('Something went wrong')
        else:
            app.main_label.setText('Save successful')

    @App.buttonfunction(buttons['fndbtn'])
    def find_clicked():
        player.find_opponent()
        app.switch_mode('fight')
        app.label.setText(f'Your opponent is {player.opponent.name}\n\n')

    @App.buttonfunction(buttons['srbtn'], static=False)
    def search_clicked(self):
        app.label.clear()
        if randint(1, 10) < 3:
            self.find_clicked()
        elif player.energy:
            x = player.search_treasure()
            app.label.insert_text('You found %s\n' % x)
            player.energy -= 1
        else:
            app.label.insert_text('No energy\n')

    @App.buttonfunction(buttons['invbtn'])
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

    @App.buttonfunction(buttons['cngarmorbtn'])
    def change_armor():
        for x in player.armorinventory:
            if x[0] == app.armorbox.currentText():
                player.equip = x
                player.armor = x[1]
                player.dodge = x[2]
                break
        app.label.insert_text(f'You armor is {player.equip[0]}\n\n')

    @App.buttonfunction(buttons['cngwpnbtn'])
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

    @App.buttonfunction(buttons['atkbtn'])
    def atk_clicked():
        player_atk = attack(player)
        enemy_atk = attack(player.opponent)
        app.label.insert_text(vivod(player_atk) + vivod(enemy_atk) + '\n\n')
        win_check()

    @App.buttonfunction(buttons['escbtn'])
    def esc_clicked():
        if pobeg(player):
            app.label.insert_text('You escaped c:\n\n')
            app.switch_mode('main')
        else:
            app.label.insert_text('Escape failed :c\nYou get %s damage\n\n' % player.opponent.attack)
            if player.health < 1:
                app.label.insert_text('You lose! Try again next time!')
                app.switch_mode('dead')

    @App.buttonfunction(buttons['mapbtn'])
    def map_clicked():
        app.mapbox.clear()
        app.label.setText('Your location is %s\n\n' % player.location[0])
        for loc in locations:
            app.mapbox.addItem(loc[0])
        app.switch_mode('map')

    @App.buttonfunction(buttons['cnglocbtn'])
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
            app.label.insert_text(f'{item[0]} in now yours.\n')
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

    def change_market_mode(self):
        if app.markettab.currentIndex():
            self.armor_market()
        else:
            self.weapons_market()


if __name__ == '__main__':
    rpg = Game()
    rpg.start()



""" Hide start buttons and start mainloop """

        app.label.setText('Now the Game begins!\n\n')
        app.switch_mode('main')