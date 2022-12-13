#!/usr/bin/python3

import ast

archivo = map(lambda x: x.rstrip('\n'), iter(open("input.txt","r").readlines()))

estado = "IZQ"
izq = []
sumador = 0

def comparacion(izq, der) -> int:
	if type(izq) == int and type(der) == int:
		return der - izq
	if type(izq) != list:
		izq = [izq]
	if type(der) != list:
		der = [der]
	return en_orden(izq, der)

def en_orden(izq: [], der: []) -> int:
	for i in range(len(izq)):
		if i >= len(der):
			return len(der) - len(izq)
		item_der = der[i]
		item_izq = izq[i]
		comp = comparacion(izq[i], der[i])
		if comp != 0:
			return comp
	return len(der) - len(izq)

i = 1
for linea in archivo:
	if linea == "":
		i += 1
		estado = "IZQ"
		continue
	arr = ast.literal_eval(linea) # Python appreciation comment
	if estado == "IZQ":
		izq = arr
	elif en_orden(izq, arr) > 0:
		print(f"{i}: {izq}, {arr}")
		sumador += i
	if estado == "IZQ":
		estado = "DER"
	elif estado == "DER":
		estado = "NEO"

print(sumador)