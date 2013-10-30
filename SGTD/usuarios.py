#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: usuarios.py J.M.M. 21/03/2011 
Descripción: mantenimiento de los usuarios del sistema
"""

import gtk
import gtk.glade

import sistema
import users
from sistema import mensajes
from sistema import exportar

class Usuarios(object):

    def __init__(self):

        # Se carga el archivo glade con la ventana principal
        objsW = gtk.Builder()
        objsW.add_from_file('vistas/maestro.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winMain = objsW.get_object('winMain')
        self.vista = objsW.get_object('vista')
        self.comboBuscar = objsW.get_object('comboBuscar')
        self.winMain.set_title('Usuarios del Sistema')

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
        lista.append([2,'Usuario'])
        lista.append([3,'Nombre'])
        lista.append([4,'e-Mail'])

        self.comboBuscar.set_model(lista)
        render = gtk.CellRendererText() # Objeto que dibuja la celda, en este caso el elemento del combo
        self.comboBuscar.pack_start(render, True)
        self.comboBuscar.add_attribute(render, 'text', 1) # De los 2 campos, elegimos el segundo
        self.comboBuscar.set_active(0) # Lo posiciona en el primer item

    #--------------------------------------------------------------------------------------------

    def cargarVista(self, inicial):

        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        lista = gtk.ListStore(int,str,str,str,str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('ID', render, text=0)
        columna1 = gtk.TreeViewColumn('Usuario', render, text=1)
        columna2 = gtk.TreeViewColumn('Nombre', render, text=2)
        columna3 = gtk.TreeViewColumn('e-Mail', render, text=3)
        columna4 = gtk.TreeViewColumn('Clave', render, text=4)
        columna4.set_visible(False) # Para que no se vea por ventana

        # Lista donde cada elemento es un objeto usuario
        usuarios = users.obtenerTodos()
        if usuarios != None:
            for usuario in usuarios:
                lista.append([usuario.getId(), usuario.getUsername(), usuario.getName(), usuario.getEmail(), usuario.getPassword()])

        # Arma la vista con las columas y lista de elementos
        self.vista.set_model(lista)
        if inicial:
            self.vista.append_column(columna0)
            self.vista.append_column(columna1)
            self.vista.append_column(columna2)
            self.vista.append_column(columna3)
            self.vista.append_column(columna4)

            # Permite ordenar por columnas
            columna0.set_sort_column_id(0)
            columna1.set_sort_column_id(1)
            columna2.set_sort_column_id(2)
            columna3.set_sort_column_id(3)

            #self.vista.set_reorderable(True) # Permite drag and drop entre los datos

        self.on_comboBuscar_changed(self.comboBuscar) # Esto es para asignar la columna por la que se puede buscar
        self.vista.show()

    #--------------------------------------------------------------------------------------------

    def cargarEdit(self):

        # Se carga el archivo glade con la ventana de edición
        objsE = gtk.Builder()
        objsE.add_from_file('vistas/usuario.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winEdit = objsE.get_object('winEdit')
        self.textoUsuario = objsE.get_object('textoUsuario')
        self.textoNombre = objsE.get_object('textoNombre')
        self.textoMail = objsE.get_object('textoMail')
        # ID y Clave no son datos modificados por ventana
        self.identificador = None
        self.clave = None

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
        self.clave = ''
        self.winEdit.show() # Ventana de edición de los datos

    # -----------------------------------------------------------------------

    def on_botonEliminar_clicked(self, widget):

        (model,iter) = self.vista.get_selection().get_selected()
        if iter != None:
            conf = mensajes.pregunta(self.winMain, mensajes.DELETE)
            if conf:
                # Se recupera el ID, único campo necesario para eliminar
                fila = list(model[iter])
                if users.eliminar(fila[0]): mostrar = mensajes.aviso(self.winMain, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winMain, mensajes.OPER_NO)
                self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)

    # -----------------------------------------------------------------------

    def on_botonModificar_clicked(self, widget):

        (model,iter) = self.vista.get_selection().get_selected()
        if iter != None:
            self.cargarEdit() # Ventana de edición de los datos

            # Se asocian a los campos de edición los valores seleccionados
            fila = list(model[iter])
            self.textoUsuario.set_text(fila[1])
            self.textoNombre.set_text(fila[2])
            self.textoMail.set_text(fila[3])

            # ID y clave no son datos modificables, se mantienen sus valores
            self.identificador = fila[0]
            self.clave = fila[4]
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

        columnas = ['ID','Usuario','Nombre','e-Mail','Clave'] # Columnas para el archivo CSV
        model = self.vista.get_model()
        exportar.genCSV(model, columnas)

    # -----------------------------------------------------------------------

    def on_botonPDF_clicked(self, widget):

        columnas = ['Identificador','Usuario','Nombre','e-Mail','Clave'] # Columnas del encabezado
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
        if (self.textoUsuario.get_text() == '') or (self.textoNombre.get_text() == '') or (self.textoMail.get_text() == ''):
            mostrar = mensajes.error(self.winEdit, mensajes.DATOS_NO)
            ctrlOK = False
        else:
            # Se recuperan todos los datos, para ver si el usuario ya existe
            usuarios = users.obtenerTodos()
            if (usuarios != None):
                for u in usuarios:
                    if (u.getUsername() == self.textoUsuario.get_text()) and (u.getId() != self.identificador):
                        mostrar = mensajes.error(self.winEdit, mensajes.USER_EXISTE)
                        ctrlOK = False
        if (ctrlOK == True):
            # Los controles están OK, se crea o modifica el registro
            usuario = users.User()
            usuario.setUsername(self.textoUsuario.get_text())
            usuario.setName(self.textoNombre.get_text())
            usuario.setEmail(self.textoMail.get_text())
            # Los datos de ID y clave son los que se mantienen en variables
            usuario.setId(self.identificador)
            usuario.setPassword(self.clave)
            if (self.identificador == 0): # Es un registro nuevo
                if users.crear(usuario): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winEdit, mensajes.OPER_NO)
            else:
                if users.actualizar(usuario): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mensajes.error(self.winEdit, mensajes.OPER_NO)
            self.winEdit.destroy()
            self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)

    # -----------------------------------------------------------------------

# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    app = Usuarios()
    gtk.main()
