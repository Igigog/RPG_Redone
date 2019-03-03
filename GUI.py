from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import \
    QWidget, QPushButton, QLabel, QGridLayout, QFrame, QComboBox, QTabBar, QTextEdit
from PyQt5.QtGui import QIcon, QPalette, QColor, QTextCursor


class TextConsole(QTextEdit):
    def insert_text(self, text):
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(text)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def okno(self):
        self.setGeometry(300, 300, 750, 500)
        self.setWindowTitle('WITCHER WITH BLACKJACK AND PLOTVA')
        self.setWindowIcon(QIcon('ico.ico'))

    def buttons(self):

        self.armorbox = QComboBox()
        self.wpnbox = QComboBox()

        self.mapbox = QComboBox()

        self.markettab = QTabBar()
        self.markettab.setShape(1)
        self.marketbox = QComboBox()
        self.markettab.addTab('Weapons')
        self.markettab.addTab('Armor')



        for k in self.buttons_dict.keys():
            exec(f'self.{k} = QPushButton("{self.buttons_dict[k]}")')

    def init_ui(self):
        self.okno()
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.label = TextConsole()
        pal = QPalette()
        pal.setColor(QPalette.Base, QColor.fromRgb(242, 242, 242))
        self.label.setPalette(pal)
        self.label.setReadOnly(True)
        self.label.setFrameStyle(QFrame.Box)           # main label
        self.label.setFrameShadow(QFrame.Raised)
        self.label.setMidLineWidth(1)
        self.label.setLineWidth(1)
        self.label.setAlignment(Qt.AlignTop)
        self.grid.addWidget(self.label, 1, 1, 1, 2)
        self.label.setText('Are you ready for adventure?')

        self.statlabel = QLabel()
        self.statlabel.setFrameStyle(QFrame.Box)            # stat label
        self.statlabel.setFrameShadow(QFrame.Raised)
        self.statlabel.setMidLineWidth(1)
        self.statlabel.setLineWidth(1)
        self.statlabel.setAlignment(Qt.AlignTop)
        self.grid.addWidget(self.statlabel, 1, 3)

        self.buttons()

        self.grid.addWidget(self.startbtn, 2, 1)    # start screen
        self.grid.addWidget(self.loadbtn, 2, 2)

        self.grid.addWidget(self.srbtn, 2, 1)       # main mode
        self.grid.addWidget(self.fndbtn, 2, 2)
        self.grid.addWidget(self.invbtn, 3, 1)
        self.grid.addWidget(self.savebtn, 3, 2)
        self.grid.addWidget(self.mapbtn, 4, 1)
        self.savebtn.hide()
        self.srbtn.hide()
        self.fndbtn.hide()
        self.mapbtn.hide()
        self.invbtn.hide()

        self.grid.addWidget(self.atkbtn, 2, 2)      # fight mode
        self.grid.addWidget(self.escbtn, 2, 1)
        self.atkbtn.hide()
        self.escbtn.hide()

        self.grid.addWidget(self.wpnbox, 2, 1)      # inventory mode
        self.grid.addWidget(self.extinvbtn, 4, 1)
        self.grid.addWidget(self.cngwpnbtn, 2, 2)
        self.grid.addWidget(self.armorbox, 3, 1)
        self.grid.addWidget(self.cngarmorbtn, 3, 2)
        self.armorbox.hide()
        self.cngarmorbtn.hide()
        self.cngwpnbtn.hide()
        self.extinvbtn.hide()
        self.wpnbox.hide()

        self.grid.addWidget(self.mapbox, 2, 1)      # map mode
        self.grid.addWidget(self.cnglocbtn, 2, 2)
        self.grid.addWidget(self.extmapbtn, 3, 1)
        self.grid.addWidget(self.marketbtn, 3, 2)
        self.marketbtn.hide()
        self.mapbox.hide()
        self.extmapbtn.hide()
        self.cnglocbtn.hide()

        self.grid.addWidget(self.markettab, 2, 1)   # market mode
        self.grid.addWidget(self.sellbtn, 4, 1)
        self.grid.addWidget(self.marketbox, 3, 1)
        self.grid.addWidget(self.buybtn, 3, 2)
        self.grid.addWidget(self.extmarket, 4, 2)

        self.buybtn.hide()
        self.sellbtn.hide()
        self.extmarket.hide()
        self.markettab.hide()
        self.marketbox.hide()

        self.show()

    def _hide_all(self):
        for button in self.buttons_dict:
            exec(f'app.{button}.hide()')

        self.wpnbox.hide()
        self.armorbox.hide()

        self.mapbox.hide()

        self.markettab.hide()
        self.marketbox.hide()

    def mode_switch(self, ui_mode):
        self._hide_all()

        for x in self.mode_button_relations[ui_mode]:
            exec(f'self.{x}.show()')


def insert_text(widget, text):
    widget.moveCursor(QTextCursor.End)
    widget.insertPlainText(text)