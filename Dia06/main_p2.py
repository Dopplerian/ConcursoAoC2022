#!/usr/bin/python3

linea = next(iter(open("input.txt", 'r').readlines()))

a_comprobar = 14

for i in range(len(linea)):
	conjunto = set()
	for j in range(a_comprobar):
		conjunto.add(linea[i + j])
	if len(conjunto) == a_comprobar:
		print(i + a_comprobar)
		break