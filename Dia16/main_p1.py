#!/usr/bin/python3

from pgraph import *
from collections import defaultdict
from dataclasses import dataclass

grafo = UGraph()

archivo = map(lambda x: x.rstrip('\n').split(' '), iter(open("input.txt","r").readlines()))

flujos = {}
adyacencias = {}

for linea in archivo:
	valvula = linea[1]
	flujo = int(linea[4][5:-1])
	v = grafo.add_vertex(name=valvula)
	flujos[v] = flujo
	adyacentes = [x.rstrip(',') for x in linea[9:]]
	adyacencias[v] = adyacentes

for vertex, adyacentes in adyacencias.items():
	for adyacente in adyacentes:
		v_adyacente = grafo[adyacente]
		if vertex not in v_adyacente.neighbours():
			vertex.connect(v_adyacente, cost = 1)

vertices_importantes = [v for v in grafo if flujos[v] > 0]
vertices_importantes.append(grafo['AA'])

def dijkstra(inicio: UVertex) -> dict[UVertex, int]:
	dist = defaultdict(lambda: float('inf'))
	dist[inicio] = 0
	abiertos = [x for x in grafo]
	while len(abiertos) != 0:
		u = min(abiertos, key = lambda x: dist[x])
		abiertos.remove(u)
		for v in u.neighbours():
			alt = dist[u] + 1
			if alt < dist[v]:
				dist[v] = alt
	dist = dict([(key, val) for key, val in dist.items() if key in vertices_importantes])
	return dist

distancias: dict[tuple[UVertex, UVertex], int] = defaultdict(lambda: None)

for i in range(len(vertices_importantes)):
	vertice1 = vertices_importantes[i]
	dist = dijkstra(vertice1)
	for vertice2, distancia in dist.items():
		distancias[(vertice1, vertice2)] = distancia

eliminados = set()
for v in grafo:
	if v not in vertices_importantes:
		eliminados.add(v)

if grafo['AA'] in eliminados:
	eliminados.remove(grafo['AA'])

for v in eliminados:
	grafo.remove(v)

for (v1, v2), dist in distancias.items():
	if v1 is v2:
		continue
	if v1 in v2.neighbours():
		v1.edgeto(v2).cost = dist
	else:
		v1.connect(v2, cost = dist)

max_tiempo = 30

@dataclass
class Nodo:
	vertice: UVertex
	visitados: dict[UVertex, int]
	minuto: int

	def __init__(self, vert, vis, min):
		self.vertice = vert
		self.visitados = vis
		self.minuto = min

def copia(nodo: Nodo) -> Nodo:
	vert = nodo.vertice
	visi = {}
	for key, val in nodo.visitados.items():
		visi[key] = val
	minu = nodo.minuto
	return Nodo(vert, visi, minu)

def presion_total(nodo: Nodo) -> int:
	abiertos = nodo.visitados
	sumador = 0
	for vertice, minuto in abiertos.items():
		cantidad_flujo = flujos[vertice]*(max_tiempo - minuto)
		sumador += cantidad_flujo
	return sumador

def vecinos(nodo: Nodo) -> list[Nodo]:
	res = []
	for vecino in nodo.vertice.neighbours():
		if vecino in nodo.visitados.keys():
			continue
		minuto = nodo.minuto + nodo.vertice.edgeto(vecino).cost
		if minuto > max_tiempo:
			continue
		nodo_vecino = Nodo(vecino, nodo.visitados, minuto)
		res.append(nodo_vecino)
	return res

def explorar(nodo: Nodo) -> Nodo:
	if nodo.vertice not in nodo.visitados.keys():
		nodo_copia = copia(nodo)
		nodo_copia.minuto += 1
		nodo_copia.visitados[nodo_copia.vertice] = nodo_copia.minuto
		nodo = nodo_copia
	
	vec = vecinos(nodo)
	if len(vec) == 0:
		return nodo
	max_act = (None, -1)
	for vecino in vec:
		res = explorar(vecino)
		presion = presion_total(res)
		if max_act[1] <= presion:
			max_act = (res, presion)
	return max_act[0]

inicial = Nodo(grafo['AA'], {grafo['AA']: 0}, 0)
print(presion_total(explorar(inicial)))
