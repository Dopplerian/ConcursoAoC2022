#!/usr/bin/python3
from typing import Callable
from dataclasses import dataclass

@dataclass
class Monkey:
	items: [int]
	operacion: Callable[int, int]
	divisor: int
	mono_true_indice: int
	mono_false_indice: int
	inspecciones: int

	def __init__(self, items, operacion, divisor, mono_true_indice, mono_false_indice):
		self.items = items
		self.operacion = operacion
		self.divisor = divisor
		self.mono_true_indice = mono_true_indice
		self.mono_false_indice = mono_false_indice
		self.inspecciones = 0

monos: [Monkey] = []

# Me da pereza hacer un intérprete del input ese la verdad
monos.append(Monkey([78, 53, 89, 51, 52, 59, 58, 85], lambda n: n * 3, 5, 2, 7))
monos.append(Monkey([64], lambda n: n + 7, 2, 3, 6))
monos.append(Monkey([71, 93, 65, 82], lambda n: n + 5, 13, 5, 4))
monos.append(Monkey([67, 73, 95, 75, 56, 74], lambda n: n + 8, 19, 6, 0))
monos.append(Monkey([85, 91, 90], lambda n: n + 4, 11, 3, 1))
monos.append(Monkey([67, 96, 69, 55, 70, 83, 62], lambda n: n * 2, 3, 4, 1))
monos.append(Monkey([53, 86, 98, 70, 64], lambda n: n + 6, 7, 7, 0))
monos.append(Monkey([88, 64], lambda n: n * n, 17, 2, 5))

from numpy import prod
ult_divisor = prod([m.divisor for m in monos])

for i in range(10_000):
	for monkey in monos:
		for item in monkey.items:
			item_nuevo = monkey.operacion(item) % ult_divisor
			if item_nuevo % monkey.divisor == 0:
				monos[monkey.mono_true_indice].items.append(item_nuevo)
			else:
				monos[monkey.mono_false_indice].items.append(item_nuevo)
		monkey.inspecciones += len(monkey.items)
		monkey.items = []

inspecciones = sorted([m.inspecciones for m in monos])

print(inspecciones[-1]*inspecciones[-2])