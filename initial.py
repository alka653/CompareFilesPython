# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
from src.view.main import Main
import sys

def initial():
	app = QApplication(sys.argv)
	view_initial = Main()
	view_initial.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	initial()