import sys
import pickle
from PyQt5.QtWidgets import QApplication
from GUI import App
from fighting_system import *


class Game:
    def __init__(self):
        self.game = QApplication(sys.argv)
        global app
        app = App()

        global player
        player = Player()

    def connect_elements(self):
        """connect last elements from GUI with functions"""

        app.elements['markettab'].currentChanged.connect(self.change_market_mode)
        app.main_label.textChanged.connect(self.update_stats)

    @staticmethod
    def update_stats():
        app.statlabel.setText(f'LVL: {player.lvl}\n'
                              f'EXP: {player.exp}\n'
                              f'ATK: {(player.attack_stat + player.weapon[1])}\n'
                              f'DEF: {player.armor_stat}\n'
                              f'ARM: {player.equip[0]}\n'
                              f'WPN: {player.weapon[0]}\n'
                              f'GOLD: {player.gold}')

    def start(self):
        self.connect_elements()
        sys.exit(self.game.exec_())

    @app.buttonfunction('startbtn')
    def start_clicked():
        """ Hide start buttons and start mainloop """

        app.main_label.setText('Now the Game begins!\n\n')
        app.switch_mode('main')

    @app.buttonfunction('extmarket', 'extmapbtn', 'extinvbtn')
    def to_main_mode():
        app.switch_mode(['main_mode'])

    @app.buttonfunction('loadbtn')
    def load_clicked():
        global player
        player.reset()

        try:
            with open('database/save.pickle', 'rb') as player_savefile:
                player = pickle.load(player_savefile)
        except EnvironmentError:
            app.main_label.setText('Save corrupted\n\n')
            return
        else:
            app.main_label.setText('Load successful')
            app.mode_switch('main')

    @app.buttonfunction('savebtn')
    def save_clicked():
        try:
            with open('database/save.pickle', 'wb') as savefile:
                pickle.dump(player, savefile)
        except EnvironmentError:
            app.main_label.setText('Something went wrong')
        else:
            app.main_label.setText('Save successful')

    @app.buttonfunction('fndbtn')
    def find_clicked():
        enemy = player.find_opponent()
        global fight
        fight = Fight(player, enemy)
        app.switch_mode('fight')
        app.main_label.setText(f'Your opponent is {fight.opponent.name}\n\n')

    @app.buttonfunction('srbtn', static=False)
    def search_clicked(self):
        app.main_label.clear()
        if randint(1, 10) < 3:
            self.find_clicked()
        elif player.energy:
            x = player.search_treasure()
            app.main_label.insert_text(f'You found {x}\n')
            player.energy -= 1
        else:
            app.main_label.insert_text('No energy\n')

    @app.buttonfunction('invbtn')
    def inv_clicked():
        app.armorbox.clear()
        app.wpnbox.clear()
        app.main_label.setText(f'You weapon is {player.weapon.name}\n')
        app.main_label.insert_text(f'You armor is {player.equip.name}\n\n')
        for x in player.wpninventory:
            app.wpnbox.addItem(x[0])
        for x in player.armorinventory:
            app.armorbox.addItem(x[0])
        app.switch_mode('inventory')

    @app.buttonfunction('cngarmorbtn')
    def change_armor():
        for x in player.armorinventory:
            if x[0] == app.armorbox.currentText():
                player.equip = x
                player.armor = x[1]
                player.dodge = x[2]
                break
        app.main_label.insert_text(f'You armor is {player.equip[0]}\n\n')

    @app.buttonfunction('cngwpnbtn')
    def change_weapon():
        for x in player.wpninventory:
            if x[0] == app.wpnbox.currentText():
                player.weapon = x
                player.crit = player.weapon[2]
                break
        app.main_label.insert_text(f'You weapon is {player.weapon.name}\n\n')

    @staticmethod
    def win_check():
        if fight.is_won():
            app.switch_mode('main')
        elif fight.is_won() is None:
            pass
        else:
            app.main_label.insert_text('You lose! Try again next time!')
            app.switch_mode('dead')

    @app.buttonfunction('atkbtn', static=False)
    def atk_clicked(self):
        text = fight.fight_step()
        app.main_label.insert_text(text)
        self.__class__.win_check()

    @app.buttonfunction('escbtn', static=False)
    def esc_clicked(self):
        if fight.escape():
            app.main_label.insert_text('You escaped c:\n\n')
            app.switch_mode('main')
        else:
            app.main_label.insert_text(f'Escape failed :c\nYou get {fight.opponent.attack} damage\n\n')
            self.win_check()

    @app.buttonfunction('mapbtn')
    def map_clicked():
        app.elements['mapbox'].clear()
        app.main_label.setText(f'Your location is {player.location.name}\n\n')
        for location in locations:
            app.elements['mapbox'].addItem(location)
        app.switch_mode('map')

    @app.buttonfunction('cnglocbtn')
    def change_loc():
        player.location = locations[app.elements['mapbox'].currentText()]
        app.main_label.insert_text(f'Your location is {player.location.name}\n\n')

    def weapons_market():
        app.marketbox.clear()
        app.main_label.clear()
        for x in weapons:
            if x[3] in range(player.location.lvl, player.location.lvl + 3):
                app.marketbox.addItem(x[0])
                app.main_label.insert_text(f'{x.name}  ATK:{x.attack}  COST:{x.cost}\n')
        app.main_label.insert_text('\n')

    def armor_market():
        app.marketbox.clear()
        app.main_label.clear()
        for x in armors:
            if x[3] in range(player.location.lvl, player.location.lvl + 3):
                app.marketbox.addItem(x[0])
                app.main_label.insert_text(f'{x.name}  DEF:{x.armor}  COST:{x.cost}\n')
        app.main_label.insert_text('\n')

    def enter_market(self):
        app.switch_mode('market')
        self.weapons_market()

    def buy_clicked():
        tab_indexes = {0: weapons, 1: armors}

        current_list = list(tab_indexes[app.markettab.currentIndex()])  # just making a copy
        current_list.pop(0)                     # removes Nothing
        current_list = list(filter(
            lambda x: x[3] in range(player.location[1], player.location[1] + 3),
            current_list))  # filter by location lvl

        item = current_list[app.marketbox.currentIndex()]
        if player.gold < item[4]:
            app.main_label.insert_text('Not enough gold.\n\n')
            return False

        elif item in player.wpninventory or item in player.armorinventory:
            app.main_label.insert_text(f'{item.name} is already yours')
            return False

        else:
            if app.markettab.currentIndex():
                player.wpninventory.append(item)
            else:
                player.armorinventory.append(item)
            player.gold -= item[4]
            app.main_label.insert_text(f'{item[0]} in now yours.\n')
            return True


    def sell_clicked():
        summa = 0
        if not player.garbageinv:
            app.main_label.insert_text('No garbage.\n\n')
            return False
        for x in range(len(player.garbageinv)):
            summa += player.garbageinv[0][1]
            player.garbageinv.pop(0)
        player.gold += summa
        app.main_label.insert_text(f'Garbage sold. You get {summa} gold.\n\n')

    def change_market_mode(self):
        if app.markettab.currentIndex():
            self.armor_market()
        else:
            self.weapons_market()


if __name__ == '__main__':
    rpg = Game()
    rpg.start()



