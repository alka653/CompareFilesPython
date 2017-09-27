from PyQt5 import QtCore, QtGui, QtWidgets
from ..logic.main import LogicMain
from functools import partial

class Main(QtWidgets.QMainWindow):

	dir_filepath_one = ''
	dir_filepath_two = ''
	content_file_one = ''
	content_file_two = ''

	def __init__(self):
		super(Main, self).__init__()
		self.qt_rect = QtCore.QRect
		self.qt_size = QtCore.QSize
		self.qt_QT = QtCore.Qt
		self.initUI()
		self.logic = LogicMain(
			self.dir_filepath_one,
			self.dir_filepath_two,
			self.content_file_one,
			self.content_file_two,
			self.labelFileFirst,
			self.labelFileSecond,
			self.textAreaFirst,
			self.textAreaSecond
		)
		self.windowConf()
		self.retranslateUi()
		self.btnFileFirst.clicked.connect(partial(self.logic.openFile, 'Archivo 1', 'one'))
		self.btnFileSecond.clicked.connect(partial(self.logic.openFile, 'Archivo 2', 'two'))
		self.compareBtn.clicked.connect(self.logic.compareFiles)
		#self.openFile('none')

	def initUI(self):
		# Imagen
		self.labelImage = QtWidgets.QLabel(self)
		self.labelImage.setPixmap(QtGui.QPixmap('assets/logo.png'))
		self.labelImage.setGeometry(self.qt_rect(350, 10, 289, 131))

		# Ubicacion boton 1
		self.btnFileFirst = QtWidgets.QPushButton(self)
		self.btnFileFirst.setGeometry(self.qt_rect(30, 180, 140, 30))
		self.btnFileFirst.setObjectName("fileFirst")
		self.btnFileFirst.setText("Seleccionar primer archivo")
		self.labelFileFirst = QtWidgets.QLabel(self)
		self.labelFileFirst.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
		self.labelFileFirst.setGeometry(self.qt_rect(180, 170, 400, 50))
		self.labelFileFirst.setText('Ubicación archivo primero')
		self.textAreaFirst = QtWidgets.QPlainTextEdit(self)
		self.textAreaFirst.setGeometry(self.qt_rect(30, 250, 400, 300))
		self.textAreaFirst.setObjectName("fileFirst")

		# Ubicacion boton 2
		self.btnFileSecond = QtWidgets.QPushButton(self)
		self.btnFileSecond.setGeometry(self.qt_rect(530, 180, 150, 30))
		self.btnFileSecond.setObjectName("fileSecond")
		self.btnFileSecond.setText("Seleccionar segundo archivo")
		self.labelFileSecond = QtWidgets.QLabel(self)
		self.labelFileSecond.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
		self.labelFileSecond.setGeometry(self.qt_rect(690, 170, 400, 50))
		self.labelFileSecond.setText('Ubicación archivo segundo')
		self.textAreaSecond = QtWidgets.QPlainTextEdit(self)
		self.textAreaSecond.setGeometry(self.qt_rect(530, 250, 400, 300))
		self.textAreaSecond.setObjectName("fileSecond")

		# bnt compare
		self.compareBtn = QtWidgets.QPushButton(self)
		self.compareBtn.setGeometry(self.qt_rect(440, 250, 80, 30))
		self.compareBtn.setObjectName("compareBtn")
		self.compareBtn.setText("Comparar")

		# FOOTER
		self.footer = QtWidgets.QLabel(self)
		self.footer.setGeometry(self.qt_rect(400, 575, 300, 17))
		self.footer.setObjectName("footer")

	def windowConf(self):
		p = self.palette()
		self.setAutoFillBackground(True)
		p.setColor(self.backgroundRole(), self.qt_QT.white)
		self.setPalette(p)
		self.setMinimumSize(self.qt_size(1000, 600))
		self.setMaximumSize(self.qt_size(1000, 600))

	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("self", "COMPARADOR DE ARCHIVOS"))
		self.footer.setText(_translate("self", "Todos los derechos reservados 2017"))