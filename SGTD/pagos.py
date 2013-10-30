#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: clientes.py 
Descripción: mantenimiento de los clientes del sistema
"""

import gtk
import gtk.glade

import sistema
import modelo_clientes
import modelo_cuentas
import calendario
import cuentas
from sistema import mensajes
from datetime import date, timedelta
import utils
#from sistema import exportar

class Cuentas(object):

    def __init__(self):

        # Se carga el archivo glade con la ventana principal
        objsW = gtk.Builder()
        objsW.add_from_file('vistas/maestro.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winMain = objsW.get_object('winMain')
        self.vista = objsW.get_object('vista')
        self.comboBuscar = objsW.get_object('comboBuscar')
        self.winMain.set_title('Pagos')

        # Se asocian las senales del archivo glade a metodos de la clase
        objsW.connect_signals(self)
        self.winMain.show()

        self.cargarCombo() # Se carga el combo de buscar con los nombres de las columnas
        self.cargarVista(True) # Se llena la vista con los registros (True indica que es la carga inicial)

    #--------------------------------------------------------------------------------------------

    def cargarCombo(self):

        lista = gtk.ListStore(int,str) # Combo de string.
        # Se arma la lista con los valores del combo, son las columnas de la vista
        lista.append([1,'Número Factura'])
        lista.append([2,'Cliente'])
        lista.append([3,'Número de Cuota'])
        lista.append([4,'Monto'])
        lista.append([5,'Fecha de Vencimiento'])
        lista.append([6,'Próximo Vencimiento'])
        
        self.comboBuscar.set_model(lista)
        render = gtk.CellRendererText() # Objeto que dibuja la celda, en este caso el elemento del combo
        self.comboBuscar.pack_start(render, True)
        self.comboBuscar.add_attribute(render, 'text', 1) # De los 2 campos, elegimos el segundo
        self.comboBuscar.set_active(0) # Lo posiciona en el primer item

    #--------------------------------------------------------------------------------------------

    
    def cargarVista(self, inicial):

        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        lista = gtk.ListStore(int,str,str,int,str,str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('Número de Factura', render, text=0)
        columna1 = gtk.TreeViewColumn('Cliente', render, text=1)
        columna2 = gtk.TreeViewColumn('Número de Cuota', render, text=2)
        columna3 = gtk.TreeViewColumn('Monto', render, text=3)
        columna4 = gtk.TreeViewColumn('Fecha de Vencimiento', render, text=4)
        columna5 = gtk.TreeViewColumn('Próximo Vencimiento', render, text=5)
        
        
        #columna6.set_visible(False) # Para que no se vea por ventana
        # Lista donde cada elemento es un objeto usuario
        pagos = modelo_pagos.obtenerTodos()
        if pagos != None:
            for pago in pagos:
                cliente = modelo_clientes.buscar(pago.getIdCliente)
                lista.append([pago.getIdFactura(), cliente.getNombre(), pago.getNroCuota(), pago.getMonto(), pago.getVenc(), pago.getProxVenc()])

        # Arma la vista con las columas y lista de elementos
        self.vista.set_model(lista)
        if inicial:
            self.vista.append_column(columna0)
            self.vista.append_column(columna1)
            self.vista.append_column(columna2)
            self.vista.append_column(columna3)
            self.vista.append_column(columna4)
            self.vista.append_column(columna5)
            
            self.vista.columns_autosize()
            
            # Permite ordenar por columnas
            columna0.set_sort_column_id(0)
            columna1.set_sort_column_id(1)
            columna2.set_sort_column_id(2)
            columna3.set_sort_column_id(3)
            columna4.set_sort_column_id(4)
            columna5.set_sort_column_id(5)
           
            
            
            
            #self.vista.set_reorderable(True) # Permite drag and drop entre los datos

        self.on_comboBuscar_changed(self.comboBuscar) # Esto es para asignar la columna por la que se puede buscar
        self.vista.show()
        
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
                if modelo_cuentas.eliminar(fila[0]): mostrar = mensajes.aviso(self.winMain, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winMain, mensajes.OPER_NO)
                self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)

    # -----------------------------------------------------------------------

    def on_botonModificar_clicked(self, widget):

        (model,iter) = self.vista.get_selection().get_selected()
        if iter != None:
            self.cargarEdit() # Ventana de edición de los datos

            # Se asocian a los campos de edición los valores seleccionados
            fila = list(model[iter])
            self.labelCliente.set_text(fila[1])
            self.labelFactura.set_text(fila[2])
            self.spinPagos.set_text(fila[3])
            self.labelMonto.set_text(fila[4])
            self.labelTotal.set_text(fila[5])
            self.treeviewVenc.set_text(fila[6])
            
            
            
            

            # ID y clave no son datos modificables, se mantienen sus valores
            self.identificador = fila[0]
            
            #self.textoNombre.set_property('editable', False) # Cuando se modifica, el usuario no de puede cambiar
            #self.cargarVista(False)
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
        if (self.spinPagos.get_value_as_int() == 0):
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
            cuenta = modelo_cuentas.Cuenta()
            cuenta.setIdFactura(self.labelFactura.get_text())
            cuenta.setIdCliente(self.labelCliente.get_text())
            cuenta.setCuotas(self.spinCuentas.get_value_as_int())
            cuenta.setFecha_Venc(self.textoFecha.get_text())
            cuenta.setTotal(self.labelTotal.get_text())
            cuenta.setEntrega(self.textoEntrega.get_text())
                
            # Los datos de ID y clave son los que se mantienen en variables
            cuenta.setId(self.identificador)
            if (self.identificador == 0): # Es un registro nuevo
                if modelo_cuentas.crear(cuenta): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winEdit, mensajes.OPER_NO)
            else:
                if modelo_cuentas.actualizar(cuenta): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mensajes.error(self.winEdit, mensajes.OPER_NO)
            self.winEdit.destroy()
            self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)

    # -----------------------------------------------------------------------
    def cargarComboCuotas(self):
        lista = gtk.ListStore(int) # Combo de string.
        # Se arma la lista con los valores del combo, son las columnas de la vista
        lista.append([1])
        lista.append([2])
        lista.append([3])
        lista.append([4])
        lista.append([5])
        lista.append([6])
        
        self.comboCuotas.set_model(lista)
        render = gtk.CellRendererText() # Objeto que dibuja la celda, en este caso el elemento del combo
        self.comboBuscar.pack_start(render, True)
        self.comboBuscar.add_attribute(render, 'text', 0) # De los 2 campos, elegimos el segundo
        self.comboBuscar.set_active(0) # Lo posiciona en el primer item

    #--------------------------------------------------------------------------------------------
class CargarPagos(object):        
    
    def __init__(self):

        # Se carga el archivo glade con la ventana de edición
        objsE = gtk.Builder()
        objsE.add_from_file('vistas/pagos.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winEdit = objsE.get_object('winEdit')
        self.textoFactura = objsE.get_object('textoFactura')
        self.labelNroFactura = objsE.get_object('labelNroFactura')
        self.labelCliente = objsE.get_object('labelCliente')
        self.labelNroCuota = objsE.get_object('labelNroCuota')
        self.labelMonto = objsE.get_object('labelMonto')
        self.textoFecha = objsE.get_object('textoFecha')
        self.labelProxVenc = objsE.get_object('labelProxVenc')
        self.labelVenc = objsE.get_object('labelVenc')
        # ID y Clave no son datos modificados por ventana
        self.winEdit.set_title('Pagos')
       
        
        # Se asocian las senales del archivo glade a metodos de la clase
        objsE.connect_signals(self)
        
        self.winEdit.show()
        
    def cargarCuentas(self):
        
        objsE = gtk.Builder()
        objsE.add_from_file('vistas/detalle_cuentas.glade')
        
        self.winEdit = objsE.get_object('winEdit')
        self.vista = objsE.get_object('vista')
        
        lista = gtk.ListStore(int,str,str,int,str,int,int,str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('ID', render, text=0)
        columna1 = gtk.TreeViewColumn('Cliente', render, text=1)
        columna2 = gtk.TreeViewColumn('Número de Cédula/RUC' , render, text=2)
        columna3 = gtk.TreeViewColumn('Número de Factura', render, text=3)
        columna4 = gtk.TreeViewColumn('Cantidad de Pagos', render, text=4)
        columna5 = gtk.TreeViewColumn('Monto a Pagar (Fraccionado)', render, text=5)
        columna6 = gtk.TreeViewColumn('Monto Total', render, text=6)
        columna7 = gtk.TreeViewColumn('Estado', render, text=7)
        
        
        #columna6.set_visible(False) # Para que no se vea por ventana
        # Lista donde cada elemento es un objeto usuario
        cuentas = modelo_cuentas.obtenerTodos()
        if cuentas != None:
            for cuenta in cuentas:
                cliente = modelo_clientes.buscar(cuenta.getIdCliente())
                lista.append([cuenta.getIdCuentas(), cliente.getNombre(), cliente.getRuc_Cedula(), cuenta.getIdFactura(), cuenta.getCuotas(), cuenta.getMonto(), cuenta.getTotal(), cuenta.getEstado()])

        # Arma la vista con las columas y lista de elementos
        self.vista.set_model(lista)
        #if inicial:
        self.vista.append_column(columna0)
        self.vista.append_column(columna1)
        self.vista.append_column(columna2)
        self.vista.append_column(columna3)
        self.vista.append_column(columna4)
        self.vista.append_column(columna5)
        self.vista.append_column(columna6)
        self.vista.append_column(columna7)
            
        self.vista.columns_autosize()
            
            # Permite ordenar por columnas
        columna0.set_sort_column_id(0)
        columna1.set_sort_column_id(1)
        columna2.set_sort_column_id(2)
        columna3.set_sort_column_id(3)
        columna4.set_sort_column_id(4)
        columna5.set_sort_column_id(5)
        columna6.set_sort_column_id(6)
        columna7.set_sort_column_id(7)
           
            
            
            
            #self.vista.set_reorderable(True) # Permite drag and drop entre los datos

        #self.on_comboBuscar_changed(self.comboBuscar) # Esto es para asignar la columna por la que se puede buscar
        self.vista.show()
        self.winEdit.show()
        
    def on_botonCuentas_clicked(self, widget):
        self.cargarCuentas()
        nroFact = self.textoFactura.get_text()
        self.buscar(nroFact)
        
    def buscar(self, texto):
        """
        Realiza una Búsqueda sobre el treeview.
        """
            
        model = self.vista.get_model()
        item = model.get_iter_first()
        
                
        if not item: return
    
        self.vista.get_selection().select_iter(item)
        first_path = model.get_path(item)
        self.vista.scroll_to_cell(first_path)
        
        padres = []
        self.posibles = []
        
        while item:
            valor = model.get_value(item, 2)
            print valor

            if texto in valor:
                self.posibles.append(item)
            
            if model.iter_has_child(item):
                path = model.get_path(item)
                self.expand_to_path(path)
                
                """if item not in padres:
                    padres.append(item)"""
                    
            item = model.iter_next(item)
        
        """if padres != []:
            for padre in padres:
                item = model.iter_children(padre)
                
                while item:
                    valor = model.get_value(item, 2)
                    valorT = str(valor)
                    
                    if str(texto) in valorT:
                        self.posibles.append(item)
                        
                    item = model.iter_next(item)"""

        if self.posibles != []:
            self.vista.get_selection().select_iter(self.posibles[0])
            new_path = model.get_path(self.posibles[0])
            self.vista.scroll_to_cell(new_path)
        self.vista.show()
           
    def on_checkEntrega_toggled(self, widget):
        if(self.checkEntrega.get_active() == True):
            self.textoEntrega.set_sensitive(True)
        else:
            self.textoEntrega.set_sensitive(False)
            
    def on_botonCalendario_clicked(self, widget):
        calendario.Calendario(None, self.textoFecha)
            
    def on_textoDias_changed(self,widget):
        fecha = date.today() + timedelta(days = int(self.textoDias.get_text()))
        fechaV = fecha.strftime("%d/%m/%Y")
        self.labelVenc.set_text(str(fechaV))
        


    def cargarVistaVenc(self):
        lista = gtk.ListStore(int,str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('Cuota Nro.', render, text=0)
        columna1 = gtk.TreeViewColumn('Fecha de Vencimiento', render, text=1)
        
        index = self.comboCuotas.get_active() + 1
        
        
        if productos != None:
            for producto in productos:
                lista.append([producto.getId(), producto.getNombre(), producto.getDescripcion(), producto.getPrecio(), producto.getStock_Act()])

        # Arma la vista con las columas y lista de elementos
        self.vistaP.set_model(lista)
        if inicial:
            self.vistaP.append_column(columna0)
            self.vistaP.append_column(columna1)
            self.vistaP.append_column(columna2)
            self.vistaP.append_column(columna3)
            self.vistaP.append_column(columna4)
            
            # Permite ordenar por columnas
            columna0.set_sort_column_id(0)
            columna1.set_sort_column_id(1)
            columna2.set_sort_column_id(2)
            columna3.set_sort_column_id(3)
            columna4.set_sort_column_id(4)
            
            
            #self.vista.set_reorderable(True) # Permite drag and drop entre los datos

        self.vistaP.show()
        
    def cargarVista(self, inicial):

        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        lista = gtk.ListStore(int,str,str,str,str,str,str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('ID', render, text=0)
        columna1 = gtk.TreeViewColumn('Cliente', render, text=1)
        columna2 = gtk.TreeViewColumn('Número de Factura', render, text=2)
        columna3 = gtk.TreeViewColumn('Cantidad de Pagos', render, text=3)
        columna4 = gtk.TreeViewColumn('Monto a Pagar (Fraccionado)', render, text=4)
        columna5 = gtk.TreeViewColumn('Monto Total', render, text=5)
        
        
        #columna6.set_visible(False) # Para que no se vea por ventana
        # Lista donde cada elemento es un objeto usuario
        cuentas = modelo_cuentas.obtenerTodos()
        if cuentas != None:
            for cuenta in cuentas:
                cliente = modelo_clientes.buscar(cuenta.getIdCliente)
                lista.append([cuenta.getIdCuentas(), cliente.getNombre(), cuenta.getIdFactura(), cuenta.getCuotas(), cuenta.getMonto(), cuenta.getTotal()])

        # Arma la vista con las columas y lista de elementos
        self.vista.set_model(lista)
        if inicial:
            self.vista.append_column(columna0)
            self.vista.append_column(columna1)
            self.vista.append_column(columna2)
            self.vista.append_column(columna3)
            self.vista.append_column(columna4)
            self.vista.append_column(columna5)
            
            self.vista.columns_autosize()
            
            # Permite ordenar por columnas
            columna0.set_sort_column_id(0)
            columna1.set_sort_column_id(1)
            columna2.set_sort_column_id(2)
            columna3.set_sort_column_id(3)
            columna4.set_sort_column_id(4)
            columna5.set_sort_column_id(5)
           
            
            
            
            #self.vista.set_reorderable(True) # Permite drag and drop entre los datos

        self.on_comboBuscar_changed(self.comboBuscar) # Esto es para asignar la columna por la que se puede buscar
        self.vista.show()
    # ------------------ Eventos de la ventana de Edición -------------------

    # -----------------------------------------------------------------------

    def on_winEdit_destroy(self, widget):
        self.winEdit.destroy()
        
    # -----------------------------------------------------------------------

    def on_botonCancel_clicked(self, widget):
        self.winEdit.destroy()

    # -----------------------------------------------------------------------

    def on_botonOK_clicked(self, widget):
        dias = int(self.textoDias.get_text())

        ctrlOK = True
        # Los datos no pueden estar vacíos
        if (self.textoEntrega.get_text == '' or self.textoDias.get_text == ''):
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
            cuotas = self.comboCuotas.get_active() + 1 
            #self.listaCuenta = []
            for i in range(cuotas):
                cuenta = modelo_cuentas.Cuenta()
                cuenta.setIdFactura(int(self.labelFactura.get_text()))
                cuenta.setIdCliente(self.cliente)
                cuenta.setCuotas(self.comboCuotas.get_active() + 1)
                cuenta.setMonto(self.montoCuotas)
                cuenta.setFecha_Venc(self.labelVenc.get_text())
                cuenta.setTotal(self.total)
                cuenta.setEntrega(self.textoEntrega.get_text())
                    
            # Los datos de ID y clave son los que se mantienen en variables
                cuenta.setIdCuentas(self.identificador)
                if (self.identificador == 0 and i == cuotas):
                    if modelo_cuentas.crear(cuenta): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                    else: mostrar = mensajes.error(self.winEdit, mensajes.OPER_NO)
                elif (self.identificador == 0 and i < cuotas):
                    modelo_cuentas.crear(cuenta)
                    dias = dias + int(self.textoDias.get_text())
                    fecha = date.today() + timedelta(days = dias)
                    fechaV = fecha.strftime("%d/%m/%Y")
                    self.labelVenc.set_text(str(fechaV))
                else:
                    if modelo_cuentas.actualizar(cuenta): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                    else: mensajes.error(self.winEdit, mensajes.OPER_NO)
                
            """if (self.identificador == 0): # Es un registro nuevo
                
                if modelo_cuentas.crear(cuenta): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winEdit, mensajes.OPER_NO)
            else:
                
                if modelo_cuentas.actualizar(cuenta): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mensajes.error(self.winEdit, mensajes.OPER_NO)"""
                
            self.winEdit.destroy()
            #self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)

    # -----------------------------------------------------------------------

# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    app = Cuentas()
    gtk.main()
