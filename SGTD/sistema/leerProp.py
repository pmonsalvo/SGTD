#!#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modulos para leer/escribir datos de archivos externos.
Forma parte del paquete sistema.

leerConfig(file)   = lee archivo de configuracion
armarDicc(archivo) = diccionario con propiedades del sistema
"""

import string

# --------------------------------------------------------------------

def leerConfig(archTexto):
	""" Lee archivo de configuracion """
	try:
		f = file(archTexto)
	except:
		f = None
	return f

# --------------------------------------------------------------------

def armarDicc(archTexto):
	""" En un diccionario retorna las propiedades de un archivo """

	# Inicializa el diccionario vacio
	dicc = {}

	# Lee el archivo del disco y va armando el diccionario con cada linea
	archivo = leerConfig(archTexto)
	if archivo == None:
		return dicc
	else:
		while True:
			cadena = archivo.readline() # Linea actual del archivo
			if not cadena: break # Si es nulo, termina el archivo y sale del ciclo
			indice = string.find(cadena, '=') # El indice es la posicion del separador
			prop = cadena[0 : indice]
			valor = cadena[indice + 1 : len(cadena) - 1]
			dicc[prop] = valor
		return dicc

# --------------------------------------------------------------------
