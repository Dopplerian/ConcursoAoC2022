#!/usr/bin/python3

archivo = map(lambda x: x.rstrip('\n').split(' '), iter(open("input.txt","r").readlines()))

y_objetivo = 2_000_000

def distancia(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

posiciones_descartadas = set()
faros = set()

for linea in archivo:
	x_sensor = int(linea[2][2:-1])
	y_sensor = int(linea[3][2:-1])
	x_faro = int(linea[8][2:-1])
	y_faro = int(linea[9][2:])
	sensor = (x_sensor, y_sensor)
	faro = (x_faro, y_faro)
	faros.add(faro)
	dist = distancia(sensor, faro)
	amplitud = 2*dist + 1
	dist_y = abs(y_sensor - y_objetivo)
	amplitud_y = max(0, amplitud - 2*dist_y)
	semi_amplitud_y = amplitud_y // 2
	for i in range(x_sensor - semi_amplitud_y, x_sensor + semi_amplitud_y + 1):
		posiciones_descartadas.add((i, y_objetivo))

for faro in faros:
	if faro in posiciones_descartadas:
		posiciones_descartadas.remove(faro)

print(len(posiciones_descartadas))
