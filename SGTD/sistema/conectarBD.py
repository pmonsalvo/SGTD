#!#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Retorna un objeto conexión, o None si no se pudo conectar a la base de datos.
El programa que use este módulo se debe encargar de liberar la conexión.
Forma parte del paquete sistema.
"""

import MySQLdb
import leerProp

# --------------------------------------------------------------------

class ConectarBD(object):

	def __init__(self):
		# Atributo oculto que indica la conexion
		self.__db = None
		
		# Lee el archivo de propiedades para extraer la información de la Base de Datos.
		# Estos datos vienen en un diccionario.
		config = leerProp.armarDicc('sistema/app.config')

		try:
			# En el archivo /etc/mysql/my.cnf está el verdadero nombre del servidor, puede ser la IP o nombre
			self.__db = MySQLdb.connect(host   = config['bdHOST'],
			                            user   = config['bdUSER'],
	                                    passwd = config['bdPASS'],
	                                    db     = config['bdNAME'])
		except:
			self.__db = None

	# Método de acceso al atributo conexión
	def get_db(self):
		return self.__db

# --------------------------------------------------------------------

# Esto solamente se usa para probar el modulo
if __name__ == '__main__':
	a = ConectarBD()
	#print a.__db
	#print a.db
	if (a.get_db() == None):
		print 'Sin conexion'
	else:
		print 'OK'
