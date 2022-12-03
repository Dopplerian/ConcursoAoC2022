#!/usr/bin/python3
archivo = open("input.txt", 'r')

lineas = archivo.readlines()

elfos_max = [(-1,-1)] * 3

elfo_actual = 1
elfo_actual_cal = 0

for linea in lineas:
	if linea != "\n":
		elfo_actual_cal += int(linea[:-1])
		continue
	# Esto próximo es medio que horrible tbh
	elfos_max.append((elfo_actual, elfo_actual_cal))
	elfos_max.sort(key=lambda x: x[1], reverse=True)
	elfos_max.pop()

	elfo_actual += 1
	elfo_actual_cal = 0

print(f"Elfos max = {elfos_max}")
cal = 0
for elfo in elfos_max:
	cal += elfo[1]
print(f"Total cal = {cal}")