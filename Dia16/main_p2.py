#!/usr/bin/python3

# No me he sentido menos orgulloso de un programa en mi vida.
# En CPython, tarda 2 horas en ejecutarse en mi ordenador.
# Me encantaría testearlo en PyPy pero pgraph me da problemas
# y me da pereza portear este código para que use otra librería.

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

arr = []
for i in range(grafo.n):
	arr1 = []
	for j in range(grafo.n):
		if grafo[i] in grafo[j].neighbours():
			arr1.append(grafo[i].edgeto(grafo[j]).cost)
		else:
			arr1.append(0)
	arr.append(arr1)
print(arr)

for i in range(grafo.n):
	if grafo['AA'] is grafo[i]:
		print(i)

# exit()
max_tiempo = 26

@dataclass
class Nodo:
	vertices: list[UVertex]
	visitados: dict[UVertex, int]
	minutos: list[int]

	def __init__(self, vert, vis, min):
		self.vertices = vert
		self.visitados = vis
		self.minutos = min

def copia(nodo: Nodo) -> Nodo:
	vert = nodo.vertices.copy()
	visi = {}
	for key, val in nodo.visitados.items():
		visi[key] = val
	min = nodo.minutos.copy()
	return Nodo(vert, visi, min)

def presion_total(nodo: Nodo) -> int:
	abiertos = nodo.visitados
	sumador = 0
	for vertice, minuto in abiertos.items():
		cantidad_flujo = flujos[vertice]*(max_tiempo - minuto)
		sumador += cantidad_flujo
	return sumador

def vecinos(nodo: Nodo) -> list[Nodo]:
	minutos = enumerate(nodo.minutos)
	minutos = sorted(minutos, key = lambda x: x[1])

	for i, minuto in minutos:
		res = []
		vertice = nodo.vertices[i]
		for vecino in vertice.neighbours():
			if vecino in nodo.visitados.keys():
				continue
			minutos_vecino = minuto + vertice.edgeto(vecino).cost
			if minutos_vecino > max_tiempo:
				continue
			nuevos_vertices = nodo.vertices.copy()
			nuevos_vertices[i] = vecino
			nuevos_minutos = nodo.minutos.copy()
			nuevos_minutos[i] = minutos_vecino
			nodo_vecino = Nodo(nuevos_vertices, nodo.visitados, nuevos_minutos)
			res.append(nodo_vecino)
		if len(res) > 0:
			return res
	return []
	
def explorar(nodo: Nodo) -> Nodo:
	for i in range(len(nodo.vertices)):
		vertice = nodo.vertices[i]
		if vertice not in nodo.visitados.keys():
			nodo_copia = copia(nodo)
			nodo_copia.minutos[i] += 1
			nodo_copia.visitados[vertice] = nodo_copia.minutos[i]
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

inicial = Nodo([grafo['AA'], grafo['AA']], {grafo['AA']: 0}, [0, 0])
print(presion_total(explorar(inicial)))
