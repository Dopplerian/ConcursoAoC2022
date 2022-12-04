#!/usr/bin/python3

contador = 0

for linea in [l.rstrip().split(',') for l in open("input.txt","r").readlines()]:
	elfo1 = [int(n) for n in linea[0].split('-')]
	elfo2 = [int(n) for n in linea[1].split('-')]
	uno_contiene_dos = elfo1[0] <= elfo2[0] and elfo1[1] >= elfo2[1]
	dos_contiene_uno = elfo2[0] <= elfo1[0] and elfo2[1] >= elfo1[1]
	if uno_contiene_dos or dos_contiene_uno:
		contador += 1

print(contador)