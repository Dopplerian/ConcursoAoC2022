#!/usr/bin/python3

archivo = map(lambda x: x.rstrip('\n').split(' '), iter(open("input.txt","r").readlines()))

ciclo = 0
x = 1

def dibujar_crt():
	global ciclo
	global x
	pos_crt_actual = (ciclo - 1) % 40 + 1
	if abs(pos_crt_actual - x) <= 1:
		caracter = '#'
	else:
		caracter = '.'
	print(caracter, end="")
	if pos_crt_actual == 40:
		print("")
	
for linea in archivo:
	ciclo += 1
	dibujar_crt()
	if linea[0] == "noop":
		pass
	elif linea[0] == "addx":
		ciclo += 1
		x += int(linea[1])
		dibujar_crt()
	else:
		print("Error de línea.")
		exit(1)
