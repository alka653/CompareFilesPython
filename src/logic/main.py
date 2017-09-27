# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtWidgets
import subprocess
import os, sys
import random
import xlrd
import csv

class LogicMain(QtWidgets.QWidget):

	cartas_juego = ['fuego', 'agua', 'hielo']

	def __init__(self, dir_filepath_one, dir_filepath_two, content_file_one, content_file_two, btnFileFirst, btnFileSecond, textAreaFirst, textAreaSecond):
		super(LogicMain, self).__init__()
		self.dir_filepath_one = dir_filepath_one
		self.dir_filepath_two = dir_filepath_two
		self.content_file_one = content_file_one
		self.content_file_two = content_file_two
		self.btnFileFirst = btnFileFirst
		self.btnFileSecond = btnFileSecond
		self.textAreaFirst = textAreaFirst
		self.textAreaSecond = textAreaSecond

	def openFile(self, text, file_var):
		options = QtWidgets.QFileDialog.Options()
		fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Abrir archivo '+text, "","Archivos con formato (*.txt *.csv *.xls, *.xlsx)", options = options)
		if fileName:
			if file_var == 'one':
				self.dir_filepath_one = fileName
				self.btnFileFirst.setText(fileName[0])
			else:
				self.dir_filepath_two = fileName
				self.btnFileSecond.setText(fileName[0])

	def put_message(self, message, textarea):
		self.textAreaFirst.appendPlainText(message) if textarea == 'first' else self.textAreaSecond.appendPlainText(message)

	def compare_txt(self, file_path):
		with open(file_path) as file_content:
			return [value.replace('\n', '').split(';') for value in file_content]

	def compare_csv(self, file_path):
		value_to_array = []
		with open(file_path, encoding = "utf-8") as file_content:
			reader = csv.reader(file_content)
			for value in reader:
				value[0] = value[0].replace('\t', '')
				if value[0] != '':
					value_to_array.append(value[0].replace('\t', '').split(';'))
			return value_to_array

	def compare_xls(self, file_path):
		value_to_array = []
		for value in xlrd.open_workbook(file_path).sheets():
			for row in range(0, value.nrows):
				row_value = []
				for col in range(0, value.ncols):
					row_value.append(str(value.cell(row, col).value))
				value_to_array.append(row_value)
		return value_to_array

	def determinate_type_file(self, file_path):
		if '.txt' in file_path:
			return self.compare_txt(file_path)
		elif '.csv' in file_path:
			return self.compare_csv(file_path)
		elif '.xls' in file_path:
			return self.compare_xls(file_path)

	def check_file_code(self, value, key, input_type, textarea):
		value = ''.join(c for c in value if c != '.')
		try:
			if len(value) != 10:
				self.put_message('El '+input_type+' no tiene longitud de 10 en el elemento N° '+str(key+1), textarea)
			value = int(value)
		except ValueError:
			self.put_message('El '+input_type+' no es numérico en el elemento N° '+str(key+1), textarea)

	def check_file_string(self, value, key, input_type, textarea):
		if not isinstance(value, str):
			self. put_message('El '+input_type+' no tiene un nombre válido en el elemento N° '+str(key+1), textarea)
		if len(value) > 30:
			self. put_message('El '+input_type+' excede la longitud 30 en el elemento N° '+str(key+1), textarea)

	def check_file_cash(self, value, key, input_type, textarea):
		value = value.replace('$', '').replace(' ', '').replace('.', '').replace(',', '.')
		try:
			if '.' in value:
				compare_value = len(value.split('.')[0]) + len(value.split('.')[1])
			elif ',' in value:
				compare_value = len(value.split(',')[0]) + len(value.split(',')[1])
			else:
				compare_value = len(value)
			if compare_value > 10:
				self.put_message('El '+input_type+' no tiene longitud de 10 en el elemento N° '+str(key+1), textarea)
			value = float(value)
		except ValueError:
			self.put_message('El '+input_type+' no es un valor válido en el elemento N° '+str(key+1), textarea)

	def compare_value_equals(self, key, text, file_1, file_2):
		if file_1 != file_2:
			self.put_message('El '+text+' es distinto del archivo 2 del elemento N° '+str(key+1), 'first')
			self.put_message('El '+text+' es distinto del archivo 1 del elemento N° '+str(key+1), 'second')
		else:
			self.put_message('El '+text+' es igual que el archivo 2 del elemento N° '+str(key+1), 'first')
			self.put_message('El '+text+' es igual que el archivo 1 del elemento N° '+str(key+1), 'second')

	def compareFiles(self):
		self.textAreaFirst.clear()
		self.textAreaSecond.clear()
		if self.dir_filepath_one == ''or self.dir_filepath_two == '':
			QtWidgets.QMessageBox.information(self, "Alerta", "Falta archivo para comparar", QtWidgets.QMessageBox.Ok)
		else:
			file_path_one = self.determinate_type_file(self.dir_filepath_one[0])
			file_path_two = self.determinate_type_file(self.dir_filepath_two[0])
			if file_path_one[0] != ['Codigo', 'Nombre', 'NoFactura', 'Valor', 'Concepto']:
				self.put_message('El archivo uno no contiene 5 columnas', 'first')
			elif file_path_two[0] != ['Codigo', 'Nombre', 'NoFactura', 'Valor', 'Concepto']:
				self.put_message('El archivo dos no contiene 5 columnas', 'second')
			else:
				key = 0
				del file_path_one[0]
				del file_path_two[0]
				if len(file_path_one) != len(file_path_two):
					self.put_message('El tamaño del archivo es distinto del archivo 2. El archivo 1 contiene '+str(len(file_path_one))+' elementos en lista.', 'first')
					self.put_message('El tamaño del archivo es distinto del archivo 1. El archivo 2 contiene '+str(len(file_path_two))+' elementos en lista.', 'second')
				else:
					self.put_message('El archivo 1 tiene el mismo tamaño que el archivo 2.', 'first')
					self.put_message('El archivo 2 tiene el mismo tamaño que el archivo 1.', 'second')
				for value in file_path_one:
					self.put_message('--------------------------------------------------------------------------------------------', 'first')
					self.put_message('--------------------------------------------------------------------------------------------', 'second')
					try:
						# Código
						self.check_file_code(value[0], key, 'código', 'first')
						self.check_file_code(file_path_two[key][0], key, 'código', 'second')
						self.compare_value_equals(key, 'código', value[0], file_path_two[key][0])
						# Nombre
						self.check_file_string(value[1], key, 'nombre', 'first')
						self.check_file_string(file_path_two[key][1], key, 'nombre', 'second')
						self.compare_value_equals(key, 'nombre', value[1], file_path_two[key][1])
						# Factura
						self.check_file_code(value[2], key, 'código de factura', 'first')
						self.check_file_code(file_path_two[key][2], key, 'código de factura', 'second')
						self.compare_value_equals(key, 'código de factura', value[2], file_path_two[key][2])
						# Valor
						self.check_file_cash(value[3], key, 'valor', 'first')
						self.check_file_cash(file_path_two[key][3], key, 'valor', 'second')
						self.compare_value_equals(key, 'valor', value[3], file_path_two[key][3])
						# Concepto
						self.check_file_string(value[4], key, 'concepto', 'first')
						self.check_file_string(file_path_two[key][4], key, 'concepto', 'second')
						self.compare_value_equals(key, 'concepto', value[4], file_path_two[key][4])
					except IndexError:
						# Código
						self.check_file_code(value[0], key, 'código', 'first')
						# Nombre
						self.check_file_string(value[1], key, 'nombre', 'first')
						# Factura
						self.check_file_code(value[2], key, 'código de factura', 'first')
						# Valor
						self.check_file_cash(value[3], key, 'valor', 'first')
						# Concepto
						self.check_file_string(value[4], key, 'concepto', 'first')
						self.put_message('El archivo 2 no contiene elemento N° '+str(key+1)+'.', 'second')
					key += 1
				if len(file_path_two) > len(file_path_one):
					for value in range(key, len(file_path_two)):
						self.put_message('--------------------------------------------------------------------------------------------', 'first')
						self.put_message('--------------------------------------------------------------------------------------------', 'second')
						# Código
						self.check_file_code(file_path_two[value][0], key, 'código', 'second')
						# Nombre
						self.check_file_string(file_path_two[value][1], key, 'nombre', 'second')
						# Factura
						self.check_file_code(file_path_two[value][2], key, 'código de factura', 'second')
						# Valor
						self.check_file_cash(file_path_two[value][3], key, 'valor', 'second')
						# Concepto
						self.check_file_string(file_path_two[value][4], key, 'concepto', 'second')
						self.put_message('El archivo 1 no contiene elemento N° '+str(key+1)+'.', 'first')
						key += 1