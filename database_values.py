from csv import reader as csv_reader
from collections import namedtuple

# GUI
Button = namedtuple('Button', 'text grid_y grid_x func');               buttons = {}
NonbuttonElement = namedtuple('NonbuttonElement', 'grid_y grid_x');     nonbuttons = {}
modes = {}

# Fighting
Weapon = namedtuple('Weapon', 'attack crit lvl cost');             weapons = {}
Armor = namedtuple('Armor', 'armor dodge lvl price');              armors = {}
Loot = namedtuple('Loot', 'cost lvl');                             loots = {}
Location = namedtuple('Location', 'lvl');                          locations = {}
Enemy = namedtuple('Enemy', 'health attack armor lvl golddrop');   enemies = {}


Relation = namedtuple('Relation', 'dict file type')


relations = [Relation(buttons, 'database/buttons.csv', Button),
             Relation(nonbuttons, 'database/nonbuttons_gui.csv', NonbuttonElement),
             Relation(modes, 'database/modes.csv', tuple),
             Relation(weapons, 'database/weapons.csv', Weapon),
             Relation(armors, 'database/armor.csv', Armor),
             Relation(loots, 'database/loot.csv', Loot),
             Relation(locations, 'database/locations.csv', Location),
             Relation(enemies, 'database/enemies.csv', Enemy),
             ]


def type_interface(format_type, iterable):
    try:
        return format_type((x for x in iterable if str(x)))
    except TypeError:
        return format_type(*iterable)


for database_num in range(len(relations)):
    with open(relations[database_num].file) as data:
        for row in tuple(csv_reader(data))[1:]:
            row = row[1:]                               # delete num variable
            relations[database_num].dict[row[0]] = type_interface(relations[database_num].type, row[1:])
