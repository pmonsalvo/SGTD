#!#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sistema import mensajes

# Esto solo se ejecuta cuando es llamado como programa principal
if __name__ == '__main__':
    mostrar = mensajes.error(None, mensajes.OPER_NO)
    print mostrar
    
    mostrar = mensajes.aviso(None, mensajes.OPER_OK)
    print mostrar

    mostrar = mensajes.pregunta(None, '¿Desea continuar?')
    print mostrar

    mostrar = mensajes.advert(None, 'Cuidado!!' + '\n' + '¿Desea continuar?')
    print mostrar
