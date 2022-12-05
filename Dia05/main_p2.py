#!/usr/bin/python3

num_pilas = 9

# pilas = [[]] * num_pilas

pilas = []
for i in range(num_pilas):
	pilas.append([])

archivo = iter(open("input.txt","r").readlines())

for linea in archivo:
	if linea[1] == '1':
		next(archivo)
		break
	for i in range(0, num_pilas):
		caracter = linea[1 + i * 4]
		if caracter == ' ':
			continue
		pilas[i].insert(0, caracter)

for linea in archivo:
	linea_sep = linea.split(' ')
	cantidad = int(linea_sep[1])
	origen = int(linea_sep[3]) - 1
	destino = int(linea_sep[5]) - 1
	ultimos_contenedores = pilas[origen][-cantidad:]
	pilas[origen] = pilas[origen][:len(pilas[origen]) - cantidad]
	pilas[destino].extend(ultimos_contenedores)

for pila in pilas:
	print(pila[-1], end = "")
print("")