#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: proveedores.py 
Descripción: mantenimiento de los clientes y proveedores del sistema
"""

import gtk
import gtk.glade

import sistema
import modelo_proveedores
from sistema import mensajes
#from sistema import exportar

class Proveedores(object):

    def __init__(self):

        # Se carga el archivo glade con la ventana principal
        objsW = gtk.Builder()
        objsW.add_from_file('vistas/maestro.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winMain = objsW.get_object('winMain')
        self.vista = objsW.get_object('vista')
        self.comboBuscar = objsW.get_object('comboBuscar')
        self.winMain.set_title('Proveedores')

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
        lista.append([2,'Nombre/Razón Social'])
        lista.append([3,'Direccion'])
        lista.append([4,'RUC/Cedula'])
        lista.append([5,'Email'])
        lista.append([6,'Tipo Persona'])
        lista.append([7,'Teléfono'])

        self.comboBuscar.set_model(lista)
        render = gtk.CellRendererText() # Objeto que dibuja la celda, en este caso el elemento del combo
        self.comboBuscar.pack_start(render, True)
        self.comboBuscar.add_attribute(render, 'text', 1) # De los 2 campos, elegimos el segundo
        self.comboBuscar.set_active(0) # Lo posiciona en el primer item

    #--------------------------------------------------------------------------------------------

    def cargarVista(self, inicial):

        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        lista = gtk.ListStore(int,str,str,str,str,str,str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('ID', render, text=0)
        columna1 = gtk.TreeViewColumn('Nombre/Razón Social', render, text=1)
        columna2 = gtk.TreeViewColumn('Direccion', render, text=2)
        columna3 = gtk.TreeViewColumn('RUC/Cedula', render, text=3)
        columna4 = gtk.TreeViewColumn('Email', render, text=4)
        columna5 = gtk.TreeViewColumn('Tipo Persona', render, text=5)
        columna6 = gtk.TreeViewColumn('Teléfono', render, text=6)
        #columna6.set_visible(False) # Para que no se vea por ventana
        # Lista donde cada elemento es un objeto usuario
        proveedores = modelo_proveedores.obtenerTodos()
        if proveedores != None:
            for proveedor in proveedores:
                lista.append([proveedor.getId(), proveedor.getNombre(), proveedor.getDireccion(), proveedor.getRuc_Cedula(), proveedor.getEmail(), proveedor.getTipo(), proveedor.getTelefono()])

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
            
            # Permite ordenar por columnas
            columna0.set_sort_column_id(0)
            columna1.set_sort_column_id(1)
            columna2.set_sort_column_id(2)
            columna3.set_sort_column_id(3)
            columna4.set_sort_column_id(4)
            columna5.set_sort_column_id(5)
            columna6.set_sort_column_id(6)
            
            #self.vista.set_reorderable(True) # Permite drag and drop entre los datos

        self.on_comboBuscar_changed(self.comboBuscar) # Esto es para asignar la columna por la que se puede buscar
        self.vista.show()

    #--------------------------------------------------------------------------------------------
        
    def cargarEdit(self):

        # Se carga el archivo glade con la ventana de edición
        objsE = gtk.Builder()
        objsE.add_from_file('vistas/proveedor.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winEdit = objsE.get_object('winEdit')
        self.textoNombre = objsE.get_object('textoNombre')
        self.textoDir = objsE.get_object('textoDir')
        self.textoTel = objsE.get_object('textoTel')
        self.textoRUC = objsE.get_object('textoRUC')
        self.textoTipo = objsE.get_object('textoTipo')
        self.textoEma = objsE.get_object('textoEma')
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
                if modelo_proveedores.eliminar(fila[0]): mostrar = mensajes.aviso(self.winMain, mensajes.OPER_OK)
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
            self.textoDir.set_text(fila[2])
            self.textoRUC.set_text(fila[3])
            self.textoEma.set_text(fila[4])
            self.textoTipo.set_text(fila[5])
            self.textoTel.set_text(fila[6])
            

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
        if (self.textoNombre.get_text() == '') or (self.textoDir.get_text() == '') or (self.textoTel.get_text() == '') or (self.textoRUC.get_text() == ''):
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
            proveedor = modelo_proveedores.Proveedor()
            proveedor.setNombre(self.textoNombre.get_text())
            proveedor.setDireccion(self.textoDir.get_text())
            proveedor.setTelefono(self.textoTel.get_text())
            proveedor.setRuc_Cedula(self.textoRUC.get_text())
            proveedor.setTipo(self.textoTipo.get_text())
            
            proveedor.setEmail(self.textoEma.get_text())
                
            # Los datos de ID y clave son los que se mantienen en variables
            proveedor.setId(self.identificador)
            if (self.identificador == 0): # Es un registro nuevo
                if modelo_proveedores.crear(proveedor): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winEdit, mensajes.OPER_NO)
            else:
                if modelo_proveedores.actualizar(proveedor): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mensajes.error(self.winEdit, mensajes.OPER_NO)
            self.winEdit.destroy()
            self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)
    # -----------------------------------------------------------------------

class CargarProveedores(object):
    
    def __init__(self):
        
        objsE = gtk.Builder()
        objsE.add_from_file('vistas/proveedor.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winEdit = objsE.get_object('winEdit')
        self.textoNombre = objsE.get_object('textoNombre')
        self.textoDir = objsE.get_object('textoDir')
        self.textoTel = objsE.get_object('textoTel')
        self.textoRUC = objsE.get_object('textoRUC')
        self.textoTipo = objsE.get_object('textoTipo')
        self.textoEma = objsE.get_object('textoEma')
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
        if (self.textoNombre.get_text() == '') or (self.textoDir.get_text() == '') or (self.textoTel.get_text() == '') or (self.textoRUC.get_text() == ''):
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
            proveedor = modelo_proveedores.Proveedor()
            proveedor.setNombre(self.textoNombre.get_text())
            proveedor.setDireccion(self.textoDir.get_text())
            proveedor.setTelefono(self.textoTel.get_text())
            proveedor.setRuc_Cedula(self.textoRUC.get_text())
            proveedor.setTipo(self.textoTipo.get_text())
            
            proveedor.setEmail(self.textoEma.get_text())
                
            # Los datos de ID y clave son los que se mantienen en variables
            proveedor.setId(self.identificador)
            if (self.identificador == 0): # Es un registro nuevo
                if modelo_proveedores.crear(proveedor): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winEdit, mensajes.OPER_NO)
            else:
                if modelo_proveedores.actualizar(proveedor): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mensajes.error(self.winEdit, mensajes.OPER_NO)
            self.winEdit.destroy()
            self.cargarVista(False) 
            
    def on_winEdit_destroy(self, widget):
        self.winEdit.destroy()

    # -----------------------------------------------------------------------

    def on_botonCancel_clicked(self, widget):
        self.winEdit.destroy()
        
    def cargarVista(self, inicial):

        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        lista = gtk.ListStore(int,str,str,str,str,str,str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('ID', render, text=0)
        columna1 = gtk.TreeViewColumn('Nombre/Razón Social', render, text=1)
        columna2 = gtk.TreeViewColumn('Direccion', render, text=2)
        columna3 = gtk.TreeViewColumn('RUC/Cedula', render, text=3)
        columna4 = gtk.TreeViewColumn('Email', render, text=4)
        columna5 = gtk.TreeViewColumn('Tipo Persona', render, text=5)
        columna6 = gtk.TreeViewColumn('Teléfono', render, text=6)
        #columna6.set_visible(False) # Para que no se vea por ventana
        # Lista donde cada elemento es un objeto usuario
        proveedores = modelo_proveedores.obtenerTodos()
        if proveedores != None:
            for proveedor in proveedores:
                lista.append([proveedor.getId(), proveedor.getNombre(), proveedor.getDireccion(), proveedor.getRuc_Cedula(), proveedor.getEmail(), proveedor.getTipo(), proveedor.getTelefono()])

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
            
            # Permite ordenar por columnas
            columna0.set_sort_column_id(0)
            columna1.set_sort_column_id(1)
            columna2.set_sort_column_id(2)
            columna3.set_sort_column_id(3)
            columna4.set_sort_column_id(4)
            columna5.set_sort_column_id(5)
            columna6.set_sort_column_id(6)
            
            #self.vista.set_reorderable(True) # Permite drag and drop entre los datos

        self.on_comboBuscar_changed(self.comboBuscar) # Esto es para asignar la columna por la que se puede buscar
        self.vista.show()
    # -----------------------------------------------------------------------


# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    app = Proveedores()
    gtk.main()
