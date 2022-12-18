#!/usr/bin/python3

# Este código es horriblemente difícil de explicar por comentarios,
# si alguien quiere saber qué es lo que hace, que me pregunte xd.

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
ciclos = 1_000_000_000_000
punto_mas_alto = 0
abiertos = set()
for i in range(anchura_camara):
	abiertos.add((i, 0))

def vecinos(punto):
	for vec in [(1,0),(-1,0),(0,-1),(0,1)]:
		nuevo_punto = (punto[0] + vec[0], punto[1] + vec[1])
		if not (0 <= nuevo_punto[0] < anchura_camara):
			continue
		if nuevo_punto[1] <= 0:
			continue
		if nuevo_punto in camara:
			continue
		yield nuevo_punto

def esta_abierto(punto: tuple[int, int]) -> bool:
	if punto[1] >= punto_mas_alto:
		return True
	visitados = set()
	pila = []
	pila.append(tuple(punto))
	while len(pila) != 0:
		vertice = pila.pop()
		if vertice in visitados:
			continue
		visitados.add(tuple(vertice))
		for vecino in vecinos(vertice):
			if vecino[1] >= punto_mas_alto:
				return True
			pila.append(tuple(vecino))
	return False

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
	global abiertos
	antiguo_punto_mas_alto = punto_mas_alto
	for punto in roca:
		punto_mas_alto = max(punto[1], punto_mas_alto)
		camara.add(tuple(punto))
	a_eliminar = []
	for x in abiertos:
		x_abs = (x[0], antiguo_punto_mas_alto + x[1])
		if not esta_abierto(x_abs):
			a_eliminar.append(x)
	for punto in a_eliminar:
		abiertos.remove(punto)
	if antiguo_punto_mas_alto != punto_mas_alto:
		diferencia = punto_mas_alto - antiguo_punto_mas_alto
		abiertos = set(map(lambda x: (x[0], x[1] - diferencia), abiertos))

	for punto in roca:
		if esta_abierto(punto):
			punto_rel = (punto[0], punto[1] - punto_mas_alto)
			abiertos.add(punto_rel)

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

def imprimir_camara():
	for j in reversed(range(1, punto_mas_alto + 5)):
		for i in range(anchura_camara):
			if (i,j) in camara:
				print('#', end = "")
			else:
				print('.', end = "")
		print("")
	print("-------\n")

estados = []
puntos_altos = []
for i in range(ciclos):
	punto_spawn = (desp_derecha, punto_mas_alto + desp_arriba)
	roca = [list(x) for x in rocas[i % len(rocas)]]
	roca = spawnear(roca, punto_spawn)
	mover_jet()
	while mover_gravedad():
		mover_jet()
	estado = (deepcopy(abiertos), i % len(rocas), contador_jet % len(movimientos))
	if estado in estados:
		ciclo_comienzo = estados.index(estado)
		punto_alto_antes = puntos_altos[ciclo_comienzo]
		punto_alto_despues = punto_mas_alto
		diferencia_altos = punto_alto_despues - punto_alto_antes
		diferencia_ciclos = i - ciclo_comienzo
		ciclos_resumibles = (ciclos - ciclo_comienzo - 1) # Mirar aquí
		repeticiones = ciclos_resumibles // diferencia_ciclos
		resumenes = repeticiones*diferencia_altos
		punto_mas_mas_alto = punto_alto_antes + resumenes
		ciclos_sin_tocar = ciclos - ciclo_comienzo - repeticiones*diferencia_ciclos - 1
		for j in range(ciclos_sin_tocar):
			normalizado = j + ciclo_comienzo + 1
			punto_mas_mas_alto += (puntos_altos[normalizado] - puntos_altos[normalizado - 1])
		print(punto_mas_mas_alto)
		exit()
	puntos_altos.append(punto_mas_alto)
	estados.append(estado)

# imprimir_camara()
# print(abiertos)
