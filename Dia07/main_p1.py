#!/usr/bin/python3

max_tamano = 100_000

archivo = map(lambda x: x.rstrip('\n').split(' '), iter(open("input.txt","r").readlines()))

dir_actual: [str] = [""]

tamanos = {"": 0}

def a_string(dir: [str]) -> str:
	return '/'.join(dir)

def comando(linea: str):
	global dir_actual # Esta línea es necesaria porque Python fue diseñado por simios
	if linea[1] != "cd":
		return

	if linea[2] == '/':
		dir_actual = [""]
	elif linea[2] == "..":
		dir_actual.pop()
	else:
		dir_actual.append(linea[2])

for linea in archivo:
	if linea[0] == '$':
		comando(linea)
	elif linea[0] == 'dir':
		dir = dir_actual + [linea[1]]
		tamanos[a_string(dir)] = 0
	else:
		tamano_fichero = int(linea[0])
		for i in range(len(dir_actual)):
			dir = a_string(dir_actual[:i + 1])
			tamanos[dir] += tamano_fichero

sumador = 0
for valor in tamanos.values():
	if valor <= max_tamano:
		sumador += valor
print(sumador)