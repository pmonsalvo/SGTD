#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: cambiopwd.py J.M.M. 20/03/2011 
Descripción: Ventana para cambiar la clave del usuario logueado
"""

import gtk
import gtk.glade

from sistema import mensajes
import users
from sistema import globalDef

class Cambiopwd(object):

    def __init__(self):

        # Se carga el archivo glade con la ventana
        objsW = gtk.Builder()
        objsW.add_from_file('vistas/cambiopwd.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winMain = objsW.get_object('winMain')
        self.textoUsuario = objsW.get_object('textoUsuario')
        self.textoClave = objsW.get_object('textoClave')
        self.textoNueva = objsW.get_object('textoNueva')
        self.textoRepite = objsW.get_object('textoRepite')

        self.textoUsuario.set_text(globalDef.glb_usrNombre) # Nombre del usuario logueado

        # Se asocian las senales del archivo glade a metodos de la clase
        objsW.connect_signals(self)
        self.winMain.show()

    # --------------- Eventos de la ventana ---------------
    # -----------------------------------------------------

    def on_botonSalir_clicked(self, widget):
        self.winMain.destroy()

    # -----------------------------------------------------

    def on_botonCambiar_clicked(self, widget):

        # Se busca el usuario y clave para ver si es un usuario correcto.
        usuario = users.buscarLogin(self.textoUsuario.get_text(), self.textoClave.get_text())

        # La clave nueva y la repetida deben ser iguales
        if (self.textoNueva.get_text() != self.textoRepite.get_text()):
            mostrar = mensajes.error(self.winMain, mensajes.REPASS_NO)
        # La clave tiene que tener un caracter
        elif (self.textoNueva.get_text() == ''):
            mostrar = mensajes.error(self.winMain, mensajes.PASS_NO)
        # El login debe ser correcto
        elif (usuario == None):
            mostrar = mensajes.error(self.winMain, mensajes.USER_NO)
        # Es un usuario válido, modificamos su clave
        else:
            # Asignamos al objeto la clave nueva.
            usuario.setPassword(self.textoRepite.get_text())
            salida = users.actualizar(usuario)
            if salida: mostrar = mensajes.aviso(self.winMain, mensajes.PASS_OK)
            else: mostrar = mensajes.error(self.winMain, mensajes.OPER_NO)
            self.winMain.destroy()

    # -----------------------------------------------------

    def on_winMain_destroy(self, widget):
        self.winMain.destroy()

    # -----------------------------------------------------

# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    app = Cambiopwd()
    gtk.main()
