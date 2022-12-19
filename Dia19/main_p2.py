#!/usr/bin/python3

from copy import copy
from copy import deepcopy

nombre_archivo = "input.txt"
archivo = map(lambda x: x.rstrip('\n').split(' '), iter(open(nombre_archivo,"r").readlines()))

max_tiempo = 24

planos = []

class Plano:
	def __init__(self, _id, _costes):
		self.id = _id
		self.costes = costes

class Nodo:
	def anadir_recursos(self):
		res = deepcopy(self)
		res_recursos = list(res.recursos)
		for i in range(len(res_recursos)):
			res_recursos[i] += res.robots[i]
		res.recursos = tuple(res_recursos)
		return res

	def recoger_robot(self):
		res = deepcopy(self)
		if res.fabrica_robot != None:
			lista = list(res.robots)
			lista[res.fabrica_robot] += 1
			res.robots = tuple(lista)
			res.fabrica_robot = None
		res.minuto += 1
		return res
	
	def crear_robot(self, robot):
		lista_recursos = []
		coste = planos[self.plano_id].costes[robot]
		tiene_sentido = False
		for i in range(len(self.recursos)):
			restante = self.recursos[i] - coste[i]
			if coste[i] > 0 and restante < self.robots[i]:
				tiene_sentido = True
			if restante < 0:
				return None
			lista_recursos.append(self.recursos[i] - coste[i])
		if not tiene_sentido:
			return None
		res = deepcopy(self)
		res.fabrica_robot = robot
		res.recursos = tuple(lista_recursos)
		return res
	
	def vecinos(self):
		if self.minuto >= max_tiempo:
			return []
		res = [self]
		for i in range(len(self.robots)):
			creado = self.crear_robot(i)
			if creado == None:
				continue
			res.append(creado)
		for i in range(len(res)):
			res[i] = res[i].anadir_recursos()
		for i in range(len(res)):
			res[i] = res[i].recoger_robot()
		return res

for linea in archivo:
	id = int(linea[1][:-1])
	costes_ore = (int(linea[6]), 0, 0, 0)
	costes_arcilla = (int(linea[12]), 0, 0, 0)
	costes_obsidiana = (int(linea[18]), int(linea[21]), 0, 0)
	costes_geoda = (int(linea[27]), 0, int(linea[30]), 0)
	costes = (costes_ore, costes_arcilla, costes_obsidiana, costes_geoda)
	plano = Plano(id, costes)
	planos.append(plano)

def nuevo(id):
	res = Nodo()
	res.minuto = 0
	res.plano_id = id
	res.recursos = (0,0,0,0)
	res.robots = (1,0,0,0)
	res.fabrica_robot = None
	return res

def explorar_plano(id):
	inicial = nuevo(id)
	max_actual = -1
	pila = [inicial]
	visitados = set()
	while len(pila) != 0:
		actual = pila.pop()
		if actual in visitados:
			continue
		visitados.add(actual)
		max_actual = max(max_actual, actual.recursos[3])
		for vecino in actual.vecinos():
			pila.append(vecino)
	return max_actual

acumulador = 1
for i in range(3):
	acumulador *= explorar_plano(i)
	print(i)

print(acumulador)