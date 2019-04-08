import sys
import pickle
from PyQt5.QtWidgets import QApplication
from GUI import App
from fighting_system import *


# noinspection PyMethodParameters
class Game:

    # PRE_GAME PREPARATIONS

    my_game = QApplication(sys.argv)    # cant define App() without QApplication()
    global app
    app = App()                         # to use buttonfunction

    def __init__(self):
        global player
        player = Player()

    def connect_elements(self):
        """connect last elements from GUI with functions"""

        app.elements['markettab'].currentChanged.connect(self.change_market_mode)
        app.main_label.textChanged.connect(self.update_stats)  # looks dirty, but works

    @staticmethod
    def update_stats():
        app.statlabel.setText(f'LVL: {player.lvl}\n'
                              f'EXP: {player.exp}\n'
                              f'ATK: {(player.attack_stat + player.weapon.main_stat)}\n'
                              f'DEF: {player.armor_stat}\n'
                              f'ARM: {player.equip.name}\n'
                              f'WPN: {player.weapon.name}\n'
                              f'GOLD: {player.gold}')

    # START FUNCTIONS

    def start(self):
        self.connect_elements()
        sys.exit(self.my_game.exec_())

    @app.buttonfunction('startbtn')
    def start_clicked():
        """ Hide start buttons and start mainloop """

        app.main_label.setText('Now the Game begins!\n\n')
        app.switch_mode('main')

    @app.buttonfunction('loadbtn')
    def load_clicked():
        global player
        player.reset()

        try:
            with open('database/save.pickle', 'rb') as player_savefile:
                player = pickle.load(player_savefile)
        except EnvironmentError:
            app.main_label.setText('Save corrupted\n\n')
        else:
            app.main_label.setText('Load successful')
            app.switch_mode('main')

    @app.buttonfunction('savebtn')
    def save_clicked():
        try:
            with open('database/save.pickle', 'wb') as savefile:
                pickle.dump(player, savefile)
        except EnvironmentError:
            app.main_label.setText('Something went wrong')
        else:
            app.main_label.setText('Save successful')

    # MAIN_MODE FUNCTIONS

    @app.buttonfunction('extmarket', 'extmapbtn', 'extinvbtn')
    def to_main_mode():
        app.switch_mode('main')

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
            Game.find_clicked()
        elif player.energy:
            x = player.search_treasure()
            app.main_label.insert_text(f'You found {x}\n')
            player.energy -= 1
        else:
            app.main_label.insert_text('No energy\n')

    @app.buttonfunction('invbtn')
    def inv_clicked():
        app.elements['armorbox'].clear()
        app.elements['wpnbox'].clear()
        app.main_label.setText(f'You weapon is {player.weapon.name}\n')
        app.main_label.insert_text(f'You armor is {player.equip.name}\n\n')
        for x in player.wpninventory:
            app.elements['wpnbox'].addItem(x.name)
        for x in player.armorinventory:
            app.elements['armorbox'].addItem(x.name)
        app.switch_mode('inventory')

    # INVENTORY FUNCTIONS

    @app.buttonfunction('cngarmorbtn')
    def change_armor():
        player.equip = armors[app.elements['armorbox'].currentText()]
        app.main_label.insert_text(f'You armor is {player.equip.name}\n\n')

    @app.buttonfunction('cngwpnbtn')
    def change_weapon():
        player.weapon = weapons[app.elements['wpnbox'].currentText()]
        app.main_label.insert_text(f'You weapon is {player.weapon.name}\n\n')

    # FIGHT FUNCTIONS

    @app.buttonfunction('atkbtn', static=False)
    def atk_clicked(self):
        text = fight.fight_step()
        app.main_label.insert_text(text)
        Game.win_check()

    @app.buttonfunction('escbtn', static=False)
    def esc_clicked(self):
        if fight.escape():
            app.main_label.insert_text('You escaped c:\n\n')
            app.switch_mode('main')
        else:
            app.main_label.insert_text(f'Escape failed :c\n'
                                       f'You get {fight.opponent.attack_stat} damage\n\n')
            Game.win_check()

    @staticmethod
    def win_check():
        if fight.is_won():
            app.switch_mode('main')
        elif fight.is_won() is None:
            pass
        else:
            app.main_label.insert_text('You lose! Try again next time!')
            app.switch_mode('dead')

    # MAP FUNCTIONS

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

    @app.buttonfunction('marketbtn', static=False)
    def enter_market(self):
        app.switch_mode('market')
        Game.fill_market('weapons')

    # MARKET FUNCTIONS

    @staticmethod
    def fill_market(objective):
        variants = {'weapons': (weapons, 'ATK'),
                    'armor': (armors, 'DEF'),
                    }
        app.elements['marketbox'].clear()
        app.main_label.clear()
        market_type = variants[objective]
        for item in market_type[0].values():
            if item.lvl in range(player.location.lvl, player.location.lvl + 3):
                app.elements['marketbox'].addItem(item.name)
                app.main_label.insert_text(f'{item.name}  {market_type[1]}:{item.main_stat}  COST:{item.cost}\n')
        app.main_label.insert_text('\n')

    @app.buttonfunction('buybtn')
    def buy_clicked():
        tab_indexes = (weapons, armors)
        current_tab = tab_indexes[app.elements['markettab'].currentIndex()]
        item = current_tab[app.elements['marketbox'].currentText()]

        if item in player.wpninventory or \
           item in player.armorinventory:
            app.main_label.insert_text(f'{item.name} is already yours')
            return False

        elif player.gold < item.cost:
            app.main_label.insert_text('Not enough gold.\n\n')
            return False

        else:
            inventory_indexes = (player.wpninventory,
                                 player.armorinventory)
            inventory = inventory_indexes[app.elements['markettab'].currentIndex()]
            inventory.append(item)

            player.gold -= item.cost
            app.main_label.insert_text(f'{item.name} in now yours.\n')
            return True

    @app.buttonfunction('sellbtn')
    def sell_clicked():
        loot_sum = 0
        if not player.garbageinv:
            app.main_label.insert_text('No garbage.\n\n')
            return False

        for item in player.garbageinv:
            loot_sum += item.cost
            player.garbageinv.pop(0)

        player.gold += loot_sum
        app.main_label.insert_text(f'Garbage sold. You get {loot_sum} gold.\n\n')

    def change_market_mode(self):
        tab_indexes = ('weapons', 'armor')
        current_tab = tab_indexes[app.elements['markettab'].currentIndex()]
        self.fill_market(current_tab)

    # END GAME


if __name__ == '__main__':
    rpg = Game()
    rpg.start()
