#!/usr/bin/python3

dic = {'A': 0, 'B': 1, 'C': 2, 'X': 0, 'Y': 1, 'Z': 2}

sumador = 0

for linea in open("input.txt","r").readlines():
	linea_tratada = linea.rstrip().split(' ')
	ganancia_por_figura_elegida = (dic[linea_tratada[0]] + dic[linea_tratada[1]] - 1) % 3 + 1
	ganancia_por_resultado = dic[linea_tratada[1]] * 3
	sumador += ganancia_por_figura_elegida + ganancia_por_resultado

print(sumador)