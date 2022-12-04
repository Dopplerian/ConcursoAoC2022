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

for linea_sin_tratar in open("input.txt","r").readlines():
	linea = linea_sin_tratar.rstrip()
	longitud = len(linea) // 2
	mitad1 = linea[:longitud]
	mitad2 = linea[longitud:]
	prioridades = [prioridad(l) for l in mitad1 if l in mitad2]
	if len(prioridades) == 0:
		continue
	sumador += prioridades[0]

print(sumador)