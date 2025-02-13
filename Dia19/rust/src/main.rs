type INT = u8;

const CANTIDAD_RECURSOS: usize = 4;
const MAX_TIEMPO: INT = 32;

type Plano = [[INT; CANTIDAD_RECURSOS]; CANTIDAD_RECURSOS];

pub fn explorar(plano: Plano) -> INT {
	use std::collections::LinkedList;
	use std::collections::HashSet;
	use std::cmp::max;
	let inicio = Nodo::new(&plano);
	let mut max_actual: INT = 0;
	// let mut pila = vec![inicio];
	let mut pila = LinkedList::from([inicio]);
	let mut visitados = HashSet::<Nodo>::new();
	while pila.len() != 0 {
		let actual = pila.pop_front().unwrap();
		if visitados.contains(&actual) {
			continue;
		}
		visitados.insert(actual);
		max_actual = max(max_actual, actual.recursos[3]);
		for vecino in actual.vecinos() {
			pila.push_front(vecino);
		}
	}
	return max_actual;
}

#[derive(Copy, Clone, Hash, Eq, PartialEq)]
enum Fabrica {
	FABRICANDO(INT),
	RECUPERANDOSE,
	OCIOSA,
}

#[derive(Clone, Copy, Hash, Eq, PartialEq)]
struct Nodo<'a> {
	minuto: INT,
	plano: &'a Plano,
	recursos: [INT; CANTIDAD_RECURSOS],
	robots: [INT; CANTIDAD_RECURSOS],
	fabrica: Fabrica,
}

impl<'a> Nodo<'a> {
	pub fn new(plano: &'a Plano) -> Self {
		Nodo {
			minuto: 0,
			plano: plano,
			recursos: [0,0,0,0],
			robots: [1,0,0,0],
			fabrica: Fabrica::OCIOSA,
		}
	}

	fn anadir_recursos(&mut self) {
		for i in 0..CANTIDAD_RECURSOS {
			self.recursos[i] += self.robots[i];
		}
	}

	fn recoger_robot(&mut self) {
		if let Fabrica::FABRICANDO(robot) = self.fabrica {
			self.robots[robot as usize] += 1;
			self.fabrica = Fabrica::RECUPERANDOSE;
		} else if self.fabrica == Fabrica::RECUPERANDOSE {
			self.fabrica = Fabrica::OCIOSA;
		}
		self.minuto += 1;
	}

	fn crear_robot(&self, robot: INT) -> Option<Self> {
		let mut res = self.clone();
		let coste = self.plano[robot as usize];
		// Comprobar esta optimización
		let mut es_optimo = false;
		for i in 0..CANTIDAD_RECURSOS {
			if self.recursos[i] < coste[i] {
				return None;
			}
			let restante = self.recursos[i] - coste[i];
			if coste[i] > 0 && restante < self.robots[i] {
				es_optimo = true;
			}
			res.recursos[i] = restante;
		}
		if !es_optimo && self.fabrica == Fabrica::OCIOSA {
			return None;
		}
		res.fabrica = Fabrica::FABRICANDO(robot);
		return Some(res);
	}

	fn tiene_sentido_esperar(&self) -> bool {
		// return true;
		for robot in 0..CANTIDAD_RECURSOS {
			for necesario in 0..CANTIDAD_RECURSOS {
				let coste = self.plano[robot][necesario];
				if self.recursos[necesario] < coste {
					return true;
				}
			}
		}
		
		false
	}

	fn vecinos(&self) -> Vec<Self> {
		if self.minuto >= MAX_TIEMPO {
			return vec![];
		}
		let mut res = vec![];
		if self.tiene_sentido_esperar() {
			res.push(self.clone());
		}
		if let Some(creado) = self.crear_robot(3) {
			res.push(creado);
		}
		if let Some(creado) = self.crear_robot(2) {
			res.push(creado);
		} else { // Estos if's deberían estar fuera del else, ni puta idea de por qué esto funciona.
			if let Some(creado) = self.crear_robot(1) {
				res.push(creado);
			}
			if let Some(creado) = self.crear_robot(0) {
				res.push(creado);
			}
		}
		for i in 0..res.len() {
			res[i].anadir_recursos();
			res[i].recoger_robot();
		}
		return res;
	}
}

const PLANOS: [Plano; 3] = [
	[
		[4, 0, 0, 0],
		[4, 0, 0, 0],
		[4, 5, 0, 0],
		[3, 0, 7, 0],
	],
	[
		[3, 0, 0, 0],
		[3, 0, 0, 0],
		[2, 20, 0, 0],
		[2, 0, 20, 0],
	],
	[
		[4, 0, 0, 0],
		[3, 0, 0, 0],
		[2, 20, 0, 0],
		[2, 0, 9, 0],
	],
];

// const PLANOS_EJEMPLOS: [Plano; 2] = [
// 	[
// 		[4, 0, 0, 0],
// 		[2, 0, 0, 0],
// 		[3, 14, 0, 0],
// 		[2, 0, 7, 0],
// 	],
// 	[
// 		[2, 0, 0, 0],
// 		[3, 0, 0, 0],
// 		[3, 8, 0, 0],
// 		[3, 0, 12, 0],
// 	],
// ];

fn main() {
	// for i in 0..PLANOS_EJEMPLOS.len() {
	// 	let res = explorar(PLANOS_EJEMPLOS[i]);
	// 	println!("{i}: {res}");
	// }
	let mut acumulador: u16 = 1;
	for i in 0..3 {
		let res = explorar(PLANOS[i]);
		acumulador *= res as u16;
		println!("{res}");
	}
	println!("{acumulador}");
}
