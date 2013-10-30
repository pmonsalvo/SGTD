#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: index.py  
Descripción: carga index.glade y define los eventos
"""

import gtk

import cambiopwd
import usuarios
#import proyectos
import acercaDe
import clientes
import proveedores
import vendedores
import productos
import ventas
import compras
import pagos

class Index(object):

    def __init__(self):

        # Se carga el archivo glade con la ventana
        objsW = gtk.Builder()
        objsW.add_from_file('vistas/index.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winMain = objsW.get_object('winMain')
        
        # Se asocian las senales del archivo glade a metodos de la clase
        objsW.connect_signals(self)
        self.winMain.show()

    # ------------------------------- Eventos de la ventana -------------------------------

    # -------------------------------------------------------------------------------------

    def on_itemCambioPwd_activate(self, widget):
        cambiopwd.Cambiopwd()

    # -------------------------------------------------------------------------------------

    def on_botonSalir_clicked(self, widget):
        self.winMain.destroy()

    # -------------------------------------------------------------------------------------

    def on_botonUsuarios_clicked(self, widget):
        usuarios.Usuarios()

    # -------------------------------------------------------------------------------------
    
    def on_botonClientes_clicked(self, widget):
        clientes.Clientes()

    # -------------------------------------------------------------------------------------
    
    def on_botonProveedores_clicked(self, widget):
        proveedores.Proveedores()
        

    # -------------------------------------------------------------------------------------
    
    def on_botonVendedores_clicked(self, widget):
        vendedores.Vendedores()
        
    # -------------------------------------------------------------------------------------
    
    def on_botonProductos_clicked(self, widget):
        productos.Productos()

    # -------------------------------------------------------------------------------------
    
    def on_botonAcerca_clicked(self, widget):
            acercaDe.AcercaDe()

    # -------------------------------------------------------------------------------------

    def on_winMain_destroy(self, widget):
        gtk.main_quit()

    # -------------------------------------------------------------------------------------
    
    def on_botonVentas_clicked(self, widget):
        ventas.Ventas()
        
    # -------------------------------------------------------------------------------------
    
    def on_botonCompras_clicked(self, widget):
        compras.Compras()
# -------------------------------------------------------------------------------------

    def on_botonPagos_clicked(self, widget):
        pagos.CargarPagos()
        
# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    app = Index()
    gtk.main()
