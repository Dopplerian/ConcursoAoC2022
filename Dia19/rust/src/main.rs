const CANTIDAD_RECURSOS: usize = 4;
const MAX_TIEMPO: i64 = 28;

type Plano = [[i64; CANTIDAD_RECURSOS]; CANTIDAD_RECURSOS];

pub fn explorar(plano: Plano) -> i64 {
	use std::collections::LinkedList;
	use std::collections::HashSet;
	let inicio = Nodo::new(&plano);
	let mut max_actual: i64 = -1;
	let mut pila = LinkedList::from([inicio]);
	let mut visitados = HashSet::<Nodo>::new();
	while pila.len() != 0 {
		let actual = pila.pop_front().unwrap();
		if visitados.contains(&actual) {
			continue;
		}
		visitados.insert(actual);
		max_actual = std::cmp::max(max_actual, actual.recursos[3]);
		for vecino in actual.vecinos() {
			pila.push_front(vecino);
		}
	}
	return max_actual;
}

#[derive(Clone, Copy, Hash, Eq, PartialEq)]
struct Nodo<'a> {
	minuto: i64,
	plano: &'a Plano,
	recursos: [i64; CANTIDAD_RECURSOS],
	robots: [i64; CANTIDAD_RECURSOS],
	fabricando: Option<i64>,
}

impl<'a> Nodo<'a> {
	pub fn new(plano: &'a Plano) -> Self {
		Nodo {
			minuto: 0,
			plano: plano,
			recursos: [0,0,0,0],
			robots: [1,0,0,0],
			fabricando: None,
		}
	}

	fn anadir_recursos(&mut self) {
		for i in 0..CANTIDAD_RECURSOS {
			self.recursos[i] += self.robots[i];
		}
	}

	fn recoger_robot(&mut self) {
		if let Some(robot) = self.fabricando {
			self.robots[robot as usize] += 1;
			self.fabricando = None;
		}
		self.minuto += 1;
	}

	fn crear_robot(&self, robot: i64) -> Option<Self> {
		let mut res = self.clone();
		let coste = self.plano[robot as usize];
		let mut es_optimo = false;
		for i in 0..CANTIDAD_RECURSOS {
			let restante = self.recursos[i] - coste[i];
			if restante < 0 {
				return None;
			}
			if coste[i] > 0 && restante < self.robots[i] {
				es_optimo = true;
			}
			res.recursos[i] = restante;
		}
		if !es_optimo {
			return None;
		}
		res.fabricando = Some(robot);
		return Some(res);
	}

	fn vecinos(&self) -> Vec<Self> {
		if self.minuto >= MAX_TIEMPO {
			return vec![];
		}
		let mut res = vec![self.clone()];
		for i in 0..CANTIDAD_RECURSOS {
			if let Some(creado) = self.crear_robot(i as i64) {
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

fn main() {
	let mut acumulador: i64 = 1;
	for i in 0..3 {
		acumulador *= explorar(PLANOS[i]);
		println!("{i}");
	}
	println!("{acumulador}");
}
