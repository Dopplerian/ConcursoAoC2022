#!/usr/bin/python3

import ast

archivo = map(lambda x: x.rstrip('\n').split('->'), iter(open("input.txt","r").readlines()))

contador = 0

mapa = [['.' for x in range(1000)] for x in range(1000)]

def signo(x):
	if x > 0:
		return 1
	if x == 0:
		return 0
	if x < 0:
		return -1

punto_mas_bajo = 0

def hacer_linea(a, b):
	global mapa
	global punto_mas_bajo
	vec = (signo(b[0] - a[0]), signo(b[1] - a[1]))
	mov = a
	punto_mas_bajo = max(b[1], a[1], punto_mas_bajo)
	while mov != b:
		mapa[mov[0]][mov[1]] = '#'
		mov[0] += vec[0]
		mov[1] += vec[1]
	mapa[mov[0]][mov[1]] = '#'

for linea in archivo:
	linea_sep = [[int(y) for y in x.strip(' ').split(',')] for x in linea]
	for i in range(len(linea_sep) - 1):
		hacer_linea(linea_sep[i], linea_sep[i + 1])

fuente = (500, 0)

grano_arena = [500,0]

while True:
	# Esto se debería poder hacer mejor pero ahora mismo no puedo xd
	if grano_arena[1] == punto_mas_bajo + 1:
		mapa[grano_arena[0]][grano_arena[1]] = 'o'
		contador += 1
		if grano_arena == [500, 0]:
			break
		grano_arena = [500, 0]
	elif mapa[grano_arena[0]][grano_arena[1] + 1] == '.':
		grano_arena[1] += 1
	elif mapa[grano_arena[0] - 1][grano_arena[1] + 1] == '.':
		grano_arena[1] += 1
		grano_arena[0] -= 1
	elif mapa[grano_arena[0] + 1][grano_arena[1] + 1] == '.':
		grano_arena[1] += 1
		grano_arena[0] += 1
	else:
		mapa[grano_arena[0]][grano_arena[1]] = 'o'
		contador += 1
		if grano_arena == [500, 0]:
			break
		grano_arena = [500, 0]

print(contador)