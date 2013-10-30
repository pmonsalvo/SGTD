#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: productos.py 
Descripción: mantenimiento de los productos del sistema
"""

import gtk
import gtk.glade

import sistema
import modelo_productos
from sistema import mensajes
#from sistema import exportar

class Productos(object):

    def __init__(self):

        # Se carga el archivo glade con la ventana principal
        objsW = gtk.Builder()
        objsW.add_from_file('vistas/maestro.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winMain = objsW.get_object('winMain')
        self.vista = objsW.get_object('vista')
        self.comboBuscar = objsW.get_object('comboBuscar')
        self.winMain.set_title('Productos')

        # Se asocian las senales del archivo glade a metodos de la clase
        objsW.connect_signals(self)
        self.winMain.show()

        self.cargarCombo() # Se carga el combo de buscar con los nombres de las columnas
        self.cargarVista(True) # Se llena la vista con los registros (True indica que es la carga inicial)

    #--------------------------------------------------------------------------------------------

    def cargarCombo(self):

        lista = gtk.ListStore(int,str) # Combo de string.
        # Se arma la lista con los valores del combo, son las columnas de la vista
        lista.append([1,'ID'])
        lista.append([2,'Nombre'])
        lista.append([3,'Descripción'])
        lista.append([4,'Precio'])
        lista.append([5,'Costo'])
        lista.append([6,'IVA'])
        lista.append([7,'Porcentaje Comisión'])
        lista.append([8,'Stock Mínimo'])
        lista.append([9,'Stock Actual'])
        lista.append([10,'Descuento'])

        self.comboBuscar.set_model(lista)
        render = gtk.CellRendererText() # Objeto que dibuja la celda, en este caso el elemento del combo
        self.comboBuscar.pack_start(render, True)
        self.comboBuscar.add_attribute(render, 'text', 1) # De los 2 campos, elegimos el segundo
        self.comboBuscar.set_active(0) # Lo posiciona en el primer item

    #--------------------------------------------------------------------------------------------

    def cargarVista(self, inicial):

        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        lista = gtk.ListStore(int,str,str,str,str,str,str, str, str, str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('ID', render, text=0)
        columna1 = gtk.TreeViewColumn('Nombre', render, text=1)
        columna2 = gtk.TreeViewColumn('Descripción', render, text=2)
        columna3 = gtk.TreeViewColumn('Precio', render, text=3)
        columna4 = gtk.TreeViewColumn('Costo', render, text=4)
        columna5 = gtk.TreeViewColumn('IVA', render, text=5)
        columna6 = gtk.TreeViewColumn('Comisión', render, text=6)
        columna7 = gtk.TreeViewColumn('Stock Actual', render, text=7)
        columna8 = gtk.TreeViewColumn('Stock Mínimo', render, text=8)
        columna9 = gtk.TreeViewColumn('Descuento' , render, text=9)
        #columna6.set_visible(False) # Para que no se vea por ventana
        # Lista donde cada elemento es un objeto usuario
        productos = modelo_productos.obtenerTodos()
        if productos != None:
            for producto in productos:
                lista.append([producto.getId(), producto.getNombre(), producto.getDescripcion(), producto.getPrecio(), producto.getCosto(), producto.getIVA(), producto.getComision(), producto.getStock_Act(), producto.getStock(), producto.getDescuento()])

        # Arma la vista con las columas y lista de elementos
        self.vista.set_model(lista)
        if inicial:
            self.vista.append_column(columna0)
            self.vista.append_column(columna1)
            self.vista.append_column(columna2)
            self.vista.append_column(columna3)
            self.vista.append_column(columna4)
            self.vista.append_column(columna5)
            self.vista.append_column(columna6)
            self.vista.append_column(columna7)
            self.vista.append_column(columna8)
            self.vista.append_column(columna9)
            
            # Permite ordenar por columnas
            columna0.set_sort_column_id(0)
            columna1.set_sort_column_id(1)
            columna2.set_sort_column_id(2)
            columna3.set_sort_column_id(3)
            columna4.set_sort_column_id(4)
            columna5.set_sort_column_id(5)
            columna6.set_sort_column_id(6)
            columna7.set_sort_column_id(7)
            columna8.set_sort_column_id(8)
            columna9.set_sort_column_id(9)
            #self.vista.set_reorderable(True) # Permite drag and drop entre los datos

        self.on_comboBuscar_changed(self.comboBuscar) # Esto es para asignar la columna por la que se puede buscar
        self.vista.show()

    #--------------------------------------------------------------------------------------------
        
    def cargarEdit(self):

        # Se carga el archivo glade con la ventana de edición
        objsE = gtk.Builder()
        objsE.add_from_file('vistas/producto.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winEdit = objsE.get_object('winEdit')
        self.textoNombre = objsE.get_object('textoNombre')
        self.textoDes = objsE.get_object('textoDes')
        self.textoPre = objsE.get_object('textoPre')
        self.textoCos = objsE.get_object('textoCos')
        self.textoIVA = objsE.get_object('textoIVA')
        self.textoCom = objsE.get_object('textoCom')
        self.textoAct = objsE.get_object('textoAct')
        self.textoMin = objsE.get_object('textoMin')
        self.textoDesc = objsE.get_object('textoDesc')
        # ID y Clave no son datos modificados por ventana
        self.identificador = None
        

        # Se asocian las senales del archivo glade a metodos de la clase
        objsE.connect_signals(self)

    # ------------------- Eventos de la ventana principal -------------------

    # -----------------------------------------------------------------------

    def on_botonSalir_clicked(self, widget):
        self.winMain.destroy()

    # -----------------------------------------------------------------------

    def on_botonNuevo_clicked(self, widget):
        self.cargarEdit() # Ventana de edición de los datos
        # ID y clave no son datos modificables, se inicializan
        self.identificador = 0
        self.winEdit.show() # Ventana de edición de los datos

    # -----------------------------------------------------------------------

    def on_botonEliminar_clicked(self, widget):

        (model,iter) = self.vista.get_selection().get_selected()
        if iter != None:
            conf = mensajes.pregunta(self.winMain, mensajes.DELETE)
            if conf:
                # Se recupera el ID, único campo necesario para eliminar
                fila = list(model[iter])
                if modelo_productos.eliminar(fila[0]): mostrar = mensajes.aviso(self.winMain, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winMain, mensajes.OPER_NO)
                self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)

    # -----------------------------------------------------------------------

    def on_botonModificar_clicked(self, widget):

        (model,iter) = self.vista.get_selection().get_selected()
        if iter != None:
            self.cargarEdit() # Ventana de edición de los datos

            # Se asocian a los campos de edición los valores seleccionados
            fila = list(model[iter])
            self.textoNombre.set_text(fila[1])
            self.textoDes.set_text(fila[2])
            self.textoPre.set_text(fila[3])
            self.textoCos.set_text(fila[4])
            self.textoIVA.set_text(fila[5])
            self.textoCom.set_text(fila[6])
            self.textoAct.set_text(fila[7])
            self.textoMin.set_text(fila[8])
            self.textoDesc.set_text(fila[9])
            
            
            

            # ID y clave no son datos modificables, se mantienen sus valores
            self.identificador = fila[0]
            
            #self.textoUsuario.set_property('editable', False) # Cuando se modifica, el usuario no de puede cambiar
            
            self.winEdit.show() # Ventana de edición de los datos

    # -----------------------------------------------------------------------

    def on_comboBuscar_changed(self, widget):

        model = self.comboBuscar.get_model()
        elemento = self.comboBuscar.get_active()
        if elemento >= 0:
            #print (model[elemento][0])
            self.vista.set_search_column(elemento) # Columna por la que es posible buscar
        else:
            self.vista.set_search_column(0) # Por defecto ID

    # -----------------------------------------------------------------------

    def on_botonExportar_clicked(self, widget):

        columnas = ['ID','Nombre/Razón Social','Direccion','RUC/Cedula','Email', 'Tipo Persona', 'Teléfono'] # Columnas para el archivo CSV
        model = self.vista.get_model()
        exportar.genCSV(model, columnas)

    # -----------------------------------------------------------------------

    def on_botonPDF_clicked(self, widget):

        columnas = ['Identificador','Nombre/Razón Social','Direccion','RUC/Cédula','Email', 'Tipo Persona', 'Teléfono'] # Columnas del encabezado
        model = self.vista.get_model()
        exportar.genPDF(model, columnas, mensajes.TITLE_PDF)

    # -----------------------------------------------------------------------

    def on_winMain_destroy(self, widget):
        self.winMain.destroy()

    # ------------------ Eventos de la ventana de Edición -------------------

    # -----------------------------------------------------------------------

    def on_winEdit_destroy(self, widget):
        self.winEdit.destroy()

    # -----------------------------------------------------------------------

    def on_botonCancel_clicked(self, widget):
        self.winEdit.destroy()

    # -----------------------------------------------------------------------

    def on_botonOK_clicked(self, widget):

        ctrlOK = True
        # Los datos no pueden estar vacíos
        if (self.textoNombre.get_text() == '') or (self.textoDes.get_text() == '') or (self.textoPre.get_text() == '') or (self.textoCos.get_text() == '') or (self.textoIVA.get_text() == '') or (self.textoCom.get_text() == '') or (self.textoMin.get_text() == '') or (self.textoDesc.get_text() == ''):
            mostrar = mensajes.error(self.winEdit, mensajes.DATOS_NO)
            ctrlOK = False
        """else:
            # Se recuperan todos los datos, para ver si el usuario ya existe
            personas = modelo_personas.obtenerTodos()
            if (personas != None):
                for u in personas:
                    if (u.getNombre() == self.textoNombre.get_text()) and (u.getId() != self.identificador):
                        mostrar = mensajes.error(self.winEdit, mensajes.USER_EXISTE)
                        ctrlOK = False"""
        if (ctrlOK == True):
            # Los controles están OK, se crea o modifica el registro
            producto= modelo_productos.Producto()
            producto.setNombre(self.textoNombre.get_text())
            producto.setDescripcion(self.textoDes.get_text())
            producto.setPrecio(self.textoPre.get_text())
            producto.setCosto(self.textoCos.get_text())
            producto.setIVA(self.textoIVA.get_text())
            producto.setComision(self.textoCom.get_text())
            producto.setStock(self.textoMin.get_text())
            producto.setDescuento(self.textoDesc.get_text())
            producto.setStock_Act(self.textoAct.get_text())
            # Los datos de ID y clave son los que se mantienen en variables
            producto.setId(self.identificador)
            if (self.identificador == 0): # Es un registro nuevo
                if modelo_productos.crear(producto): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winEdit, mensajes.OPER_NO)
            else:
                if modelo_productos.actualizar(producto): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mensajes.error(self.winEdit, mensajes.OPER_NO)
            self.winEdit.destroy()
            self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)

    # -----------------------------------------------------------------------
    
class CargarProductos(object):
    
    def __init__(self):
        
        objsE = gtk.Builder()
        objsE.add_from_file('vistas/producto.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winEdit = objsE.get_object('winEdit')
        self.textoNombre = objsE.get_object('textoNombre')
        self.textoDes = objsE.get_object('textoDes')
        self.textoPre = objsE.get_object('textoPre')
        self.textoCos = objsE.get_object('textoCos')
        self.textoIVA = objsE.get_object('textoIVA')
        self.textoCom = objsE.get_object('textoCom')
        self.textoAct = objsE.get_object('textoAct')
        self.textoMin = objsE.get_object('textoMin')
        self.textoDesc = objsE.get_object('textoDesc')
        # ID y Clave no son datos modificados por ventana
        self.identificador = None
        

        # Se asocian las senales del archivo glade a metodos de la clase
        objsE.connect_signals(self)
        self.winEdit.show()
        
    def on_winEdit_destroy(self, widget):
        self.winEdit.destroy()

    # -----------------------------------------------------------------------

    def on_botonCancel_clicked(self, widget):
        self.winEdit.destroy()

    # -----------------------------------------------------------------------

    def on_botonOK_clicked(self, widget):

        ctrlOK = True
        # Los datos no pueden estar vacíos
        if (self.textoNombre.get_text() == '') or (self.textoDes.get_text() == '') or (self.textoPre.get_text() == '') or (self.textoCos.get_text() == '') or (self.textoIVA.get_text() == '') or (self.textoCom.get_text() == '') or (self.textoMin.get_text() == '') or (self.textoDesc.get_text() == ''):
            mostrar = mensajes.error(self.winEdit, mensajes.DATOS_NO)
            ctrlOK = False
        """else:
            # Se recuperan todos los datos, para ver si el usuario ya existe
            personas = modelo_personas.obtenerTodos()
            if (personas != None):
                for u in personas:
                    if (u.getNombre() == self.textoNombre.get_text()) and (u.getId() != self.identificador):
                        mostrar = mensajes.error(self.winEdit, mensajes.USER_EXISTE)
                        ctrlOK = False"""
        if (ctrlOK == True):
            # Los controles están OK, se crea o modifica el registro
            producto= modelo_productos.Producto()
            producto.setNombre(self.textoNombre.get_text())
            producto.setDescripcion(self.textoDes.get_text())
            producto.setPrecio(self.textoPre.get_text())
            producto.setCosto(self.textoCos.get_text())
            producto.setIVA(self.textoIVA.get_text())
            producto.setComision(self.textoCom.get_text())
            producto.setStock(self.textoMin.get_text())
            producto.setDescuento(self.textoDesc.get_text())
            producto.setStock_Act(self.textoAct.get_text())
            # Los datos de ID y clave son los que se mantienen en variables
            producto.setId(self.identificador)
            if (self.identificador == 0): # Es un registro nuevo
                if modelo_productos.crear(producto): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winEdit, mensajes.OPER_NO)
            else:
                if modelo_productos.actualizar(producto): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mensajes.error(self.winEdit, mensajes.OPER_NO)
            self.winEdit.destroy()
            self.cargarVista(False)
            
    def cargarVista(self, inicial):

        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        lista = gtk.ListStore(int,str,str,str,str,str,str, str, str, str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('ID', render, text=0)
        columna1 = gtk.TreeViewColumn('Nombre', render, text=1)
        columna2 = gtk.TreeViewColumn('Descripción', render, text=2)
        columna3 = gtk.TreeViewColumn('Precio', render, text=3)
        columna4 = gtk.TreeViewColumn('Costo', render, text=4)
        columna5 = gtk.TreeViewColumn('IVA', render, text=5)
        columna6 = gtk.TreeViewColumn('Comisión', render, text=6)
        columna7 = gtk.TreeViewColumn('Stock Actual', render, text=7)
        columna8 = gtk.TreeViewColumn('Stock Mínimo', render, text=8)
        columna9 = gtk.TreeViewColumn('Descuento' , render, text=9)
        #columna6.set_visible(False) # Para que no se vea por ventana
        # Lista donde cada elemento es un objeto usuario
        productos = modelo_productos.obtenerTodos()
        if productos != None:
            for producto in productos:
                lista.append([producto.getId(), producto.getNombre(), producto.getDescripcion(), producto.getPrecio(), producto.getCosto(), producto.getIVA(), producto.getComision(), producto.getStock_Act(), producto.getStock(), producto.getDescuento()])

        # Arma la vista con las columas y lista de elementos
        self.vista.set_model(lista)
        if inicial:
            self.vista.append_column(columna0)
            self.vista.append_column(columna1)
            self.vista.append_column(columna2)
            self.vista.append_column(columna3)
            self.vista.append_column(columna4)
            self.vista.append_column(columna5)
            self.vista.append_column(columna6)
            self.vista.append_column(columna7)
            self.vista.append_column(columna8)
            self.vista.append_column(columna9)
            
            # Permite ordenar por columnas
            columna0.set_sort_column_id(0)
            columna1.set_sort_column_id(1)
            columna2.set_sort_column_id(2)
            columna3.set_sort_column_id(3)
            columna4.set_sort_column_id(4)
            columna5.set_sort_column_id(5)
            columna6.set_sort_column_id(6)
            columna7.set_sort_column_id(7)
            columna8.set_sort_column_id(8)
            columna9.set_sort_column_id(9)
            #self.vista.set_reorderable(True) # Permite drag and drop entre los datos

        self.on_comboBuscar_changed(self.comboBuscar) # Esto es para asignar la columna por la que se puede buscar
        self.vista.show()
        
        
# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    app = Productos()
    gtk.main()
