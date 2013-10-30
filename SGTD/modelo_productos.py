#!#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modelo de la tabla productos con sus métodos de acceso a datos.
Esos métodos son los que deben usarse para acceder a la BD.
Forma parte del paquete modelos.
"""

from sistema import conectarBD

class Producto(object):
    """
    La clase que define el registro de la BD.
    """

    def __init__(self):

        # Atributos de la clase, son los campos de la tabla
        self.__id = 0
        self.__nombre = ''
        self.__descripcion = ''
        self.__precio = ''
        self.__costo = ''
        self.__iva = ''
        self.__comision = ''
        self.__stock_min = ''
        self.__descuento = ''
        self.__stoc_act = ''
        

    # Método que define str(clase) por defecto, para usar por ejemplo en print objeto
    def __str__(self):
        return self.getNombre()

    # ------------------------- Getters y Setters -------------------------
    
    def getId(self):
        return self.__id
    def setId(self, valor):
        self.__id = valor

    def getDescripcion(self):
        return self.__descripcion
    def setDescripcion(self, valor):
        self.__descripcion = valor

    def getNombre(self):
        return self.__nombre_razon
    def setNombre(self, valor):
        self.__nombre_razon = valor

    def getPrecio(self):
        return self.__precio
    def setPrecio(self, valor):
        self.__precio = valor

    def getCosto(self):
        return self.__costo
    def setCosto(self, valor):
        self.__costo = valor
    
    def getIVA(self):
        return self.__iva
    def setIVA(self, valor):
        self.__iva = valor

    def getComision(self):
        return self.__comision
    def setComision(self, valor):
        self.__comision = valor

    def getStock(self):
        return self.__stock_min
    def setStock(self, valor):
        self.__stock_min = valor
        
    def getDescuento(self):
        return self.__descuento
    def setDescuento(self, valor):
        self.__descuento = valor
        
    def getStock_Act(self):
        return self.__stock_act
    def setStock_Act(self, valor):
        self.__stock_act = valor
        
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
        cursor.execute('select * from Productos')       
        filas = cursor.fetchall()
        cursor.close()

    # Recorre las filas generadas y arma una tupla de objetos de la clase
    lista = None # Se arma todo en una lista, una tupla no se puede alterar
    for fila in filas:
        objeto = Producto()
        objeto.setId(fila[0])
        objeto.setNombre(fila[1].strip()) # strip() elimina caracteres no imprimibles
        objeto.setDescripcion(fila[2].strip())
        objeto.setPrecio(fila[3].strip())
        objeto.setCosto(fila[4].strip())
        objeto.setIVA(fila[5].strip())
        objeto.setComision(fila[6].strip())
        objeto.setStock(fila[7].strip())
        objeto.setStock_Act(fila[8].strip())
        objeto.setDescuento(fila[9].strip())
        

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
        cursor.execute('select * from Productos where idProductos = %s', (codigo,))
        fila = cursor.fetchone()
        cursor.close()

    if (fila != None):
        objeto = Producto()
        objeto.setId(fila[0])
        objeto.setNombre(fila[1].strip()) # strip() elimina caracteres no imprimibles
        objeto.setDescripcion(fila[2].strip())
        objeto.setPrecio(fila[3].strip())
        objeto.setCosto(fila[4].strip())
        objeto.setIVA(fila[5].strip())
        objeto.setComision(fila[6].strip())
        objeto.setStock(fila[7].strip())
        objeto.setStock_Act(fila[8].strip())
        objeto.setDescuento(fila[9].strip())
        

    return objeto
    

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
def crear(producto):
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
        cursor.execute('insert into Productos (nombre, descripcion, precio, costo, porc_iva, porc_comision, stock_minimo, stock_actual, porc_descuento) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (producto.getNombre(), producto.getDescripcion(), producto.getPrecio(), producto.getCosto(), producto.getIVA(), producto.getComision(), producto.getStock(), producto.getStock_Act(), producto.getDescuento()))
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
        cursor.execute('delete from Productos where idProductos = %s', (codigo,))
        bd.get_db().commit()
        cursor.close()
        salida = True

    return salida

# ---------------------------------------------------------------------------------------

def actualizar(producto):
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
        cursor.execute('update Productos set nombre = %s, descripcion = %s, precio = %s, costo = %s, porc_iva = %s, porc_comision = %s, stock_minimo = %s, stock_actual=%s, porc_descuento = %s where idProductos = %s',
                       (producto.getNombre(), producto.getDescripcion(), producto.getPrecio(), producto.getCosto(), producto.getIVA(), producto.getComision(), producto.getStock(), producto.getStock_Act(), producto.getDescuento(), producto.getId()))
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
