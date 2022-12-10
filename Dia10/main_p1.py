#!/usr/bin/python3

archivo = map(lambda x: x.rstrip('\n').split(' '), iter(open("input.txt","r").readlines()))

ciclo = 0
x = 1

sumador = 0

def comprobar_ciclo():
	global ciclo
	global x
	global sumador
	if (ciclo - 20) % 40 == 0:
		sumador += ciclo*x

for linea in archivo:
	ciclo += 1
	comprobar_ciclo()
	if linea[0] == "noop":
		pass
	elif linea[0] == "addx":
		ciclo += 1
		comprobar_ciclo()
		x += int(linea[1])
	else:
		print("Error de línea.")
		exit(1)

print(sumador)