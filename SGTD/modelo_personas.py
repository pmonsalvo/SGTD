#!#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modelo de la tabla personas con sus métodos de acceso a datos.
Esos métodos son los que deben usarse para acceder a la BD.
Forma parte del paquete modelos.
"""

from sistema import conectarBD

class Persona(object):
    """
    La clase que define el registro de la BD.
    """

    def __init__(self):

        # Atributos de la clase, son los campos de la tabla
        self.__id = 0
        self.__tipo_persona = ''
        self.__nombre_razon_social = ''
        self.__direccion = ''
        self.__telefono = ''
        self.__ruc_cedula = ''
        self.__es_cliente = ''
        self.__es_proveedor = ''


    # Método que define str(clase) por defecto, para usar por ejemplo en print objeto
    def __str__(self):
        return self.getNombre()

    # ------------------------- Getters y Setters -------------------------
    
    def getId(self):
        return self.__id
    def setId(self, valor):
        self.__id = valor

    def getTipo(self):
        return self.__tipo_persona
    def setTipo(self, valor):
        self.__tipo_persona = valor

    def getNombre(self):
        return self.__nombre_razon_social
    def setNombre(self, valor):
        self.__nombre_razon_social = valor

    def getDireccion(self):
        return self.__direccion
    def setDireccion(self, valor):
        self.__direccion = valor

    def getTelefono(self):
        return self.__telefono
    def setTelefono(self, valor):
        self.__telefono = valor
    
    def getRuc_Cedula(self):
        return self.__ruc_cedula
    def setRuc_Cedula(self, valor):
        self.__ruc_cedula = valor

    def getCliente(self):
        return self.__es_cliente
    def setCliente(self, valor):
        self.__es_cliente = valor

    def getProveedor(self):
        return self.__es_proveedor
    def setProveedor(self, valor):
        self.__es_proveedor = valor

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
        cursor.execute('select * from Personas')        
        filas = cursor.fetchall()
        cursor.close()

    # Recorre las filas generadas y arma una tupla de objetos de la clase
    lista = None # Se arma todo en una lista, una tupla no se puede alterar
    for fila in filas:
        objeto = Persona()
        objeto.setId(fila[0])
        objeto.setTipo(fila[1]) # strip() elimina caracteres no imprimibles
        objeto.setNombre(fila[2].strip())
        objeto.setDireccion(fila[3].strip())
        objeto.setTelefono(fila[4].strip())
        objeto.setRuc_Cedula(fila[5].strip())
        objeto.setCliente(fila[6])
        objeto.setProveedor(fila[7])

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
        cursor.execute('select * from Personas where idClientes = %s', (codigo,))
        fila = cursor.fetchone()
        cursor.close()

    if (fila != None):
        objeto = User()
        objeto.setId(fila[0])
        objeto.setTipo(fila[1].strip()) # strip() elimina caracteres no imprimibles
        objeto.setNombre(fila[2].strip())
        objeto.setDireccion(fila[3].strip())
        objeto.setTelefono(fila[4].strip())
        objeto.setRuc_Cedula(fila[5].strip())
        objeto.setCliente(fila[6].strip())
        objeto.setProveedor(fila[7].strip())

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
def crear(persona):
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
        cursor.execute('insert into Personas (tipo_persona, nombre_razon_social, direccion, telefono, ruc_cedula, es_cliente, es_proveedor) values(%s, %s, %s, %s, %s, %s, %s)',
                       (persona.getTipo(), persona.getNombre(), persona.getDireccion(), persona.getTelefono(), persona.getRuc_Cedula(), persona.getCliente(), persona. getProveedor()))
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
        cursor.execute('delete from Personas where idClientes = %s', (codigo,))
        bd.get_db().commit()
        cursor.close()
        salida = True

    return salida

# ---------------------------------------------------------------------------------------

def actualizar(persona):
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
        cursor.execute('update Personas set tipo_persona = %s, nombre_razon_social = %s, direccion = %s, telefono = %s, ruc_cedula = %s, es_cliente = %s, es_proveedor = %s where id = %s',
                       (persona.getTipo(), persona.getNombre(), persona.getDireccion(), persona.getTelefono(), persona.getRuc_Cedula(), persona.getCliente(), persona.getProveedor(), persona.getId()))
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
