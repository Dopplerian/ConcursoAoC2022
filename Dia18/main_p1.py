#!/usr/bin/python3

nombre_archivo = "input.txt"
archivo = map(lambda x: x.rstrip('\n').split(','), iter(open(nombre_archivo,"r").readlines()))

cubos = set()

for linea in archivo:
	linea_int = tuple(map(lambda x: int(x), linea))
	cubos.add(linea_int)

def caras_descubiertas(cubo):
	contador = 0
	vectores = [(0,0,-1),(0,-1,0),(-1,0,0),(0,0,1),(0,1,0),(1,0,0)]
	for vec in vectores:
		cubo_adyacente = (cubo[0] + vec[0], cubo[1] + vec[1], cubo[2] + vec[2])
		if cubo_adyacente not in cubos:
			contador += 1
	return contador

total = 0
for cubo in cubos:
	total += caras_descubiertas(cubo)

print(total)
