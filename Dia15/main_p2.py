#!/usr/bin/python3

# Este no es el programa más eficiente del mundo la verdad
# En CPython en mi máquina tarda unos 100 segundos :(
# Por lo que recomiendo usar pypy aquí, que corre en unos 2 segundos

archivo = map(lambda x: x.rstrip('\n').split(' '), iter(open("input.txt","r").readlines()))

def distancia(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

sensores_y_distancias = set()

def esta_en_distancia(x, y):
	global sensores_y_distancias
	for sensor, dist in sensores_y_distancias:
		if distancia(sensor, (x, y)) <= dist:
			return True
	return False

for linea in archivo:
	x_sensor = int(linea[2][2:-1])
	y_sensor = int(linea[3][2:-1])
	x_faro = int(linea[8][2:-1])
	y_faro = int(linea[9][2:])
	faro = (x_faro, y_faro)
	sensor = (x_sensor, y_sensor)
	dist = distancia(sensor, faro)
	sensores_y_distancias.add((sensor, dist))

max_coord = 4000000
for sensor, dist in sensores_y_distancias:
	for vec in [(1,1), (1,-1), (-1,1), (-1,-1)]:
		for i in range(dist + 2):
			desp = dist + 1
			x = sensor[0] + vec[0]*(i - desp)
			y = sensor[1] + vec[1]*i
			if not (0 <= x <= max_coord) or not (0 <= y <= max_coord):
				continue
			if not esta_en_distancia(x, y):
				print(x*4000000 + y)
				exit()
