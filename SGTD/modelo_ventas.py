#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modelo de la tabla clientes con sus métodos de acceso a datos.
Esos métodos son los que deben usarse para acceder a la BD.
Forma parte del paquete modelos.
"""

from sistema import conectarBD

class Venta(object):
    """
    La clase que define el registro de la BD.
    """

    def __init__(self):

        # Atributos de la clase, son los campos de la tabla
        self.__idFactura = 0
        self.__fecha = ''
        self.__tipo = ''
        self.__idCliente = 0
        self.__idVendedor = 0
        self.__total = 0
        

    # Método que define str(clase) por defecto, para usar por ejemplo en print objeto
    def __str__(self):
        return self.getNombre()

    # ------------------------- Getters y Setters -------------------------
    
    def getId(self):
        return self.__idFactura
    def setId(self, valor):
        self.__idFactura = valor

    def getTipo(self):
        return self.__tipo
    def setTipo(self, valor):
        self.__tipo = valor

    def getFecha(self):
        return self.__fecha
    def setFecha(self, valor):
        self.__fecha = valor

    def getDireccion(self):
        return self.__direccion
    def setDireccion(self, valor):
        self.__direccion = valor

    def getCliente(self):
        return self.__idCliente
    def setCliente(self, valor):
        self.__idCliente = valor
    
    def getVendedor(self):
        return self.__idVendedor
    def setVendedor(self, valor):
        self.__idVendedor = valor
        
    def getTotal(self):
        return self.__total
    def setTotal(self, valor):
        self.__total = valor

    
    

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
        cursor.execute('select * from Factura_Venta')     
        filas = cursor.fetchall()
        cursor.close()

    # Recorre las filas generadas y arma una tupla de objetos de la clase
    lista = None # Se arma todo en una lista, una tupla no se puede alterar
    for fila in filas:
        objeto = Venta()
        objeto.setId(fila[0])
        objeto.setFecha(fila[1].strip()) # strip() elimina caracteres no imprimibles
        objeto.setTipo(fila[2].strip())
        objeto.setCliente(fila[3])
        objeto.setVendedor(fila[4])
        objeto.setTotal(fila[5])
        

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
        cursor.execute('select * from Factura_Venta where idFactura = %s', (codigo,))
        fila = cursor.fetchone()
        cursor.close()

    if (fila != None):
        objeto = Venta()
        objeto.setId(fila[0])
        objeto.setFecha(fila[1].strip()) # strip() elimina caracteres no imprimibles
        objeto.setTipo(fila[2].strip())
        objeto.setCliente(fila[3])
        objeto.setVendedor(fila[4])
        objeto.setTotal(fila[5])
        

    return objeto


def ultimo():
        
    objeto = None
    bd = conectarBD.ConectarBD()
    if (bd.get_db() == None):
        return objeto
    else:
        cursor = bd.get_db().cursor()
        cursor.execute('select max(IdFactura) from Factura_Venta')
        fila = cursor.fetchone()
        cursor.close()
        
    if (fila!=None):
        return fila[0]
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
def crear(venta):
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
        cursor.execute('insert into Factura_Venta (fecha, tipo, idcliente, idvendedor, total) values(%s, %s, %s, %s, %s)',
                       (venta.getFecha(), venta.getTipo(), venta.getCliente(), venta.getVendedor(), venta.getTotal()))
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
        cursor.execute('delete from Factura_Venta where idFactura = %s', (codigo,))
        bd.get_db().commit()
        cursor.close()
        salida = True

    return salida

# ---------------------------------------------------------------------------------------

def actualizar(venta):
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
        cursor.execute('update Factura_Venta set fecha = %s, tipo = %s, idcliente = %s, idvendedor = %s, total = %s where idFactura = %s',
                       (venta.getFecha(), venta.getTipo(), venta.getCliente(), venta.getVendedor(), venta.getTotal(), venta.getId()))
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
