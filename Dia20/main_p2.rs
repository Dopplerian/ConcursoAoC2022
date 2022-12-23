use std::fs::File;
use std::str::FromStr;
use std::io::{self, BufReader, prelude::*};

#[derive(PartialEq, Eq, Hash, Clone, Copy)]
struct Numero {
	valor: isize,
	posicion_inicial: usize,
}

fn main() -> io::Result<()> {
	let args = std::env::args().collect::<Vec<String>>();
	let archivo = File::open(args[1].clone())?;
	let lector = BufReader::new(archivo);
	let clave_desencriptado = 811589153;

	let mut texto = vec![];
	let mut posiciones = vec![];
	let mut posicion_cero = None;
	for (i, linea) in lector.lines().enumerate() {
		let contenido = isize::from_str(&(linea?)).unwrap();
		let n = Numero {
			valor: contenido * clave_desencriptado,
			posicion_inicial: i
		};
		posiciones.push(i);
		texto.push(n);
		if contenido == 0 {
			posicion_cero = Some(i);
		}
	}

	for _j in 0..10 {
		for i in 0..texto.len() {
			mover(&mut texto, &mut posiciones, i);
		}
	}

	if let Some(pos0) = posicion_cero {
		let posicion_final_cero = posiciones[pos0];
		let pos1000 = (posicion_final_cero + 1000) % texto.len();
		let pos2000 = (posicion_final_cero + 2000) % texto.len();
		let pos3000 = (posicion_final_cero + 3000) % texto.len();
		let elem1000 = texto[pos1000].valor;
		let elem2000 = texto[pos2000].valor;
		let elem3000 = texto[pos3000].valor;
		let suma = elem1000 + elem2000 + elem3000;
		println!("{suma}");
	}
	Ok(())
}

fn mover(vec: &mut Vec<Numero>, pos: &mut Vec<usize>, indice: usize) {
	let posicion = pos[indice];
	let a_mover = vec[posicion];
	let movimiento = a_mover.valor;
	if movimiento == 0 {
		return;
	}
	let len = vec.len();
	let movimiento_canonizado = (movimiento).rem_euclid(len as isize - 1) as usize;
	if movimiento_canonizado == 0 {
		return;
	}
	for i in posicion..(posicion + movimiento_canonizado) {
		vec[i % len] = vec[(i + 1) % len];
		pos[vec[i % len].posicion_inicial] = i % len;
	}
	let pos_final = (posicion + movimiento_canonizado) % len;
	vec[pos_final] = a_mover;
	pos[indice] = pos_final;
}
