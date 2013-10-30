#!#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: mensajes.py J.M.M. 18/03/2011 
Descripción: Carteles de mensajes de avisos, warning y preguntas.
Forma parte del paquete sistema.
"""

import gtk
import leerProp

# --------------------------------------------------------------------

# Constantes que leen los mensajes desde el archivo de configuración
msg = leerProp.armarDicc('sistema/msg.config') # Estos datos vienen en un diccionario.

LOGIN_TRUE = msg['LOGIN_TRUE']
LOGIN_FALSE = msg['LOGIN_FALSE']
OPER_NO = msg['OPER_NO']
OPER_OK = msg['OPER_OK']
REPASS_NO = msg['REPASS_NO']
PASS_NO = msg['PASS_NO']
USER_NO = msg['USER_NO']
PASS_OK = msg['PASS_OK']
DELETE = msg['DELETE']
DATOS_NO = msg['DATOS_NO']
USER_EXISTE = msg['USER_EXISTE']
TITLE_PDF = msg['TITLE_PDF']
ARCH_OPEN = msg['ARCH_OPEN']
ARCH_SAVE = msg['ARCH_SAVE']
CAR_PROD = msg['CAR_PROD']
CANT_ERR = msg['CANT_ERR']

# --------------------------------------------------------------------

def mostrar(padre, cartel, tipo, botones):
	ventana = gtk.MessageDialog(parent = padre,
	                            type = tipo,
	                            buttons = botones,
	                            message_format = cartel)
	respuesta = ventana.run()
	ventana.destroy()
	if (respuesta == gtk.RESPONSE_OK) or (respuesta == gtk.RESPONSE_YES):
		return True
	else:
		return False

# --------------------------------------------------------------------

def aviso(padre, cartel):
	"""
	Muestra un cartel con el mensaje del usuario.
	Retorna siempre True por el botón que muestra, igualmente no se usa respuesta, solo es para aviso.
	"""
	return mostrar(padre, cartel, gtk.MESSAGE_INFO, gtk.BUTTONS_OK)

# --------------------------------------------------------------------

def error(padre, cartel):
	"""
	Muestra un cartel con el mensaje del usuario. Es para indicar un error.
	Retorna siempre False por el botón que muestra, igualmente no se usa respuesta, solo es para aviso.
	"""
	return mostrar(padre, cartel, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE)

# --------------------------------------------------------------------

def advert(padre, cartel):
	"""
	Muestra un cartel con el mensaje del usuario. Es para indicar advertencia.
	2 salidas posibles, True-False
	"""
	return mostrar(padre, cartel, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK_CANCEL)

# --------------------------------------------------------------------

def pregunta(padre, cartel):
	"""
	Muestra un cartel con el mensaje del usuario. Es para indicar una pregunta.
	2 salidas posibles, True-False
	"""
	return mostrar(padre, cartel, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO)

# --------------------------------------------------------------------
