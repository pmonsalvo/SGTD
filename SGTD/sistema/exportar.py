#!#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: exportar.py J.M.M. 24/03/2011 
Descripción: Exporta a CSV y PDF.
Forma parte del paquete sistema.
"""

import gtk
import csv
import os

import mensajes
from PyFPDF import FPDF
import leerProp

# --------------------------------------------------------------------

# Programas por defecto que abren los archivos.
prop = leerProp.armarDicc('sistema/app.config') # Estos datos vienen en un diccionario.
progCSV = prop['appCSV']
archivoCSV = prop['fileCSV']
progPDF = prop['appPDF']
archivoPDF = prop['filePDF']

# -------------------------------------------------------------------------------------------------

def genCSV(model,columnas):
	"""
	Exporta a CSV un modelo representando un TreeView completo.
	Permite abrir el archivo con OpenOffice.
	"""

	# Archivo de salida en formato CSV separado por tabuladores
	archivo = open(archivoCSV, "wb")
	writer = csv.writer(archivo, delimiter = '\t', quotechar = '"', quoting = csv.QUOTE_ALL)

	writer.writerow(columnas) # Columnas del archivo CSV

	iter = model.get_iter_first() # El iterador es el que se encarga de apuntar a la fila correspondiente
	while iter != None:
		fila = list(model[iter])
		writer.writerow(fila)
		iter = model.iter_next(iter) # Siguiente elemento desde iter
	archivo.close()
	abrir = mensajes.pregunta(None, mensajes.ARCH_SAVE + archivoCSV + '\n' + mensajes.ARCH_OPEN)
	if abrir: os.system(progCSV + ' ' + archivoCSV) # Este comando no hace transportable la aplicación.

# -------------------------------------------------------------------------------------------------

def genPDF(model,columnas,titulo):
	"""
	Exporta a PDF un modelo representando un TreeView completo.
	Permite abrir el archivo con el visor de archivos de GNOME.
	"""

	# ---------------------------------------------------------------------------------------------

	class PDF(FPDF):
		"""
		Se crea una nueva clase PDF que extiende de FPDF solamente para poder re escribir los métodos Header y Footer.
		Están vacíos por defecto, es la manera de que se los pueda invocar (los invoca directamente AddPage y Close).
		Como la clase solo se usa para genPDF, se define dentro del programa y no global al modulo.
		
		El código que arma el PDF está muy en duro, lo idea sería tener un procedimiento que lo dibuje de manera estandar.
		"""

		# ---------------------------------------------------------------------------------------------

		def Header(self):
			self.SetFont('Arial', 'B', 15); # Select Arial bold 15			
			self.Cell(5); # Move to the right
			self.Cell(185, 10, titulo, 1, 0, 'C'); # Framed title
			#self.Ln(20); # Line break

		# ---------------------------------------------------------------------------------------------

		def Footer(self):
			self.SetY(-15); # Go to 1.5 cm from bottom
			self.SetFont('Arial', 'I', 8); # Select Arial italic 8
			self.Cell(0, 10, 'Pagina ' + str(self.PageNo()), 0, 0, 'C'); # Print centered page number

	# ---------------------------------------------------------------------------------------------

	def nuevaPag(pdf):
		pdf.AddPage()
		pdf.Rect(15.0, 25.0, 185.0, 235.0) # Rectángulo de la página
		pdf.SetFont('Arial', '', 10) # Letra del Contenido
		#pdf.SetXY(20.0, 30.0) # Posición inicial del contenido
		pdf.SetY(30.0) # Línea inicial del contenido

	# ---------------------------------------------------------------------------------------------

	# Genera PDF con los datos
	pdf = PDF(format = 'Letter') # Ver que es nuestra clase PDF, sino se usan headers o footers, usar FPDF

	elementos = len(columnas)
	# El iterador es el que se encarga de apuntar a la fila correspondiente
	iter = model.get_iter_first()

	while iter != None:
		fila = list(model[iter])
		nuevaPag(pdf) # Se genera una página del PDF
		# Una vez en la fila, se recorre cada elemento
		for indice in range(elementos):
			pdf.SetX(20.0) # Se posiciona en la columna indicada
			pdf.Cell(w = 0, align = 'L', txt = str(columnas[indice]) + ': ')
			pdf.SetX(50.0) # Se posiciona en la columna indicada
			pdf.Cell(w = 0, align = 'L', txt = str(fila[indice]))
			pdf.Ln(5)
		# Siguiente elemento desde iter
		iter = model.iter_next(iter)

	pdf.Close()

	pdf.Output(archivoPDF, 'F')
	abrir = mensajes.pregunta(None, mensajes.ARCH_SAVE + archivoPDF + '\n' + mensajes.ARCH_OPEN)
	if abrir: os.system(progPDF + ' ' + archivoPDF) # Este comando no hace transportable la aplicación.

# ---------------------------------------------------------------------------------------------
