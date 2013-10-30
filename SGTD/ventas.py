#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Archivo: ventas.py 
Descripción: mantenimiento de los ventas del sistema
"""

import gtk
import gtk.glade

import sistema
import modelo_ventas
import modelo_clientes
import modelo_vendedores
import modelo_productos
import detalle_ventas
import modelo_detalle_ventas
import clientes
import calendario
import utils
import cuentas
import medio_pago
from sistema import mensajes
#from sistema import exportar

class Ventas(object):

    def __init__(self):

        # Se carga el archivo glade con la ventana principal
        objsW = gtk.Builder()
        objsW.add_from_file('vistas/maestro.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winMain = objsW.get_object('winMain')
        self.vista = objsW.get_object('vista')
        self.comboBuscar = objsW.get_object('comboBuscar')
        self.winMain.set_title('Ventas')

        # Se asocian las senales del archivo glade a metodos de la clase
        objsW.connect_signals(self)
        self.winMain.show()

        self.cargarCombo() # Se carga el combo de buscar con los nombres de las columnas
        self.cargarVista(True) # Se llena la vista con los registros (True indica que es la carga inicial)
        self.total = 0
#--------------------------------------------------------------------------------------------

    def cargarCombo(self):

        lista = gtk.ListStore(int,str) # Combo de string.
        # Se arma la lista con los valores del combo, son las columnas de la vista
        lista.append([1,'Nro. Factura'])
        lista.append([2,'Condición de Venta'])
        lista.append([3,'Cliente'])
        lista.append([4,'Vendedor'])
        
        self.comboBuscar.set_model(lista)
        render = gtk.CellRendererText() # Objeto que dibuja la celda, en este caso el elemento del combo
        self.comboBuscar.pack_start(render, True)
        self.comboBuscar.add_attribute(render, 'text', 1) # De los 2 campos, elegimos el segundo
        self.comboBuscar.set_active(0) # Lo posiciona en el primer item

    #--------------------------------------------------------------------------------------------

    def cargarVista(self, inicial):

        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        lista = gtk.ListStore(int,str,str,str,str,str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('Nro. de Factura', render, text=0)
        columna1 = gtk.TreeViewColumn('Fecha de Emisión', render, text=1)
        columna2 = gtk.TreeViewColumn('Condición de Venta', render, text=2)
        columna3 = gtk.TreeViewColumn('Cliente', render, text=3)
        columna4 = gtk.TreeViewColumn('Vendedor', render, text=4)
        columna5 = gtk.TreeViewColumn('Total', render, text=5)
        
        #columna6.set_visible(False) # Para que no se vea por ventana
        # Lista donde cada elemento es un objeto usuario
        ventas = modelo_ventas.obtenerTodos()
        if ventas != None:
            for venta in ventas:
                cliente = modelo_clientes.buscar(venta.getCliente())
                vendedor = modelo_vendedores.buscar(venta.getVendedor())
                #total = utils.convertir_numero(int(venta.getTotal()))
                lista.append([venta.getId(), venta.getFecha(), venta.getTipo(), cliente.getNombre(), vendedor.getNombre(), venta.getTotal()])

        # Arma la vista con las columas y lista de elementos
        self.vista.set_model(lista)
        if inicial:
            self.vista.append_column(columna0)
            self.vista.append_column(columna1)
            self.vista.append_column(columna2)
            self.vista.append_column(columna3)
            self.vista.append_column(columna4)
            self.vista.append_column(columna5)
            
            
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

    #--------------------------------------------------------------------------------------------
    
    
    #--------------------------------------------------------------------------------------------
    def ListaProductos(self, inicial):
        
        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        self.lista = gtk.ListStore(int,int,str,int,int) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('Código Producto', render, text=0)
        columna1 = gtk.TreeViewColumn('Cantidad', render, text=1)
        columna2 = gtk.TreeViewColumn('Descripción', render, text=2)
        columna3 = gtk.TreeViewColumn('Precio Unitario', render, text=3)
        columna4 = gtk.TreeViewColumn('Importe', render, text=4)
        
        #columna6.set_visible(False) # Para que no se vea por ventana
        # Lista donde cada elemento es un objeto usuario
        
        self.treeview1.set_model(self.lista)
        if inicial:
            self.treeview1.append_column(columna0)
            self.treeview1.append_column(columna1)
            self.treeview1.append_column(columna2)
            self.treeview1.append_column(columna3)
            self.treeview1.append_column(columna4)
            
            
            # Permite ordenar por columnas
            columna0.set_sort_column_id(0)
            columna1.set_sort_column_id(1)
            columna2.set_sort_column_id(2)
            columna3.set_sort_column_id(3)
            columna4.set_sort_column_id(4)
            
            #columna0.add_attribute(render,"editable",0)
            
            #self.vista.set_reorderable(True) # Permite drag and drop entre los datos

        self.treeview1.show()
    #--------------------------------------------------------------------------------------------
    def cargarListadoProductos(self, prod):
        
        
        if prod != None:
            for producto in prod:
                precioU = utils.convertir_numero(producto.getPrecioU())
                importe = utils.convertir_numero(producto.getImporte())
                self.lista.append([producto.getIdProducto(), producto.getCantidad(), producto.getDescripcion(), producto.getPrecioU(), producto.getImporte()])
                self.total = self.total + producto.getImporte()
        # Arma la vista con las columas y lista de elementos
        self.totalSinC = self.total
        subT = int(self.total/1.1)
        iva = self.total - subT
        subT = utils.convertir_numero(subT)
        iva = utils.convertir_numero(iva)
        total = utils.convertir_numero(self.total)
        self.labelIVA.set_text(str(iva))
        self.labelSub.set_text(str(subT))
        self.labelTotal.set_text(str(total))
        
        
        
    #--------------------------------------------------------------------------------------------
    
    def cargarVistaProductos(self, inicial):
        
        # Tipos de dato de cada columna. ListStore es el modelo del TreeView, en este caso, lista. Podria ser Tree.
        lista = gtk.ListStore(int,str,str,str,str) # ID, usuario, nombre, mail, clave
        render = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit = gtk.CellRendererText() # Objeto que se encarga de dibujar cada celda
        #renderEdit.set_property('editable', True)

        # Columnas de la vista
        columna0 = gtk.TreeViewColumn('ID Producto', render, text=0)
        columna1 = gtk.TreeViewColumn('Nombre Producto', render, text=1)
        columna2 = gtk.TreeViewColumn('Descripción', render, text=2)
        columna3 = gtk.TreeViewColumn('Precio Unitario', render, text=3)
        columna4 = gtk.TreeViewColumn('Stock Actual', render, text=4)
        
        #columna6.set_visible(False) # Para que no se vea por ventana
        # Lista donde cada elemento es un objeto usuario
        productos = modelo_productos.obtenerTodos()
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
    
    #--------------------------------------------------------------------------------------------
        
    def cargarEdit(self):

        # Se carga el archivo glade con la ventana de edición
        objsE = gtk.Builder()
        objsE.add_from_file('vistas/factura_venta.glade')

        # Se recuperan los widget a usar (no son necesarios todos)
        self.winEdit = objsE.get_object('winEdit')
        self.textoFecha = objsE.get_object('textoFecha')
        self.checkContado = objsE.get_object('checkContado')
        self.checkCredito = objsE.get_object('checkCredito')
        self.comboCliente = objsE.get_object('comboCliente')
        self.comboVendedor = objsE.get_object('comboVendedor')
        self.labelRUC = objsE.get_object('labelRUC')
        self.labelTelefono = objsE.get_object('labelTelefono')
        self.labelDireccion = objsE.get_object('labelDireccion')
        self.labelFactura = objsE.get_object('labelFactura')
        self.labelSub = objsE.get_object('labelSub')
        self.labelIVA = objsE.get_object('labelIVA')
        self.labelTotal = objsE.get_object('labelTotal')
        self.treeview1 = objsE.get_object('treeview1')
        
       
        # ID y Clave no son datos modificados por ventana
        self.identificador = None
        ventas = modelo_ventas.ultimo()
        self.labelFactura.set_text(str(ventas+1))
        self.winEdit.maximize()
     
        
                

        # Se asocian las senales del archivo glade a metodos de la clase
        objsE.connect_signals(self)
        
    def devolver_ultimo(self):
        return self.labelFactura.set_text(str(ventas+1))
        
    def cargarProductos(self):
        detalle_ventas.DetVentas(ventana=self)
        
    def ProductosVenta(self, vendidos):
        self.prodVenta = vendidos
        
        
        
    def cargarComboCliente(self,clienteID, data=None):
       self.lista = gtk.ListStore(int,str)
       elemento = 0
       mostrar = 0
       cliente = modelo_clientes.obtenerTodos()
       if (cliente != None):
            for u in cliente:
                self.lista.append([u.getId(), u.getNombre()])
                if(u.getId() == clienteID): mostrar = elemento
                elemento = elemento + 1
                
            self.comboCliente.set_model(self.lista)
            render = gtk.CellRendererText()
            self.comboCliente.pack_start(render, True)
            self.comboCliente.add_attribute(render,'text', 1)
            self.comboCliente.set_active(mostrar)
        
                    
    def cargarComboVendedor(self,vendedorID, data=None):
        
        lista = gtk.ListStore(int,str)
        elemento = 0
        mostrar = 0
        vendedor = modelo_vendedores.obtenerTodos()
        if(vendedor != None):
            for u in vendedor:
                lista.append([u.getId(), u.getNombre()])
                if(u.getId() == vendedorID): mostrar = elemento
                elemento = elemento + 1
                
            self.comboVendedor.set_model(lista)
            render = gtk.CellRendererText()
            self.comboVendedor.pack_start(render, True)
            self.comboVendedor.add_attribute(render, 'text', 1)
            self.comboVendedor.set_active(mostrar)      
            
    
    # ------------------- Eventos de la ventana principal -------------------

    # -----------------------------------------------------------------------

    def on_botonSalir_clicked(self, widget):
        self.winMain.destroy()
    
    # -----------------------------------------------------------------------
    
    def on_comboCliente_changed(self, widget):
        
        nro_id = self.comboCliente.get_active() + 2
        cliente = modelo_clientes.buscar(nro_id)
        self.labelRUC.set_text(cliente.getRuc_Cedula())
        self.labelDireccion.set_text(cliente.getDireccion())
        self.labelTelefono.set_text(cliente.getTelefono())
    # -----------------------------------------------------------------------

    def on_botonNuevo_clicked(self, widget):
        self.cargarEdit() # Ventana de edición de los datos
        self.cargarComboCliente(0)
        self.cargarComboVendedor(0)
        self.ListaProductos(True)
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
                ventaID = fila[0]
                venta = modelo_ventas.buscar(ventaID)
                modelo_detalle_ventas.eliminar(ventaID)
                #clienteID = modelo_ventas.getCliente()
                #vendedorID = modelo_ventas.getVendedor()
                if modelo_ventas.eliminar(ventaID): mostrar = mensajes.aviso(self.winMain, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winMain, mensajes.OPER_NO)
                self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)

    # -----------------------------------------------------------------------

    def on_botonModificar_clicked(self, widget):

        (model,iter) = self.vista.get_selection().get_selected()
        if iter != None:
            self.cargarEdit() # Ventana de edición de los datos
            fila = list(model[iter])
            
            idVenta = fila[0]
            venta = modelo_ventas.buscar(idVenta)
            

            # Se asocian a los campos de edición los valores seleccionados
            self.identificador = venta.getId()
            self.textoFecha.set_text(venta.getFecha())
            if (venta.getTipo() == 'Contado'): 
                self.checkContado.set_active(True)
            else: 
                self.checkCredito.set_active(True)
            self.cargarComboCliente(venta.getCliente())
            self.cargarComboVendedor(venta.getVendedor())
            self.labelFactura.set_text(str(self.identificador))
            tup = modelo_detalle_ventas.buscar(self.identificador)
            self.ListaProductos(True)
            self.cargarListadoProductos(tup)
            total = venta.getTotal()
            subtotal = int(int(total)/1.1)
            iva = int(total) - subtotal
            self.labelTotal.set_text(str(total))
            self.labelIVA.set_text(str(iva))
            self.labelSub.set_text(str(subtotal))
            
            # ID y clave no son datos modificables, se mantienen sus valores
            
            
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
    def on_botonCalendario_clicked(self, widget):
        calendario.Calendario(None, self.textoFecha)
    # -----------------------------------------------------------------------

    def on_winMain_destroy(self, widget):
        self.winMain.destroy()

    # ------------------ Eventos de la ventana de Edición -------------------

    # -----------------------------------------------------------------------

    def on_winEdit_destroy(self, widget):
        self.winEdit.destroy()

    # -----------------------------------------------------------------------

    def on_botonCancel_clicked(self, widget):
        self.labelIVA.set_text('0')
        self.labelSub.set_text('0')
        self.labelTotal.set_text('0')
        self.winEdit.destroy()

    # -----------------------------------------------------------------------
    
    def on_botonNewProducto_clicked(self, widget):
        self.cargarProductos()
    
    # -----------------------------------------------------------------------
    
    def on_botonOK_clicked(self, widget):
        cliente = self.comboCliente.get_model()
        clienteID = cliente[self.comboCliente.get_active()][0]
        vendedor = self.comboVendedor.get_model()
        vendedorID = vendedor[self.comboVendedor.get_active()][0]
        ctrlOK = True
        # Los datos no pueden estar vacíos
        if (self.textoFecha.get_text() == '') or (self.checkContado.get_active() == True and self.checkCredito.get_active() == True) or (self.checkContado.get_active() == False and self.checkCredito.get_active() == False):
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
            detalle_venta = modelo_detalle_ventas.DetVenta()
            venta = modelo_ventas.Venta()
            venta.setCliente(clienteID)
            venta.setVendedor(vendedorID)
            venta.setFecha(self.textoFecha.get_text())
            if (self.checkContado.get_active() == True):
                venta.setTipo('Contado')
            else:
                venta.setTipo('Crédito')
                            
            # Los datos de ID y clave son los que se mantienen en variables
            venta.setTotal(self.labelTotal.get_text())
            venta.setId(self.identificador)
            if (self.identificador == 0): # Es un registro nuevo
                if modelo_ventas.crear(venta): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mostrar = mensajes.error(self.winEdit, mensajes.OPER_NO)
                if self.prodVenta != None:
                    for pv in self.prodVenta:
                        detalle_venta.setIdFactura(int(self.labelFactura.get_text()))
                        detalle_venta.setIdProducto(pv.getIdProducto())
                        detalle_venta.setCantidad(pv.getCantidad())
                        detalle_venta.setDescripcion(pv.getDescripcion())
                        detalle_venta.setPrecioU(pv.getPrecioU())
                        detalle_venta.setImporte(pv.getImporte())
                        modelo_detalle_ventas.crear(detalle_venta)
                        prodDesc = modelo_productos.buscar(pv.getIdProducto())
                        prodDesc.setStock_Act(int(prodDesc.getStock_Act())-pv.getCantidad())
                        modelo_productos.actualizar(prodDesc)
            else:
                if modelo_ventas.actualizar(venta): mostrar = mensajes.aviso(self.winEdit, mensajes.OPER_OK)
                else: mensajes.error(self.winEdit, mensajes.OPER_NO)
            
                    
            self.winEdit.destroy()
            self.cargarVista(False) # Se llena la vista con los registros (False indica que no es la carga inicial)
            if(self.checkContado.get_active() == True):
                medio_pago.CargarMedioPagos(clienteID, self.labelFactura.get_text(), self.totalSinC)
            else:
                cuentas.CargarCuentas(clienteID,self.labelFactura.get_text(), self.totalSinC)
    
    def on_botonNewClientes_clicked(self, widget):
            clientes.CargarClientes()
            
            
            
    # -----------------------------------------------------------------------

# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    app = Ventas()
    gtk.main()
