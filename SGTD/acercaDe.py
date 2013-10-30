#!/usr/bin/env python
# -*- coding: utf-8 -*-


import gtk

class AcercaDe(object):

    def __init__(self):

        # Se carga el archivo glade con la ventana
        objsW = gtk.Builder()
        objsW.add_from_file('vistas/acercaDe.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winMain = objsW.get_object('winMain')

        # Se asocian las senales del archivo glade a metodos de la clase
        objsW.connect_signals(self)
        self.winMain.show()

    def on_botonCerrar_clicked(self, widget):
        self.winMain.destroy()

    def on_winMain_destroy(self, widget):
        # Esto es solamente por si se llama a la ventana como programa principal, para poder cerrarla
        if __name__ == '__main__':
            gtk.main_quit()
        else:
            self.winMain.destroy()

# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    app = AcercaDe()
    gtk.main()

