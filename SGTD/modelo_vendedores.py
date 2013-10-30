#!#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modelo de la tabla vendedores con sus métodos de acceso a datos.
Esos métodos son los que deben usarse para acceder a la BD.
Forma parte del paquete modelos.
"""

from sistema import conectarBD

class Vendedor(object):
    """
    La clase que define el registro de la BD.
    """

    def __init__(self):

        # Atributos de la clase, son los campos de la tabla
        self.__id = 0
        self.__cedula = 0
        self.__nombres = ''
        self.__apellidos = ''
        self.__telefono = ''
        self.__direccion = ''
        self.__barrio = ''
        self.__ciudad = ''
        

    # Método que define str(clase) por defecto, para usar por ejemplo en print objeto
    def __str__(self):
        return self.getNombre()

    # ------------------------- Getters y Setters -------------------------
    def getId(self):
        return self.__id
    def setId(self, valor):
        self.__id = valor
        
    def getCedula(self):
        return self.__cedula
    def setCedula(self, valor):
        self.__cedula = valor

    def getApellido(self):
        return self.__apellidos
    def setApellido(self, valor):
        self.__apellidos = valor

    def getNombre(self):
        return self.__nombres
    def setNombre(self, valor):
        self.__nombres = valor

    def getDireccion(self):
        return self.__direccion
    def setDireccion(self, valor):
        self.__direccion = valor

    def getTelefono(self):
        return self.__telefono
    def setTelefono(self, valor):
        self.__telefono = valor
    
    def getBarrio(self):
        return self.__barrio
    def setBarrio(self, valor):
        self.__barrio = valor

    def getCiudad(self):
        return self.__ciudad
    def setCiudad(self, valor):
        self.__ciudad = valor

    

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
        cursor.execute('select * from Vendedores')      
        filas = cursor.fetchall()
        cursor.close()

    # Recorre las filas generadas y arma una tupla de objetos de la clase
    lista = None # Se arma todo en una lista, una tupla no se puede alterar
    for fila in filas:
        objeto = Vendedor()
        objeto.setId(fila[0])
        objeto.setCedula(fila[1].strip()) # strip() elimina caracteres no imprimibles
        objeto.setNombre(fila[2].strip())
        objeto.setApellido(fila[3].strip())
        objeto.setTelefono(fila[4].strip())
        objeto.setDireccion(fila[5].strip())
        objeto.setBarrio(fila[6].strip())
        objeto.setCiudad(fila[7].strip())

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
        cursor.execute('select * from Vendedores where idVendedores = %s', (codigo,))
        fila = cursor.fetchone()
        cursor.close()

    if (fila != None):
        objeto = Vendedor()
        objeto.setId(fila[0])
        objeto.setCedula(fila[1].strip()) # strip() elimina caracteres no imprimibles
        objeto.setNombre(fila[2].strip())
        objeto.setApellido(fila[3].strip())
        objeto.setTelefono(fila[4].strip())
        objeto.setDireccion(fila[5].strip())
        objeto.setBarrio(fila[6].strip())
        objeto.setCiudad(fila[7].strip())

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
def crear(vendedor):
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
        cursor.execute('insert into Vendedores (cedula, nombres, apellidos, telefono, direccion, barrio, ciudad) values(%s, %s, %s, %s, %s, %s, %s)',
                       (vendedor.getCedula(), vendedor.getNombre(), vendedor.getApellido(), vendedor.getTelefono(), vendedor.getDireccion(), vendedor.getBarrio(), vendedor.getCiudad()))
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
        cursor.execute('delete from Vendedores where idVendedores = %s', (codigo,))
        bd.get_db().commit()
        cursor.close()
        salida = True

    return salida

# ---------------------------------------------------------------------------------------

def actualizar(vendedor):
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
        cursor.execute('update Vendedores set cedula = %s, nombres = %s, apellidos = %s, direccion = %s, telefono = %s, barrio = %s, ciudad = %s where idVendedores= %s',
                       (vendedor.getCedula(), vendedor.getNombre(), vendedor.getApellido(), vendedor.getDireccion(), vendedor.getTelefono(), vendedor.getBarrio(), vendedor.getCiudad(), vendedor.getId()))
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
