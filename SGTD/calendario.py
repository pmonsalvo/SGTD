#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: calendario.py J.M.M. 06/04/2011 
Descripción: carga calendario.glade - Ventana de que retorna una fecha mostrando un calendario
"""

import gtk
import time

from sistema import mensajes

class Calendario(object):

    def __init__(self, fecha, wtexto):
        """
        fecha  = inicializa el calendario. None inicializa en fecha actual del sistema.
        wtexto = widget que muestra lo seleccionado. None no tiene asociado widget.
        """
       
        # Se carga el archivo glade con la ventana
        objsW = gtk.Builder()
        objsW.add_from_file('vistas/calendario.glade')
        
        # Se recuperan los widget a usar (no son necesarios todos)
        self.winMain = objsW.get_object('winMain')
        self.calendario = objsW.get_object('calendario')
        self.wtexto = wtexto

        if fecha == None:
            fecha = time.localtime() # Tupla con la hora y fecha completa
        self.setFecha(fecha)

        # Se asocian las senales del archivo glade a metodos de la clase
        objsW.connect_signals(self)
        self.winMain.show()

    # -------------------------------------------------------------------------------------
    
    def setFecha(self,fecha):
        self.calendario.select_month(fecha[1] - 1, fecha[0]) # Mes y año se seleccionan juntos
        self.calendario.select_day(fecha[2])

    # ------------------------------- Eventos de la ventana -------------------------------

    # -------------------------------------------------------------------------------------

    def on_botonCerrar_clicked(self, widget):
        self.wtexto.set_text(toStr(self.calendario.get_date()))
        self.winMain.hide()

    # -------------------------------------------------------------------------------------

    def on_winMain_destroy(self, widget):
        self.winMain.destroy()

    # -------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------

def toStr(fecha):
    """
    Recibe una fecha de formato tupla, y la pasa a str
    """
    if (fecha != None):
        dia = str(fecha[2])
        mes = str(fecha[1] + 1)
        anio = str(fecha[0])
        return (dia + '/' + mes + '/' + anio)
    else:
        return ''

# -----------------------------------------------------------------------------------------

def toTuple(fecha):
    """
    Recibe una fecha de formato MySQL, y la pasa a formato tupla
    """
    fechaStr = str(fecha)
    fechaTupla = (int(fechaStr[0:4]),int(fechaStr[5:7]),int(fechaStr[8:10]))
    return fechaTupla

# -----------------------------------------------------------------------------------------

def toMySQL(fecha):
    """
    Recibe una fecha de formato tuple, y la pasa a formato str de MySQL (YYYY-MM-DD)
    Este suma uno al mes, ya que se usa cuando la tupla informa los meses de 0 a 11
    """
    dia = str(fecha[2])
    mes = str(fecha[1] + 1)
    anio = str(fecha[0])
    return anio + '-' + mes + '-' + dia

# -----------------------------------------------------------------------------------------

def timeToMySQL(fecha):
    """
    Recibe una fecha de formato tuple, y la pasa a formato str de MySQL (YYYY-MM-DD)
    Este asume que el mes se informa de 1 a 12, como lo haría la fecha del sistema
    """
    dia = str(fecha[2])
    mes = str(fecha[1])
    anio = str(fecha[0])
    return anio + '-' + mes + '-' + dia

# -----------------------------------------------------------------------------------------

# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    fecha = (2010,12,1)
    app = Calendario(None)
    gtk.main()
