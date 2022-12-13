#!/usr/bin/python3

import ast

archivo = map(lambda x: x.rstrip('\n'), iter(open("input.txt","r").readlines()))

lista = [[[2]], [[6]]]

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

for linea in archivo:
	if linea == "":
		continue
	arr = ast.literal_eval(linea) # Python appreciation comment
	lista.append(arr)

from functools import cmp_to_key
lista = sorted(lista, key = cmp_to_key(en_orden), reverse = True)
index1 = lista.index([[2]]) + 1
index2 = lista.index([[6]]) + 1
for i in lista:
	print(i)
print(index1*index2)