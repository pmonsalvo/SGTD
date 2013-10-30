#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modelo de la tabla clientes con sus métodos de acceso a datos.
Esos métodos son los que deben usarse para acceder a la BD.
Forma parte del paquete modelos.
"""

from sistema import conectarBD

class DetCompra(object):
    """
    La clase que define el registro de la BD.
    """

    def __init__(self):

        # Atributos de la clase, son los campos de la tabla
        self.__idDetalle_Factura_Compra = 0
        self.__idNroFactura = 0
        self.__idProducto = 0
        self.__cantidad = 0
        self.__descripcion = ''
        self.__precio_unitario = 0
        self.__importe = 0
        

    # Método que define str(clase) por defecto, para usar por ejemplo en print objeto
    def __str__(self):
        return self.getDescripcion()

    # ------------------------- Getters y Setters -------------------------
    
    def getIdDetalle(self):
        return self.__idDetalle_Factura_Compra
    def setIdDetalle(self, valor):
        self.__idDetalle_Factura_Compra = valor

    def getIdFactura(self):
        return self.__idNroFactura
    def setIdFactura(self, valor):
        self.__idNroFactura = valor

    def getIdProducto(self):
        return self.__idProducto
    def setIdProducto(self, valor):
        self.__idProducto = valor

    def getCantidad(self):
        return self.__cantidad
    def setCantidad(self, valor):
        self.__cantidad = valor

    def getDescripcion(self):
        return self.__descripcion
    def setDescripcion(self, valor):
        self.__descripcion = valor
    
    def getPrecioU(self):
        return self.__precio_unitario
    def setPrecioU(self, valor):
        self.__precio_unitario = valor

    def getImporte(self):
        return self.__importe
    def setImporte(self, valor):
        self.__importe = valor
    

# ----------------------- Métodos de Acceso a Datos para la clase -----------------------

def obtenerTodos():
    """
    Retorna una tupla con todos los registros de la BD.
    """

    tupla = None # La tupla se inicializa
    # Cuando no hay conexión a la BD, se retorna la tupla vacía
    bd = conectarBD.ConectarBD()
    if (bd.get_db() == None):
        return tupla
    else:
        cursor = bd.get_db().cursor()
        cursor.execute('select * from Detalle_Factura_Compra')     
        filas = cursor.fetchall()
        cursor.close()

    # Recorre las filas generadas y arma una tupla de objetos de la clase
    lista = None # Se arma todo en una lista, una tupla no se puede alterar
    for fila in filas:
        objeto = DetCompra()
        objeto.setIdDetalle(fila[0])
        objeto.setIdFactura(fila[1]) # strip() elimina caracteres no imprimibles
        objeto.setIdProducto(fila[2])
        objeto.setCantidad(fila[3])
        objeto.setDescripcion(fila[4].strip())
        objeto.setPrecioU(fila[5])
        objeto.setImporte(fila[6])
        

        if (lista == None): lista = [objeto]
        else: lista.append(objeto)
    tupla = tuple(lista)

    return tupla

# ---------------------------------------------------------------------------------------

def buscar(codigo):
    """
    Retorna un objeto con id = codigo, None si no existe registro.
    """

    objeto = None
    # Cuando no hay conexión a la BD o el registro no existe, se retorna None
    bd = conectarBD.ConectarBD()
    if (bd.get_db() == None):
        return objeto
    else:
        cursor = bd.get_db().cursor()
        cursor.execute('select * from Detalle_Factura_Compra where idNroFactura = %s', (codigo,))
        filas = cursor.fetchall()
        cursor.close()
        
    lista = None
    for fila in filas:    
        objeto = DetCompra()
        objeto.setIdDetalle(fila[0])
        objeto.setIdFactura(fila[1]) # strip() elimina caracteres no imprimibles
        objeto.setIdProducto(fila[2])
        objeto.setCantidad(fila[3])
        objeto.setDescripcion(fila[4].strip())
        objeto.setPrecioU(fila[5])
        objeto.setImporte(fila[6])
        
        if (lista == None): lista = [objeto]
        else: lista.append(objeto)
    tupla = tuple(lista)

    return tupla

# ---------------------------------------------------------------------------------------
"""
def buscarLogin(nombre, clave):
    
    Retorna un objeto con un Login válido (usuario y claves ok).
    None si no existe registro.
    

    objeto = None
    # Cuando no hay conexión a la BD o el registro no existe, se retorna None
    bd = conectarBD.ConectarBD()
    if (bd.get_db() == None):
        return objeto
    else:
        cursor = bd.get_db().cursor()
        cursor.execute('select * from Usuarios where (username = %s) and (password = %s)', (nombre, clave,))
        fila = cursor.fetchone()
        cursor.close()

    if (fila != None):
        objeto = User()
        objeto.setId(fila[0])
        objeto.setUsername(fila[1].strip()) # strip() elimina caracteres no imprimibles
        objeto.setPassword(fila[2].strip())
        objeto.setEmail(fila[3].strip())
        objeto.setName(fila[4].strip())

    return objeto

# ---------------------------------------------------------------------------------------
"""
def crear(detCompra):
    """
    Dado un objeto de la clase, crea un registro nuevo para la BD.
    """

    salida = False
    # Cuando no hay conexión a la BD o el registro no existe, se retorna False
    bd = conectarBD.ConectarBD()
    if (bd.get_db() == None):
        return salida
    else:
        cursor = bd.get_db().cursor()
        cursor.execute('insert into Detalle_Factura_Compra (idNroFactura, idProducto, cantidad, descripcion, precio_unitario, importe) values(%s, %s, %s, %s, %s, %s)',
                       (detCompra.getIdFactura(), detCompra.getIdProducto(), detCompra.getCantidad(), detCompra.getDescripcion(), detCompra.getPrecioU(), detCompra.getImporte()))
        bd.get_db().commit()
        cursor.close()
        salida = True

    return salida

# ---------------------------------------------------------------------------------------

def eliminar(codigo):
    """
    Busca un objeto con ID = codigo y lo elimina de la BD.
    """

    salida = False
    # Cuando no hay conexión a la BD o el registro no existe, se retorna False
    bd = conectarBD.ConectarBD()
    if (bd.get_db() == None):
        return salida
    else:
        cursor = bd.get_db().cursor()
        cursor.execute('delete from Detalle_Factura_Compra where idNroFactura = %s', (codigo,))
        bd.get_db().commit()
        cursor.close()
        salida = True

    return salida

# ---------------------------------------------------------------------------------------

def actualizar(detCompra):
    """
    Dado un objeto de la clase, modifica sus atributos en la BD.
    El ID del mismo objeto se utiliza para localizarlo en la BD.
    """

    salida = False
    # Cuando no hay conexión a la BD o el registro no existe, se retorna None
    bd = conectarBD.ConectarBD()
    if (bd.get_db() == None):
        return salida
    else:
        cursor = bd.get_db().cursor()
        cursor.execute('update Detalle_Factura_Compra set idProducto = %s, cantidad = %s, descripcion = %s, precio_unitario = %s, importe = %s where idNroFactura = %s',
                       (detCompra.getIdProducto(), detCompra.getCantidad(), detCompra.getDescripcion(), detCompra.getPrecioU(), detCompra.getImporte(), detCompra.getIdFactura()))
        bd.get_db().commit()
        cursor.close()
        salida = True

    return salida

# ---------------------------------------------------------------------------------------

# Esto solamente se usa para probar el modulo
if __name__ == '__main__':
    a = User()
    b = User()
    a.setName('Usuario a')
    print str(a.getName()) + ' - ' + str(b.getName())
    print a
