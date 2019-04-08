from csv import reader as csv_reader
from collections import namedtuple

# GUI
Button = namedtuple('Button', 'name text grid_y grid_x');               buttons = {}
NonbuttonElement = namedtuple('NonbuttonElement', 'name grid_y grid_x');     nonbuttons = {}
modes = {}


class Mode:
    def __init__(self, iterable):
        not_first = False
        self.elements = []
        for x in iterable:
            if not_first:
                self.elements.append(x)
            else:
                self.name = x
                not_first = True


# Fighting
Weapon = namedtuple('Weapon', 'name main_stat crit lvl cost');             weapons = {}
Armor = namedtuple('Armor', 'name main_stat dodge lvl cost');              armors = {}
Loot = namedtuple('Loot', 'name cost lvl, rarity');                             loots = {}
Location = namedtuple('Location', 'name lvl');                          locations = {}
Enemy = namedtuple('Enemy', 'name health attack armor lvl golddrop');   enemies = {}


Relation = namedtuple('Relation', 'dict file type')


relations = [Relation(buttons, 'database/buttons.csv', Button),
             Relation(nonbuttons, 'database/nonbuttons_gui.csv', NonbuttonElement),
             Relation(modes, 'database/modes.csv', Mode),
             Relation(weapons, 'database/weapons.csv', Weapon),
             Relation(armors, 'database/armor.csv', Armor),
             Relation(loots, 'database/loot.csv', Loot),
             Relation(locations, 'database/locations.csv', Location),
             Relation(enemies, 'database/enemies.csv', Enemy),
             ]


def type_interface(format_type, iterable):
    no_blank_strings = (x for x in iterable if str(x))
    try:
        return format_type(no_blank_strings)
    except TypeError:
        return format_type(*no_blank_strings)


def int_converter(arguments):
    new_args = []
    for x in arguments:
        try:
            x = float(x)
            x = int(x)
        except ValueError:
            pass
        new_args.append(x)
    return new_args


for database_num in range(len(relations)):
    with open(relations[database_num].file) as data:
        for row in tuple(csv_reader(data))[1:]:
            row = row[1:]                               # delete num variable
            relations[database_num].dict[row[0]] = type_interface(
                relations[database_num].type,
                int_converter(row))
