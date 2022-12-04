#!/usr/bin/python3

def prioridad(x: str) -> int:
	if not x.isalpha():
		raise ValueError("wtf")
	ascii = ord(x)
	if x.islower():
		ascii -= ord('z') - ord('A') + 1
	ascii -= ord('A') - (ord('z') - ord('a') + 2)
	return ascii

sumador = 0
alfabeto = [l for l in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"]
grupo_actual = alfabeto
elfo_actual = 1

for linea_sin_tratar in open("input.txt","r").readlines():
	linea = linea_sin_tratar.rstrip()
	grupo_actual = [l for l in linea if l in grupo_actual]
	elfo_actual += 1
	if elfo_actual > 3:
		elfo_actual = 1
		if len(grupo_actual) != 0:
			sumador += prioridad(grupo_actual[0])
		grupo_actual = alfabeto

print(sumador)