#!/usr/bin/python3

archivo = map(lambda x: x.rstrip('\n').split(' '), iter(open("input.txt","r").readlines()))

fila = [[0, 0] for _ in range(10)]

posiciones_visitadas = set()
posiciones_visitadas.add((fila[-1][0], fila[-1][1]))

direcciones = {'R': (1, 0), 'L': (-1, 0), 'D': (0, -1), 'U': (0, 1)}

def signo(x: int) -> int:
	if x < 0:
		return -1
	if x > 0:
		return 1
	if x == 0:
		return 0

def actualizar_tail(head: [int], tail: [int]) -> [int]:
	nueva_tail = tail.copy()
	distancia_vert = abs(head[0] - tail[0])
	distancia_hori = abs(head[1] - tail[1])
	if max(distancia_vert, distancia_hori) > 1:
		mov = (signo(head[0] - tail[0]), signo(head[1] - tail[1]))
		nueva_tail[0] += mov[0]
		nueva_tail[1] += mov[1]
	return nueva_tail

for linea in archivo:
	direccion = direcciones[linea[0]]
	movimientos = int(linea[1])
	for _ in range(movimientos):
		fila[0][0] += direccion[0]
		fila[0][1] += direccion[1]
		for i in range(1, len(fila)):
			fila[i] = actualizar_tail(fila[i - 1], fila[i])
		posiciones_visitadas.add((fila[-1][0], fila[-1][1]))

print(len(posiciones_visitadas))