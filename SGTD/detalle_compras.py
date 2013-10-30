#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: ventas.py 
Descripción: mantenimiento de las ventas del sistema
"""

import gtk
import gtk.glade

import sistema
import modelo_productos
import modelo_detalle_compras
import modelo_compras
import productos
import compras
import utils
from sistema import mensajes
#from sistema import exportar

class DetCompras(object):

    def __init__(self, nroF, ventana):

        # Se carga el archivo glade con la ventana principal
        objsW = gtk.Builder()
        objsW.add_from_file('vistas/detalle_compra.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winMain = objsW.get_object('winMain')
        self.vista = objsW.get_object('vista')
        self.spinCant = objsW.get_object('spinCant')
        self.textoPrecioU = objsW.get_object('textoPrecioU')
        self.winMain.set_title('Elija el Producto Comprado')

        # Se asocian las senales del archivo glade a metodos de la clase
        objsW.connect_signals(self)
        self.winMain.show()

        self.cargarVista(True) # Se llena la vista con los registros (True indica que es la carga inicial)

        self.compras = ventana
        self.fact = nroF
        
        self.lista = []
        self.listaProd = []
        self.total = 0

    #--------------------------------------------------------------------------------------------

    def cargarVista(self, inicial):

        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        lista = gtk.ListStore(int,str,str,str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('ID Producto', render, text=0)
        columna1 = gtk.TreeViewColumn('Nombre del Producto', render, text=1)
        columna2 = gtk.TreeViewColumn('Descripción', render, text=2)
        columna3 = gtk.TreeViewColumn('Precio de Compra', render, text=3)
        
        
        #columna6.set_visible(False) # Para que no se vea por ventana
        # Lista donde cada elemento es un objeto usuario
        productos = modelo_productos.obtenerTodos()
        if productos != None:
            for producto in productos:
                precio = utils.convertir_numero(int(producto.getCosto()))
                lista.append([producto.getId(), producto.getNombre(), producto.getDescripcion(), precio])

        # Arma la vista con las columas y lista de elementos
        self.vista.set_model(lista)
        if inicial:
            self.vista.append_column(columna0)
            self.vista.append_column(columna1)
            self.vista.append_column(columna2)
            self.vista.append_column(columna3)
            
            # Permite ordenar por columnas
            columna0.set_sort_column_id(0)
            columna1.set_sort_column_id(1)
            columna2.set_sort_column_id(2)
            columna3.set_sort_column_id(3)
            
            
            
            #self.vista.set_reorderable(True) # Permite drag and drop entre los datos

        self.vista.show()
    
    
    #--------------------------------------------------------------------------------------------
    
    # ------------------- Eventos de la ventana principal -------------------

    # -----------------------------------------------------------------------

    def on_botonSalir_clicked(self, widget):
        self.winMain.destroy()

    # -----------------------------------------------------------------------


    def on_winMain_destroy(self, widget):
        self.winMain.destroy()

    # ------------------ Eventos de la ventana de Edición -------------------

    # -----------------------------------------------------------------------

    def on_botonCancel_clicked(self, widget):
        self.winMain.destroy()

    # -----------------------------------------------------------------------
    
    def on_botonNewProducto_clicked(self, widget):
        productos.CargarProductos()

    # -----------------------------------------------------------------------
    def on_botonOK_clicked(self, widget):
        (model, iter) = self.vista.get_selection().get_selected()
        if iter != None:
            self.listaProd = []
            fila = list(model[iter])
            idProducto = fila[0]
            producto = modelo_productos.buscar(idProducto)
            cant = self.spinCant.get_value_as_int()
            factura = modelo_detalle_compras.DetCompra()
            factura.setIdFactura(self.fact)
            factura.setIdProducto(producto.getId())
            if(cant != 0): 
                factura.setCantidad(cant)
            else:
                mostrar = mensajes.error(self.winMain, mensajes.CANT_ERR)
            factura.setDescripcion(producto.getNombre() + ' ' + producto.getDescripcion())
            factura.setPrecioU(int(self.textoPrecioU.get_text()))
            factura.setImporte(cant*int(self.textoPrecioU.get_text()))
            self.listaProd.append(factura)
            self.total = self.total + (cant*int(self.textoPrecioU.get_text()))
            tupla = tuple(self.listaProd)
            self.compras.cargarListadoProductos(tupla, self.total)
            self.lista.append(factura)
                
        tupla = tuple(self.lista)
        self.compras.ProductosCompra(tupla)
        
       
        
            
    # -----------------------------------------------------------------------

# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    app = DetCompras()
    gtk.main()
