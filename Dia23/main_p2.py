#!/usr/bin/python3

from copy import copy

archivo = map(lambda x: x.rstrip('\n'), iter(open("input.txt","r").readlines()))

mapa = set()

for j, linea in enumerate(archivo):
	for i, c in enumerate(linea):
		if c == '#':
			tupla = (i, j)
			mapa.add(tupla)

def esta_solo(x, y, mapa):
	for vec in [(1, 0),(-1, 0),(0, 1),(0, -1),(1, 1),(-1, 1),(-1, -1),(1, -1)]:
		if (vec[0] + x, vec[1] + y) in mapa:
			return False
	return True

def meter(tx, ty, fx, fy, deseado):
	if (tx, ty) not in deseado:
		deseado[(tx, ty)] = [(fx, fy)]
	else:
		deseado[(tx, ty)].append((fx, fy))

def comprobacion(x, y, i, deseado, mapa):
	if i == 0:
		if (x, y - 1) not in mapa and (x + 1, y - 1) not in mapa and (x - 1, y - 1) not in mapa:
			meter(x, y - 1, x, y, deseado)
			return True
	elif i == 1:
		if (x, y + 1) not in mapa and (x + 1, y + 1) not in mapa and (x - 1, y + 1) not in mapa:
			meter(x, y + 1, x, y, deseado)
			return True
	elif i == 2:
		if (x - 1, y) not in mapa and (x - 1, y + 1) not in mapa and (x - 1, y - 1) not in mapa:
			meter(x - 1, y, x, y, deseado)
			return True
	elif i == 3:
		if (x + 1, y) not in mapa and (x + 1, y + 1) not in mapa and (x + 1, y - 1) not in mapa:
			meter(x + 1, y, x, y, deseado)
			return True
	return False

def ronda(mapa, i):
	deseado = {}

	for elfo in mapa:
		x = elfo[0]
		y = elfo[1]
		if esta_solo(x, y, mapa):
			meter(x, y, x, y, deseado)
			continue
		for j in range(4):
			if comprobacion(x, y, (i + j) % 4, deseado, mapa):
				break
		else: # Dios mio acabo de encontrar un caso de uso real para el else de un bucle
			meter(x, y, x, y, deseado)

	for key, val in deseado.items():
		if len(val) == 1:
			mapa.remove(val[0])
			mapa.add(key)

i = 1
while True:
	mapa_previo = copy(mapa)
	ronda(mapa, i - 1)
	if mapa_previo == mapa:
		print(i)
		break
	i += 1
