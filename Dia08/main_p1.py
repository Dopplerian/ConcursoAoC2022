#!/usr/bin/python3

archivo = map(lambda x: x.rstrip('\n'), iter(open("input.txt","r").readlines()))

mapa = []

for linea in archivo:
	linea_mapa = []
	for c in linea:
		linea_mapa.append(int(c))
	mapa.append(linea_mapa)

visibles = [[False] * len(mapa[0]) for x in range(len(mapa))]

for i in range(len(mapa[0])):
	max_hasta_ahora = -1
	for j in range(len(mapa)):
		if mapa[j][i] > max_hasta_ahora:
			max_hasta_ahora = mapa[j][i]
			visibles[j][i] = True

for j in range(len(mapa)):
	max_hasta_ahora = -1
	for i in range(len(mapa[0])):
		if mapa[j][i] > max_hasta_ahora:
			max_hasta_ahora = mapa[j][i]
			visibles[j][i] = True

for i in range(len(mapa[0])):
	max_hasta_ahora = -1
	for j in reversed(range(len(mapa))):
		if mapa[j][i] > max_hasta_ahora:
			max_hasta_ahora = mapa[j][i]
			visibles[j][i] = True

for j in range(len(mapa)):
	max_hasta_ahora = -1
	for i in reversed(range(len(mapa[0]))):
		if mapa[j][i] > max_hasta_ahora:
			max_hasta_ahora = mapa[j][i]
			visibles[j][i] = True

sumador = 0

for i in range(len(visibles)):
	for j in range(len(visibles[i])):
		if visibles[i][j]:
			sumador += 1
			
print(sumador)