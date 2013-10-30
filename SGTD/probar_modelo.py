#!#!/usr/bin/env python
# -*- coding: utf-8 -*-

import users
from sistema import mensajes

"""
# Ejemplo de buscar un usuario por código
usuario = users.buscar(1)
print usuario
"""

"""
# Ejemplo de traer todos los usuarios y recorrer la lista (tupla en realidad)
lista = users.obtenerTodos()
usuario = lista[0]
print usuario
for usuario in lista:
    print str(usuario.getId()) + ' - ' + str(usuario.getName())
"""

"""
# Ejemplo de modificar un usuario
usuario = users.buscar(1)
usuario.setName('Juan Manuel Marchese')
print users.actualizar(usuario)
"""

"""
# Ejemplo de crear un usuario
usuario = users.User()
usuario.setName('Nombre Prueba')
usuario.setUsername('prueba')
usuario.setEmail('mail@mail.com')
print users.crear(usuario)
"""

"""
# Ejemplo de eliminar usuario
print users.eliminar(2)
"""
