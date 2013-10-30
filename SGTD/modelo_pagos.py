#!#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modelo de la tabla cuentas métodos de acceso a datos.
Esos métodos son los que deben usarse para acceder a la BD.
Forma parte del paquete modelos.
"""

from sistema import conectarBD

class Pago(object):
    """
    La clase que define el registro de la BD.
    """

    def __init__(self):

        # Atributos de la clase, son los campos de la tabla
        self.__idPagos = 0
        self.__id_Factura = 0
        self.__id_Cliente = 0
        self.__monto_cuota = 0
        self.__vencimiento = ''
        self.__fecha_pago = ''
        
        

    # Método que define str(clase) por defecto, para usar por ejemplo en print objeto
    def __str__(self):
        return self.getNombre()

    # ------------------------- Getters y Setters -------------------------
    
    def getIdPagos(self):
        return self.__idPagos
    def setIdPagos(self, valor):
        self.__idPagos = valor

    def getIdFactura(self):
        return self.__id_Factura
    def setIdFactura(self, valor):
        self.__id_Factura = valor

    def getIdCliente(self):
        return self.__id_Cliente
    def setIdCliente(self, valor):
        self.__id_Cliente = valor

    def getCuotas(self):
        return self.__cuotas
    def setCuotas(self, valor):
        self.__cuotas = valor

    def getMonto(self):
        return self.__monto
    def setMonto(self, valor):
        self.__monto = valor
    
    def getFecha_Venc(self):
        return self.__fecha_vencimiento
    def setFecha_Venc(self, valor):
        self.__fecha_vencimiento = valor

    def getEntrega(self):
        return self.__entrega
    def setEntrega(self, valor):
        self.__entrega = valor

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
        cursor.execute('select * from Cuentas')        
        filas = cursor.fetchall()
        cursor.close()

    # Recorre las filas generadas y arma una tupla de objetos de la clase
    lista = None # Se arma todo en una lista, una tupla no se puede alterar
    for fila in filas:
        objeto = Pago()
        objeto.setIdPagos(fila[0])
        objeto.setIdFactura(fila[1]) # strip() elimina caracteres no imprimibles
        objeto.setIdCliente(fila[2])
        objeto.setCuotas(fila[3])
        objeto.setMonto(fila[4])
        objeto.setFecha_Venc(fila[5].strip())
        objeto.setEntrega(fila[6])
        objeot.setTotal(fila[7])

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
        cursor.execute('select * from Pagos where idPagos = %s', (codigo,))
        fila = cursor.fetchall()
        cursor.close()

    lista = None # Se arma todo en una lista, una tupla no se puede alterar
    for fila in filas:
        objeto = Cuenta()
        objeto.setIdPagos(fila[0])
        objeto.setIdFactura(fila[1]) # strip() elimina caracteres no imprimibles
        objeto.setIdCliente(fila[2])
        objeto.setCuotas(fila[3])
        objeto.setMonto(fila[4])
        objeto.setFecha_Venc(fila[5].strip())
        objeto.setEntrega(fila[6])
        objeot.setTotal(fila[7])

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
def crear(cuenta):
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
        cursor.execute('insert into Cuentas (idfactura, idcliente, cuotas, monto, fecha_vencimiento, total, entrega) values(%s, %s, %s, %s, %s, %s, %s)',
                       (cuenta.getIdFactura(), cuenta.getIdCliente(), cuenta.getCuotas(), cuenta.getMonto(), cuenta.getFecha_Venc(), cuenta.getTotal(), cuenta.getEntrega()))
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
        cursor.execute('delete from Cuentas where idCuentas = %s', (codigo,))
        bd.get_db().commit()
        cursor.close()
        salida = True

    return salida

# ---------------------------------------------------------------------------------------

def actualizar(cuenta):
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
        cursor.execute('update Cuentas set idfactura = %s, idcliente = %s, cuotas = %s, monto = %s, fecha_vencimiento = %s, total = %s, entrega = %s where idCuentas = %s',
                       (cuenta.getIdFactura(), cuenta.getIdCliente(), cuenta.getCuotas(), cuenta.getMonto(), cuenta.getFecha_Venc(), cuenta.getTotal(), cuenta.getEntrega(), cuenta.getIdCuentas()))
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
