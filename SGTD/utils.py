#!/usr/bin/env python
# -*- coding: utf-8 -*-

import compras

def convertir_numero(numero):
    
        inicial_comas = "{:,}".format(numero)
        final_puntos = inicial_comas.replace(",", ".")
        return final_puntos

def recogerNro():
    nro = compras.DevolverNro()
    return nro
