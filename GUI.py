from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import \
    QWidget, QPushButton, QLabel, QGridLayout, QFrame, QComboBox, QTabBar, QTextEdit
from PyQt5.QtGui import QIcon, QPalette, QColor, QTextCursor
from database_values import buttons as buttons_dict, modes as modes_dict, nonbuttons as nonbuttons_dict


class TextConsole(QTextEdit):
    def insert_text(self, text):
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(text)


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.elements = {}
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self._init_ui()
        self.switch_mode('dead')

    def _init_ui(self):

        def configure_window():
            self.setGeometry(300, 300, 750, 500)
            self.setWindowTitle('WITCHER WITH BLACKJACK AND PLOTVA')
            self.setWindowIcon(QIcon('ico.ico'))

        def make_nonbuttons():
            for element_name in nonbuttons_dict:
                element_type = element_name[::-1][0:3][::-1]  # last three literals
                if element_type == 'box':
                    self.elements[element_name] = QComboBox()
                elif element_type == 'tab':
                    self.elements[element_name] = QTabBar()

        def configure_tabs():
            self.elements['markettab'].setShape(1)
            self.elements['markettab'].addTab('Weapons')
            self.elements['markettab'].addTab('Armor')

        def make_buttons():
            for button_name in buttons_dict:
                chosen_button = buttons_dict[button_name]
                self.elements[button_name] = QPushButton(chosen_button.text)

        def place_everything():
            self.grid.addWidget(self.main_label, 1, 1, 1, 2)
            self.grid.addWidget(self.statlabel, 1, 3)

            dicts = (buttons_dict, nonbuttons_dict)
            for dictionary in dicts:
                for element_name in dictionary:
                    chosen_element = dictionary[element_name]
                    self.grid.addWidget(self.elements[element_name], int(chosen_element.grid_y),
                                        int(chosen_element.grid_x))
                    self.elements[element_name].hide()

        def make_labels():
            self.main_label = TextConsole()
            pal = QPalette()
            pal.setColor(QPalette.Base, QColor.fromRgb(242, 242, 242))
            self.main_label.setPalette(pal)
            self.main_label.setReadOnly(True)
            self.main_label.setFrameStyle(QFrame.Box)  # main label
            self.main_label.setFrameShadow(QFrame.Raised)
            self.main_label.setMidLineWidth(1)
            self.main_label.setLineWidth(1)
            self.main_label.setAlignment(Qt.AlignTop)
            self.main_label.setText('Are you ready for adventure?')

            self.statlabel = QLabel()
            self.statlabel.setFrameStyle(QFrame.Box)  # stat label
            self.statlabel.setFrameShadow(QFrame.Raised)
            self.statlabel.setMidLineWidth(1)
            self.statlabel.setLineWidth(1)
            self.statlabel.setAlignment(Qt.AlignTop)

        configure_window()
        make_buttons()
        make_labels()
        make_nonbuttons()
        make_nonbuttons()
        configure_tabs()

        place_everything()
        self.show()

    def _hide_all(self):
        for element in self.elements:
            self.elements[element].hide()

    @staticmethod
    def buttonfunction(button, static=True):

        def real_decorator(func):
            button.clicked.connect(func)
            if static:
                return staticmethod(func)
            else:
                return func

        return real_decorator


    def switch_mode(self, ui_mode):
        self._hide_all()

        for element in modes_dict[ui_mode]:
            self.elements[element].show()
