#!#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modelo de la tabla users con sus métodos de acceso a datos.
Esos métodos son los que deben usarse para acceder a la BD.
Forma parte del paquete modelos.
"""

from sistema import conectarBD

class User(object):
    """
    La clase que define el registro de la BD.
    """

    def __init__(self):

        # Atributos de la clase, son los campos de la tabla
        self.__id = 0
        self.__username = ''
        self.__password = ''
        self.__email = ''
        self.__name = ''

    # Método que define str(clase) por defecto, para usar por ejemplo en print objeto
    def __str__(self):
        return self.getName()

    # ------------------------- Getters y Setters -------------------------
    
    def getId(self):
        return self.__id
    def setId(self, valor):
        self.__id = valor

    def getUsername(self):
        return self.__username
    def setUsername(self, valor):
        self.__username = valor

    def getPassword(self):
        return self.__password
    def setPassword(self, valor):
        self.__password = valor

    def getEmail(self):
        return self.__email
    def setEmail(self, valor):
        self.__email = valor

    def getName(self):
        return self.__name
    def setName(self, valor):
        self.__name = valor

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
        cursor.execute('select * from Usuarios')        
        filas = cursor.fetchall()
        cursor.close()

    # Recorre las filas generadas y arma una tupla de objetos de la clase
    lista = None # Se arma todo en una lista, una tupla no se puede alterar
    for fila in filas:
        objeto = User()
        objeto.setId(fila[0])
        objeto.setUsername(fila[1].strip()) # strip() elimina caracteres no imprimibles
        objeto.setPassword(fila[2].strip())
        objeto.setEmail(fila[3].strip())
        objeto.setName(fila[4].strip())
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
        cursor.execute('select * from Usuarios where id = %s', (codigo,))
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

def buscarLogin(nombre, clave):
    """
    Retorna un objeto con un Login válido (usuario y claves ok).
    None si no existe registro.
    """

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

def crear(usuario):
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
        cursor.execute('insert into Usuarios (username, name, email, password) values(%s, %s, %s, %s)',
                       (usuario.getUsername(), usuario.getName(), usuario.getEmail(), usuario.getPassword()))
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
        cursor.execute('delete from Usuarios where id = %s', (codigo,))
        bd.get_db().commit()
        cursor.close()
        salida = True

    return salida

# ---------------------------------------------------------------------------------------

def actualizar(usuario):
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
        cursor.execute('update Usuarios set username = %s, password = %s, email = %s, name = %s where id = %s',
                       (usuario.getUsername(), usuario.getPassword(), usuario.getEmail(), usuario.getName(), usuario.getId()))
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
