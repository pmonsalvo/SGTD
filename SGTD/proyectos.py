#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: proyectos.py J.M.M. 04/04/2011 
Descripción: mantenimiento de los proyectos del sistema
"""

import gtk

import sistema
import calendario
import proy_usr

from modelos import users
from modelos import projects
from sistema import mensajes
from sistema import exportar
from sistema import globalDef

class Proyectos(object):

    def __init__(self):

        # Se carga el archivo glade con la ventana principal
        objsW = gtk.Builder()
        objsW.add_from_file('vistas/maestro.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winMain = objsW.get_object('winMain')
        self.vista = objsW.get_object('vista')
        self.comboBuscar = objsW.get_object('comboBuscar')
        self.winMain.set_title('Proyectos del Sistema')

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
        lista.append([4,'Descripción'])
        lista.append([5,'Fecha'])

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
        columna3 = gtk.TreeViewColumn('Descripción', render, text=3)
        columna4 = gtk.TreeViewColumn('Fecha', render, text=4)

        # Lista donde cada elemento es un objeto proyecto
        proyectos = projects.obtenerTodos()
        if proyectos != None:
            for proyecto in proyectos:
                # Recupera el usuario del proyecto
                usuario = users.buscar(proyecto.getCreated_user_id())
                lista.append([proyecto.getId(), usuario.getName(), proyecto.getName(), proyecto.getDescription(), proyecto.getCreated()])

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
            columna4.set_sort_column_id(4)

            #self.vista.set_reorderable(True) # Permite drag and drop entre los datos

        self.on_comboBuscar_changed(self.comboBuscar) # Esto es para asignar la columna por la que se puede buscar
        self.vista.show()

    #--------------------------------------------------------------------------------------------

    def cargarEdit(self):

        # Se carga el archivo glade con la ventana de edición
        objsE = gtk.Builder()
        objsE.add_from_file('vistas/proyecto.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winEdit = objsE.get_object('winEdit')
        self.comboUsuario = objsE.get_object('comboUsuario')
        self.textoNombre = objsE.get_object('textoNombre')
        self.textoDesc = objsE.get_object('textoDesc')
        self.textoDescBuffer = self.textoDesc.get_buffer()
        self.textoFecha = objsE.get_object('textoFecha')

        # ID se iniciliza ya que no es dato que se vea en la ventana de edición 
        self.identificador = 0
        # El calendario se inicializa con la fecha actual
        self.calendario = calendario.Calendario(None, self.textoFecha)
        self.textoFecha.set_text(calendario.toStr(self.calendario.calendario.get_date()))

        # Se asocian las senales del archivo glade a metodos de la clase
        objsE.connect_signals(self)

    #--------------------------------------------------------------------------------------------

    def cargarComboUsuario(self,userID):

        lista = gtk.ListStore(int,str) # Combo de string.
        # Se usan para saber que elemento es el que se tiene que mostrar
        elemento = 0
        mostrar = 0

        # Se recorre la lista de usuarios para ir armando el combo, con el par ID - Nombre
        usuarios = users.obtenerTodos()
        if (usuarios != None):
            for u in usuarios:
                lista.append([u.getId(), u.getName()])
                if (u.getId() == userID): mostrar = elemento
                elemento = elemento + 1

            self.comboUsuario.set_model(lista)
            render = gtk.CellRendererText() # Objeto que dibuja la celda, en este caso el elemento del combo
            self.comboUsuario.pack_start(render, True)
            self.comboUsuario.add_attribute(render, 'text', 1) # De los 2 campos, elegimos el segundo
            self.comboUsuario.set_active(mostrar) # Lo posiciona en el primer item

    # ------------------- Eventos de la ventana principal -------------------

    # -----------------------------------------------------------------------

    def on_botonSalir_clicked(self, widget):
        self.winMain.destroy()

    # -----------------------------------------------------------------------

    def on_botonNuevo_clicked(self, widget):
        self.cargarEdit() # Ventana de edición de los datos
        self.cargarComboUsuario(0)
        # ID no es dato modificable, se inicializa
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
                proyID = fila[0]
                # Se recupera el proyecto para obtener el usuario del mismo
                proyecto = projects.buscar(proyID)
                usrID = proyecto.getCreated_user_id()
                # Solo se puede eliminar el proyecto del propio usuario
                if (usrID != globalDef.glb_usuario):
                    mostrar = mensajes.error(self.winMain, mensajes.USER_ACT)
                else:
                    if projects.eliminar(proyID): mostrar = mensajes.aviso(self.winMain, mensajes.OPER_OK)
                    else: mostrar = mensajes.error(self.winMain, mensajes.OPER_NO)
                    self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)

    # -----------------------------------------------------------------------

    def on_botonModificar_clicked(self, widget):

        (model,iter) = self.vista.get_selection().get_selected()
        if iter != None:
            self.cargarEdit() # Ventana de edición de los datos
            fila = list(model[iter])

            # Se busca el proyecto para recuperar sus datos (en la tabla no están todos)
            idProyecto = fila[0]
            proyecto = projects.buscar(idProyecto)
            usrID = proyecto.getCreated_user_id() # Para controlar si puede modificar

            # Solo se puede modificar el proyecto del propio usuario
            if (usrID != globalDef.glb_usuario):
                mostrar = mensajes.error(self.winMain, mensajes.USER_ACT)
            else:
                # Se asocian a los campos de edición los valores seleccionados
                self.identificador = proyecto.getId() # El ID no es dato modificable, se mantiene su valor
                self.cargarComboUsuario(proyecto.getCreated_user_id())
                self.textoNombre.set_text(proyecto.getName())
                self.textoDescBuffer.set_text(proyecto.getDescription())
                # Se toma la fecha en SQL y se pasa el dato a Tuple (el tipo de dato que maneja calendario)
                fechaTupla = calendario.toTuple(proyecto.getCreated())
                self.calendario.setFecha(fechaTupla)
                self.textoFecha.set_text(calendario.toStr(self.calendario.calendario.get_date()))

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

        columnas = ['ID','Usuario','Nombre','Descripción','Fecha'] # Columnas para el archivo CSV
        model = self.vista.get_model()
        exportar.genCSV(model, columnas)

    # -----------------------------------------------------------------------

    def on_botonPDF_clicked(self, widget):

        columnas = ['Identificador','Usuario','Nombre','Descripción','Fecha'] # Columnas del encabezado
        model = self.vista.get_model()
        exportar.genPDF(model, columnas, 'Proyectos del Sistema')

    # -----------------------------------------------------------------------

    def on_winMain_destroy(self, widget):
        self.winMain.destroy()

    # ------------------ Eventos de la ventana de Edición -------------------

    # -----------------------------------------------------------------------

    def on_winEdit_destroy(self, widget):
        self.winEdit.destroy()

    # -----------------------------------------------------------------------

    def on_botonFecha_clicked(self, widget):
        self.calendario.winMain.show()

    # -----------------------------------------------------------------------

    def on_botonCancel_clicked(self, widget):
        self.winEdit.destroy()

    # -----------------------------------------------------------------------

    def on_botonOK_clicked(self, widget):

        model = self.comboUsuario.get_model()
        userID = model[self.comboUsuario.get_active()][0]
        ini,fin = self.textoDescBuffer.get_bounds() # Iteradores con el inicio y fin del buffer de texto
        desc = self.textoDescBuffer.get_text(ini,fin)
        ctrlOK = True

        # Los datos no pueden estar vacíos. Usuario y fecha no se controlan porque tienen valores por defecto
        if (userID <= 0) or (self.textoNombre.get_text() == '') or (desc == ''):
            mostrar = mensajes.error(self.winEdit, mensajes.DATOS_NO)
            ctrlOK = False

        # El usuario del proyecto debe ser el usuario que ingreso al sistema
        if (userID != globalDef.glb_usuario):
            mostrar = mensajes.error(self.winEdit, mensajes.USER_NEW)
            ctrlOK = False
        

        if (ctrlOK == True):
            # Los controles están OK, se crea o modifica el registro
            proyecto = projects.Project()
            proyecto.setCreated_user_id(userID)
            proyecto.setName(self.textoNombre.get_text())
            proyecto.setDescription(desc)
            fechaMySQL = calendario.toMySQL(self.calendario.calendario.get_date())
            proyecto.setCreated(fechaMySQL)
            
            # El dato de ID se mantienen en variables, aunque no son usados para crear ni modificar
            proyecto.setId(self.identificador)
            if (self.identificador == 0): # Es un registro nuevo
                if projects.crear(proyecto): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winEdit, mensajes.OPER_NO)
            else:
                if projects.actualizar(proyecto): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mensajes.error(self.winEdit, mensajes.OPER_NO)
            self.winEdit.destroy()
            self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)

    # -----------------------------------------------------------------------

    def on_botonUsuarios_clicked(self, widget):
        if (self.identificador == 0): # Es un registro nuevo, no se puede asociar usuario, se debe crear
            mensajes.aviso(self.winEdit, mensajes.PROY_USR)
        else: proy_usr.Proy_Usr(self.identificador)

    # -----------------------------------------------------------------------

# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    app = Proyectos()
    gtk.main()
