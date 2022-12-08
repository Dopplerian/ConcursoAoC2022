#!/usr/bin/python3

archivo = map(lambda x: x.rstrip('\n'), iter(open("input.txt","r").readlines()))

mapa = []

for linea in archivo:
	linea_mapa = []
	for c in linea:
		linea_mapa.append(int(c))
	mapa.append(linea_mapa)

def puntuacion_en_direccion(i: int, j: int, k: tuple[int, int]) -> int:
	global mapa
	contador = 0
	paso = list(k)
	paso[0] += i
	paso[1] += j
	while 0 <= paso[0] < len(mapa) and 0 <= paso[1] < len(mapa[paso[0]]):
		contador += 1
		if mapa[i][j] <= mapa[paso[0]][paso[1]]:
			break
		paso[0] += k[0]
		paso[1] += k[1]
	return contador

def puntuacion_escenica(i: int, j: int) -> int:
	global mapa
	resultado = 1
	resultado *= puntuacion_en_direccion(i, j, (1, 0))
	resultado *= puntuacion_en_direccion(i, j, (0, 1))
	resultado *= puntuacion_en_direccion(i, j, (-1, 0))
	resultado *= puntuacion_en_direccion(i, j, (0, -1))
	return resultado

max_puntuacion_escenica = 0

for i in range(len(mapa)):
	for j in range(len(mapa[i])):
		max_puntuacion_escenica = max(max_puntuacion_escenica, puntuacion_escenica(i,j))

print(max_puntuacion_escenica)