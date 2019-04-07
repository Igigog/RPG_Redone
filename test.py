from GUI import app
from PyQt5.QtWidgets import QApplication
import sys

game = QApplication(sys.argv)
app = app()
sys.exit(game.exec_())