#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modelo de la tabla clientes con sus métodos de acceso a datos.
Esos métodos son los que deben usarse para acceder a la BD.
Forma parte del paquete modelos.
"""

from sistema import conectarBD

class Compra(object):
    """
    La clase que define el registro de la BD.
    """

    def __init__(self):

        # Atributos de la clase, son los campos de la tabla
        self.__idNroComp = 0
        self.__fecha = ''
        self.__tipo = ''
        self.__idProveedor = 0
        self.__total = 0
        

    # Método que define str(clase) por defecto, para usar por ejemplo en print objeto
    def __str__(self):
        return self.getNombre()

    # ------------------------- Getters y Setters -------------------------
    
    def getId(self):
        return self.__idNroComp
    def setId(self, valor):
        self.__idNroComp = valor

    def getTipo(self):
        return self.__tipo
    def setTipo(self, valor):
        self.__tipo = valor

    def getFecha(self):
        return self.__fecha
    def setFecha(self, valor):
        self.__fecha = valor

    def getProveedor(self):
        return self.__idProveedor
    def setProveedor(self, valor):
        self.__idProveedor = valor
    
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
        cursor.execute('select * from Factura_Compra')     
        filas = cursor.fetchall()
        cursor.close()

    # Recorre las filas generadas y arma una tupla de objetos de la clase
    lista = None # Se arma todo en una lista, una tupla no se puede alterar
    for fila in filas:
        objeto = Compra()
        objeto.setId(fila[0])
        objeto.setFecha(fila[1].strip()) # strip() elimina caracteres no imprimibles
        objeto.setTipo(fila[2].strip())
        objeto.setProveedor(fila[3])
        objeto.setTotal(fila[4])
        

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
        cursor.execute('select * from Factura_Compra where idNroComp = %s', (codigo,))
        fila = cursor.fetchone()
        cursor.close()

    if (fila != None):
        objeto = Venta()
        objeto.setId(fila[0])
        objeto.setFecha(fila[1].strip()) # strip() elimina caracteres no imprimibles
        objeto.setTipo(fila[2].strip())
        objeto.setProveedor(fila[3])
        objeto.setTotal(fila[4])
        

    return objeto


def ultimo():
        
    objeto = None
    bd = conectarBD.ConectarBD()
    if (bd.get_db() == None):
        return objeto
    else:
        cursor = bd.get_db().cursor()
        cursor.execute('select max(IdFactura) from Factura')
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
def crear(compra):
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
        cursor.execute('insert into Factura_Compra (idNroComp, fecha, tipo, idproveedor, total) values(%s, %s, %s, %s, %s)',
                       (compra.getId(),compra.getFecha(), compra.getTipo(), compra.getProveedor(), compra.getTotal()))
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
        cursor.execute('delete from Factura_Compra where idNroComp = %s', (codigo,))
        bd.get_db().commit()
        cursor.close()
        salida = True

    return salida

# ---------------------------------------------------------------------------------------

def actualizar(compra):
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
        cursor.execute('update Factura_Compra set fecha = %s, tipo = %s, idproveedor = %s, total = %s where idNroComp= %s',
                       (compra.getFecha(), compra.getTipo(), compra.getProveedor(), compra.getTotal(), compra.getId()))
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
