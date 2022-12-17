// Esto es un intento de la parte 2 en Rust.
// Los COSTES y FLUJOS son extraídos de la
// primera parte de la versión de Python de
// este programa.
// Me da un error de stack y no tengo la
// suficiente paciencia para arreglarlo.

const NODOS: usize = 16;

const COSTES: [[usize; NODOS]; NODOS] = [[0, 3, 3, 7, 8, 11, 3, 3, 5, 10, 5, 2, 5, 5, 8, 12],
								[3, 0, 5, 7, 9, 12, 2, 2, 2, 11, 7, 3, 6, 5, 10, 13],
								[3, 5, 0, 4, 6, 9, 3, 6, 7, 8, 2, 3, 6, 2, 5, 10],
								[7, 7, 4, 0, 2, 5, 5, 9, 9, 4, 5, 7, 5, 2, 8, 6],
								[8, 9, 6, 2, 0, 3, 7, 11, 11, 2, 7, 6, 3, 4, 10, 4],
								[11, 12, 9, 5, 3, 0, 10, 14, 14, 3, 10, 9, 6, 7, 13, 2],
								[3, 2, 3, 5, 7, 10, 0, 4, 4, 9, 5, 2, 5, 3, 8, 11],
								[3, 2, 6, 9, 11, 14, 4, 0, 3, 13, 8, 5, 8, 7, 11, 15],
								[5, 2, 7, 9, 11, 14, 4, 3, 0, 13, 9, 5, 8, 7, 12, 15],
								[10, 11, 8, 4, 2, 3, 9, 13, 13, 0, 9, 8, 5, 6, 12, 2],
								[5, 7, 2, 5, 7, 10, 5, 8, 9, 9, 0, 5, 8, 3, 3, 11],
								[2, 3, 3, 7, 6, 9, 2, 5, 5, 8, 5, 0, 3, 5, 8, 10],
								[5, 6, 6, 5, 3, 6, 5, 8, 8, 5, 8, 3, 0, 7, 11, 7],
								[5, 5, 2, 2, 4, 7, 3, 7, 7, 6, 3, 5, 7, 0, 6, 8],
								[8, 10, 5, 8, 10, 13, 8, 11, 12, 12, 3, 8, 11, 6, 0, 14],
								[12, 13, 10, 6, 4, 2, 11, 15, 15, 2, 11, 10, 7, 8, 14, 0]];

const FLUJOS: [usize; NODOS] = [7, 14, 6, 12, 21, 23, 0, 20, 15, 22, 19, 3, 8, 13, 17, 24];

const MAX_TIEMPO: usize = 10;

#[derive(Clone, Copy)]
struct Posicion {
	vertice: usize,
	minuto: usize
}

#[derive(Clone, Copy)]
struct Nodo {
	entidades: [Posicion; 2],
	visitados: [Option<usize>; FLUJOS.len()]
}

fn presion_total(nodo: Nodo) -> isize {
	let mut sumador = 0;
	for i in 0..nodo.visitados.len() {
		if let Some(minuto) = nodo.visitados[i] {
			sumador += (MAX_TIEMPO as isize - minuto as isize)*(FLUJOS[i] as isize);
		}
	}
	return sumador;
}

fn vecinos(nodo: Nodo) -> Vec<Nodo> {
	if nodo.entidades[0].minuto < nodo.entidades[1].minuto {
		let res = vecinos_entidad(nodo, 0);
		if res.len() != 0 {
			return res;
		}
		return vecinos_entidad(nodo, 1);
	} else {
		let res = vecinos_entidad(nodo, 1);
		if res.len() != 0 {
			return res;
		}
		return vecinos_entidad(nodo, 0);
	}
}

fn vecinos_entidad(nodo: Nodo, entidad: usize) -> Vec<Nodo> {
	let mut res = vec![];
	for i in 0..NODOS {
		if i == entidad {
			continue;
		}
		if let Some(_) = nodo.visitados[i] {
			continue;
		}
		let vertice = nodo.entidades[entidad].vertice;
		let minuto_vecino = nodo.entidades[entidad].minuto + COSTES[vertice][i];
		if minuto_vecino > MAX_TIEMPO {
			continue;
		}
		let mut entidades_vecino = nodo.entidades;
		entidades_vecino[entidad].vertice = i;
		entidades_vecino[entidad].minuto = minuto_vecino;
		let nodo_vecino = Nodo {
			entidades: entidades_vecino,
			visitados: nodo.visitados,
		};
		res.push(nodo_vecino);
	}
	res
}

fn main() {
	let ini = 6;
	let inicial = Nodo {
		entidades: [Posicion {
			vertice: ini,
			minuto: 0
		}; 2],
		visitados: [None; NODOS],
	};
	let res = presion_total(explorar(inicial));
	println!("{res}");
}

fn explorar(nodo_i: Nodo) -> Nodo {
	let mut nodo = nodo_i;
	for i in 0..nodo.entidades.len() {
		let vertice = nodo.entidades[i].vertice;
		if let Some(_) = nodo.visitados[vertice] {
			continue;
		}
		if nodo.entidades[i].minuto >= MAX_TIEMPO {
			continue;
		}
		nodo.entidades[i].minuto += 1;
		nodo.visitados[vertice] = Some(nodo.entidades[i].minuto);
	}
	
	let vecinos = vecinos(nodo);
	if vecinos.len() == 0 {
		return nodo;
	}
	let mut max_nodo = None;
	let mut max_presion = 0;
	for vecino in vecinos {
		let res = explorar(vecino);
		let presion = presion_total(res);
		if presion > max_presion {
			max_presion = presion;
			max_nodo = Some(res);
		}
	}
	if let Some(resultado) = max_nodo {
		return resultado;
	}
	panic!();
}
