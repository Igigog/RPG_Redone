from GUI import App
from PyQt5.QtWidgets import QApplication
import sys

game = QApplication(sys.argv)
app = App()
sys.exit(game.exec_())