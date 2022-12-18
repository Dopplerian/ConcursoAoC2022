#!/usr/bin/python3

nombre_archivo = "input.txt"
archivo = map(lambda x: x.rstrip('\n').split(','), iter(open(nombre_archivo,"r").readlines()))

cubos = set()

minimos = [float('inf'),float('inf'),float('inf')]
maximos = [-float('inf'),-float('inf'),-float('inf')]

for linea in archivo:
	linea_int = tuple(map(lambda x: int(x), linea))
	cubos.add(linea_int)
	for i in range(len(maximos)):
		maximos[i] = max(maximos[i], linea_int[i])
	for i in range(len(minimos)):
		minimos[i] = min(minimos[i], linea_int[i])

def en_limite(cubo):
	for i in range(len(maximos)):
		if cubo[i] >= maximos[i] + 2:
			return True
	for i in range(len(minimos)):
		if cubo[i] <= minimos[i] - 2:
			return True
	return False

def vecinos(cubo):
	vectores = [(0,0,-1),(0,-1,0),(-1,0,0),(0,0,1),(0,1,0),(1,0,0)]
	for vec in vectores:
		cubo_adyacente = (cubo[0] + vec[0], cubo[1] + vec[1], cubo[2] + vec[2])
		if not en_limite(cubo):
			yield cubo_adyacente

caras_tocadas = 0
inicial = (maximos[0] + 1, maximos[1] + 1, maximos[2] + 1)
visitados = set()
pila = [inicial]
while len(pila) != 0:
	cubo = pila.pop()
	if cubo in visitados:
		continue
	visitados.add(cubo)
	for vecino in vecinos(cubo):
		if vecino in cubos:
			caras_tocadas += 1
		else:
			pila.append(vecino)

print(caras_tocadas)
