#!/usr/bin/python3

from copy import deepcopy

archivo = map(lambda x: x.rstrip('\n'), iter(open("input.txt","r").readlines()))

desp_arriba = 4
desp_derecha = 2

camara = set()
anchura_camara = 7

rocas = [
	[(0,0),(1,0),(2,0),(3,0)],
	[(0,1),(1,0),(1,1),(1,2),(2,1)],
	[(0,0),(1,0),(2,0),(2,1),(2,2)],
	[(0,0),(0,1),(0,2),(0,3)],
	[(0,0),(0,1),(1,0),(1,1)]
]

def traducir(char):
	if char == '<':
		return -1
	if char == '>':
		return 1
	print("wtf")
	exit()
movimientos = [traducir(x) for x in next(archivo)]
ciclos = 20220
punto_mas_alto = 0

def spawnear(roca_c, punto_spawn):
	roca = roca_c
	for item in roca:
		item[0] += punto_spawn[0]
		item[1] += punto_spawn[1]
	return roca

contador_jet = 0
def mover_jet():
	global roca
	global contador_jet
	movimiento = movimientos[contador_jet % len(movimientos)]
	contador_jet += 1
	nueva_roca = deepcopy(roca)
	nueva_roca = spawnear(nueva_roca, (movimiento, 0))
	for punto in nueva_roca:
		if anchura_camara <= punto[0] or punto[0] < 0:
			return
		if tuple(punto) in camara:
			return
	roca = nueva_roca

def cristalizar():
	global camara
	global punto_mas_alto
	for punto in roca:
		punto_mas_alto = max(punto[1], punto_mas_alto)
		camara.add(tuple(punto))

def mover_gravedad():
	global roca
	nueva_roca = deepcopy(roca)
	nueva_roca = spawnear(nueva_roca, (0, -1))
	for punto in nueva_roca:
		if punto[1] <= 0 or tuple(punto) in camara:
			cristalizar()
			return False
	roca = nueva_roca
	return True

for i in range(ciclos):
	punto_spawn = (desp_derecha, punto_mas_alto + desp_arriba)
	roca = [list(x) for x in rocas[i % len(rocas)]]
	roca = spawnear(roca, punto_spawn)
	mover_jet()
	while mover_gravedad():
		mover_jet()

print(punto_mas_alto)
