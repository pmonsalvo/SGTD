#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: medio_pago.py 
Descripción: mantenimiento de los medios de pago del módulo ventas.
"""

import gtk
import gtk.glade

import sistema
import modelo_clientes
import modelo_cuentas
import calendario
from sistema import mensajes
from datetime import date, timedelta
import utils
#from sistema import exportar

class Medio_Pago(object):

    def __init__(self):

        # Se carga el archivo glade con la ventana principal
        objsW = gtk.Builder()
        objsW.add_from_file('vistas/maestro.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winMain = objsW.get_object('winMain')
        self.vista = objsW.get_object('vista')
        self.comboBuscar = objsW.get_object('comboBuscar')
        self.winMain.set_title('Medios de Pago')

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
        lista.append([2,'Medio de Pago'])
        lista.append([3,'Número de Factura'])
        lista.append([4,'Cliente'])
        lista.append([5,'Monto a Pagar'])
        
        
        self.comboBuscar.set_model(lista)
        render = gtk.CellRendererText() # Objeto que dibuja la celda, en este caso el elemento del combo
        self.comboBuscar.pack_start(render, True)
        self.comboBuscar.add_attribute(render, 'text', 1) # De los 2 campos, elegimos el segundo
        self.comboBuscar.set_active(0) # Lo posiciona en el primer item

    #--------------------------------------------------------------------------------------------

    
    def cargarVista(self, inicial):

        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        lista = gtk.ListStore(int,str,int,str,str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('ID', render, text=0)
        columna1 = gtk.TreeViewColumn('Medio de Pago', render, text=1)
        columna2 = gtk.TreeViewColumn('Número de Factura', render, text=2)
        columna3 = gtk.TreeViewColumn('Cliente', render, text=3)
        columna4 = gtk.TreeViewColumn('Monto a Pagar', render, text=4)
        
        
        
        #columna6.set_visible(False) # Para que no se vea por ventana
        # Lista donde cada elemento es un objeto usuario
        medios = modelo_medios_pago.obtenerTodos()
        if medios != None:
            for medio in medios:
                cliente = modelo_clientes.buscar(medio.getIdCliente)
                factura = modelo_ventas.buscar(medio.getIdNroFactura)
                lista.append([medio.getIdMedio_Pago(), medio.getTipo_Pago(), factura.getIdFactura(), cliente.getNombre(), medio.getTotal()])

        # Arma la vista con las columas y lista de elementos
        self.vista.set_model(lista)
        if inicial:
            self.vista.append_column(columna0)
            self.vista.append_column(columna1)
            self.vista.append_column(columna2)
            self.vista.append_column(columna3)
            self.vista.append_column(columna4)
            
            
            self.vista.columns_autosize()
            
            # Permite ordenar por columnas
            columna0.set_sort_column_id(0)
            columna1.set_sort_column_id(1)
            columna2.set_sort_column_id(2)
            columna3.set_sort_column_id(3)
            columna4.set_sort_column_id(4)
            
           
            
            
            
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
                if modelo_medios_pago.eliminar(fila[0]): mostrar = mensajes.aviso(self.winMain, mensajes.OPER_OK)
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
class CargarMedioPagos(object):        
    
    def __init__(self, cli, fact, total):

        # Se carga el archivo glade con la ventana de edición
        objsE = gtk.Builder()
        objsE.add_from_file('vistas/forma_pago.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winEdit = objsE.get_object('winEdit')
        self.notebookMedio = objsE.get_object('notebookMedio')
        self.labelFactura = objsE.get_object('labelFactura')
        self.labelCliente = objsE.get_object('labelCliente')
        self.labelTotal = objsE.get_object('labelTotal')
        self.checkDescuento = objsE.get_object('checkDescuento')
        self.textoDescuento = objsE.get_object('textoDescuento')
        self.labelDescontado = objsE.get_object('labelDescontado')
        self.textoBanco = objsE.get_object('textoBanco')
        self.textoNroCheque = objsE.get_object('textoNroCheque')
        self.checkCredito = objsE.get_object('checkCredito')
        self.checkDebito = objsE.get_object('checkDebito')
        self.textoCodAut = objsE.get_object('textoCodAut')
        self.textoEmisor = objsE.get_object('textoEmisor')
        self.textoPagarC = objsE.get_object('textoPagarC')
        self.textoPagarCH = objsE.get_object('textoPagarCH')
        self.textoPagarT = objsE.get_object('textoPagarT')
        self.labelSaldo = objsE.get_object('labelSaldo')
        
        # ID y Clave no son datos modificados por ventana
        self.winEdit.set_title('Seleccione el Medio de Pago Correspondiente')
        self.identificador = 0
        self.cliente = cli
        self.total = total
        cliente = modelo_clientes.buscar(cli)
        self.labelCliente.set_text(cliente.getNombre())
        self.labelFactura.set_text(str(fact))
        self.toal = utils.convertir_numero(total)
        self.labelSaldo.set_text(self.toal)
        self.labelTotal.set_text(str(self.toal))
        self.textoDescuento.set_sensitive(False)
        self.aux = 0
        
        # Se asocian las senales del archivo glade a metodos de la clase
        objsE.connect_signals(self)
        
        self.winEdit.show()
        
    """def cargarComboCuotas(self):
        
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
        self.comboCuotas.pack_start(render, True)
        self.comboCuotas.add_attribute(render, 'text', 0) # De los 2 campos, elegimos el segundo
        self.comboCuotas.set_active(0) # Lo posiciona en el primer item
        
    def on_comboCuotas_changed(self, widget):
        index = self.comboCuotas.get_active() + 1
        if(self.checkEntrega.get_active() == True and self.textoEntrega.get_text != ''):
            entrega = int(self.textoEntrega.get_text())
            total = int(self.total)
            if(entrega < total):
                saldo = total - entrega
                self.monto_cuotas = saldo/index
                monC = utils.convertir_numero(self.monto_cuotas)
                self.labelMonto.set_text(str(monC))
        else:
            self.monto_cuotas = int(self.labelTotal.get_text())/index
            monC = utils.copnvertir_numero(self.monto_cuotas)
            self.labelMonto.set_text(str(monC))"""        
    
    def on_checkDescuento_toggled(self, widget):
        if(self.checkDescuento.get_active() == True):
            self.textoDescuento.set_sensitive(True)
        else:
            self.textoDescuento.set_sensitive(False)
            self.labelTotal.set_text(self.toal)
            
    def on_textoDescuento_changed(self,widget):
        if(self.textoDescuento.get_text() != ''):
            porc_desc = int(self.textoDescuento.get_text())
            descuento = self.total * porc_desc /100
            self.labelDescontado.set_text(str(descuento))
            totalDesc = self.total - descuento
            td = utils.convertir_numero(totalDesc)
            self.labelTotal.set_text(td)
        else:
            self.labelTotal.set_text(self.toal)
            
    def on_textoPagarC_changed(self,widget):
        if(self.textoPagarCH.get_text() == '' and self.textoPagarT.get_text() == ''):
            if(self.textoPagarC.get_text() == ''):
                contado = 0
            else:
                contado = int(self.textoPagarC.get_text())
            saldo = self.total - contado
            if(contado != 0):
                if(contado > self.total):
                    print 'Aquí irá un mensaje de error'
                elif (saldo == 0):
                    self.labelSaldo.set_text('0')
                    self.textoBanco.set_sensitive(False)
                    self.textoNroCheque.set_sensitive(False)
                    self.textoPagarCH.set_sensitive(False)
                    self.checkCredito.set_sensitive(False)
                    self.checkDebito.set_sensitive(False)
                    self.textoCodAut.set_sensitive(False)
                    self.textoEmisor.set_sensitive(False)
                    self.textoPagarT.set_sensitive(False)
                else:
                    self.aux = saldo
                    s = utils.convertir_numero(saldo)
                    self.labelSaldo.set_text(s)
                    self.textoBanco.set_sensitive(True)
                    self.textoNroCheque.set_sensitive(True)
                    self.textoPagarCH.set_sensitive(True)
                    self.checkCredito.set_sensitive(True)
                    self.checkDebito.set_sensitive(True)
                    self.textoCodAut.set_sensitive(True)
                    self.textoEmisor.set_sensitive(True)
                    self.textoPagarT.set_sensitive(True)
        else:
            contado = int(self.textoPagarC.get_text())
            saldo = self.aux - contado
            if(contado != ''):
                if(contado > self.total):
                    print 'Aquí va un mensaje de Error'
                elif(saldo == 0):
                    self.labelSaldo.set_text('0')
                    self.textoBanco.set_sensitive(False)
                    self.textoNroCheque.set_sensitive(False)
                    self.textoPagarCH.set_sensitive(False)
                    self.checkCredito.set_sensitive(False)
                    self.checkDebito.set_sensitive(False)
                    self.textoCodAut.set_sensitive(False)
                    self.textoEmisor.set_sensitive(False)
                    self.textoPagarT.set_sensitive(False)
                else:
                    self.aux = saldo
                    s = utils.convertir_numero(saldo)
                    self.labelSaldo.set_text(s)
                    self.textoBanco.set_sensitive(True)
                    self.textoNroCheque.set_sensitive(True)
                    self.textoPagarCH.set_sensitive(True)
                    self.checkCredito.set_sensitive(True)
                    self.checkDebito.set_sensitive(True)
                    self.textoCodAut.set_sensitive(True)
                    self.textoEmisor.set_sensitive(True)
                    self.textoPagarT.set_sensitive(True)
                    
    def on_textoPagarCH_changed(self,widget):
        if(self.textoPagarC.get_text() == '' and self.textoPagarT.get_text() == ''):
            if(self.textoPagarCH.get_text() == ''):
                contado = 0
            else:
                contado = int(self.textoPagarCH.get_text())
            saldo = self.total - contado
            if(contado != 0):
                if(contado > self.total):
                    print 'Aquí irá un mensaje de error'
                elif (saldo == 0):
                    self.labelSaldo.set_text('0')
                    self.checkDescuento.set_sensitive(False)
                    self.textoPagarC.set_sensitive(False)
                    self.checkCredito.set_sensitive(False)
                    self.checkDebito.set_sensitive(False)
                    self.textoCodAut.set_sensitive(False)
                    self.textoEmisor.set_sensitive(False)
                    self.textoPagarT.set_sensitive(False)
                else:
                    self.aux = saldo
                    s = utils.convertir_numero(saldo)
                    self.labelSaldo.set_text(s)
                    self.checkDescuento.set_sensitive(True)
                    self.textoPagarC.set_sensitive(True)
                    self.checkCredito.set_sensitive(True)
                    self.checkDebito.set_sensitive(True)
                    self.textoCodAut.set_sensitive(True)
                    self.textoEmisor.set_sensitive(True)
                    self.textoPagarT.set_sensitive(True)
        else:
            contado = int(self.textoPagarCH.get_text())
            saldo = self.aux - contado
            if(contado != ''):
                if(contado > self.total):
                    print 'Aquí va un mensaje de Error'
                elif(saldo == 0):
                    self.labelSaldo.set_text('0')
                    self.checkDescuento.set_sensitive(False)
                    self.textoPagarC.set_sensitive(False)
                    self.checkCredito.set_sensitive(False)
                    self.checkDebito.set_sensitive(False)
                    self.textoCodAut.set_sensitive(False)
                    self.textoEmisor.set_sensitive(False)
                    self.textoPagarT.set_sensitive(False)
                else:
                    self.aux = saldo
                    s = utils.convertir_numero(saldo)
                    self.labelSaldo.set_text(s)
                    self.checkDescuento.set_sensitive(True)
                    self.textoPagarC.set_sensitive(True)
                    self.checkCredito.set_sensitive(True)
                    self.checkDebito.set_sensitive(True)
                    self.textoCodAut.set_sensitive(True)
                    self.textoEmisor.set_sensitive(True)
                    self.textoPagarT.set_sensitive(True)    
                    
    def on_textoPagarT_changed(self,widget):
        if(self.textoPagarC.get_text() == '' and self.textoPagarCH.get_text() == ''):
            if(self.textoPagarT.get_text() == ''):
                contado = 0
            else:
                contado = int(self.textoPagarT.get_text())
            saldo = self.total - contado
            if(contado != 0):
                if(contado > self.total):
                    print 'Aquí irá un mensaje de error'
                elif (saldo == 0):
                    self.labelSaldo.set_text('0')
                    self.checkDescuento.set_sensitive(False)
                    self.textoPagarC.set_sensitive(False)
                    self.textoBanco.set_sensitive(False)
                    self.textoNroCheque.set_sensitive(False)
                    self.textoPagarCH.set_sensitive(False)
                    
                else:
                    self.aux = saldo
                    s = utils.convertir_numero(saldo)
                    self.labelSaldo.set_text(s)
                    self.checkDescuento.set_sensitive(True)
                    self.textoPagarC.set_sensitive(True)
                    self.textoBanco.set_sensitive(True)
                    self.textoNroCheque.set_sensitive(True)
                    self.textoPagarCH.set_sensitive(True)
                    
        else:
            contado = int(self.textoPagarT.get_text())
            saldo = self.aux - contado
            if(contado != ''):
                if(contado > self.total):
                    print 'Aquí va un mensaje de Error'
                elif(saldo == 0):
                    self.labelSaldo.set_text('0')
                    self.checkDescuento.set_sensitive(False)
                    self.textoPagarC.set_sensitive(False)
                    self.textoBanco.set_sensitive(False)
                    self.textoNroCheque.set_sensitive(False)
                    self.textoPagarCH.set_sensitive(False)
                else:
                    s = utils.convertir_numero(saldo)
                    self.labelSaldo.set_text(s)
                    self.checkDescuento.set_sensitive(True)
                    self.textoPagarC.set_sensitive(True)
                    self.textoBanco.set_sensitive(True)
                    self.textoNroCheque.set_sensitive(True)
                    self.textoPagarCH.set_sensitive(True)
                    

    def cargarVista(self, inicial):

        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        lista = gtk.ListStore(int,int,str,str,str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('ID', render, text=0)
        columna1 = gtk.TreeViewColumn('Número de Factura', render, text=1)
        columna2 = gtk.TreeViewColumn('Cliente', render, text=2)
        columna3 = gtk.TreeViewColumn('Tipo de Medio de Pago', render, text=3)
        columna4 = gtk.TreeViewColumn('Monto a Pagar', render, text=4)
        
        medios = modelo_medios_pago.obtenerTodos()
        if medios != None:
            for medio in medios:
                cliente = modelo_clientes.buscar(medio.getIdCliente)
                factura = modelo_ventas.buscar(medio.getIdNroFactura)
                lista.append([medio.getIdMedio_Pago(), medio.getTipo_Pago(), factura.getIdFactura(), cliente.getNombre(), medio.getTotal()])

        # Arma la vista con las columas y lista de elementos
        self.vista.set_model(lista)
        if inicial:
            self.vista.append_column(columna0)
            self.vista.append_column(columna1)
            self.vista.append_column(columna2)
            self.vista.append_column(columna3)
            self.vista.append_column(columna4)
            
            
            self.vista.columns_autosize()
            
            # Permite ordenar por columnas
            columna0.set_sort_column_id(0)
            columna1.set_sort_column_id(1)
            columna2.set_sort_column_id(2)
            columna3.set_sort_column_id(3)
            columna4.set_sort_column_id(4)
            
           
            
            
            
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
        
        pagina = self.notebookMedio.get_current_page()
        ctrlOK = True
        if(pagina == 1):
            if(self.checkDescuento.get_active() == True and self.textoDescuento.get_text() == ''):
                mostrar = mensajes.error(self.winEdit, mensajes.DATOS_NO)
                ctrlOK = False
        
            if (ctrlOK == True):
                # Los controles están OK, se crea o modifica el registro
                medio = modelo_medios_pago.Medios_Pagos()
                medio.setIdNroFactura(int(self.labelFactura.get_text()))
                medio.setIdCliente(self.cliente)
                medio.setTotal(self.total)
                medio.setPorcDesc(int(self.textoDescuento.get_text()))
                medio.setDescuento(int(self.labelDescontado.get_text()))
                medio.setTipo_Pago('Contado')
                
                    
            # Los datos de ID y clave son los que se mantienen en variables
            cuenta.setIdCuentas(self.identificador)
           
            
            if (self.identificador == 0): # Es un registro nuevo
                
                if modelo_cuentas.crear(cuenta): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winEdit, mensajes.OPER_NO)
            else:
                
                if modelo_cuentas.actualizar(cuenta): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mensajes.error(self.winEdit, mensajes.OPER_NO)
            self.winEdit.destroy()
            #self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)

    # -----------------------------------------------------------------------

# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    app = Cuentas()
    gtk.main()
