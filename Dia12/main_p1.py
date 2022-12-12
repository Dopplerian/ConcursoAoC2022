#!/usr/bin/python3

# Ésta no es una solución muy eficiente que digamos (de hecho en mi
# máquina tarda unos 2,5 segundos en dar una respuesta, mientras que
# las soluciones de los anteriores problemas era instantánea), pero
# tampoco me preocupa mucho. Si quisiese rapidez hubiera escogido C
# o Rust, no Python.

archivo = map(lambda x: x.rstrip('\n'), iter(open("input.txt","r").readlines()))

mapa = []
posicion_inicial = None
posicion_final = None
abiertos = []
distancias = {}

for j, linea in enumerate(archivo):
	fila = []
	for i, c in enumerate(linea):
		coords = (i, j)
		abiertos.append(coords)
		distancias[coords] = float('inf')
		if c == 'S':
			distancias[coords] = 0
			posicion_inicial = coords
			fila.append(0)
		elif c == 'E':
			posicion_final = coords
			fila.append(ord('z') - ord('a'))
		else:
			fila.append(ord(c) - ord('a'))
	mapa.append(fila)

def es_accesible(actual, vecino):
	global mapa
	valor_actual = mapa[actual[1]][actual[0]]
	valor_vecino = mapa[vecino[1]][vecino[0]]
	diferencia = valor_vecino - valor_actual
	return diferencia <= 1

def vecinos_abiertos(actual):
	global abiertos
	global mapa
	arriba = (actual[0], actual[1] + 1)
	abajo = (actual[0], actual[1] - 1)
	derecha = (actual[0] + 1, actual[1])
	izquierda = (actual[0] - 1, actual[1])
	posibles = [arriba, abajo, derecha, izquierda]
	posibles = filter(lambda x: x in abiertos, posibles)
	posibles = filter(lambda x: es_accesible(actual, x), posibles)
	return posibles

while len(abiertos) != 0:
	actual = sorted(abiertos, key = lambda x: distancias[x])[0]
	abiertos.remove(actual)

	for vecino in vecinos_abiertos(actual):
		nueva_distancia = distancias[actual] + 1
		if nueva_distancia < distancias[vecino]:
			distancias[vecino] = nueva_distancia

print(distancias[posicion_final])