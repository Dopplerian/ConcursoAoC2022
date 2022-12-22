use std::fs::File;
use std::str::FromStr;
use std::io::{self, BufReader, prelude::*};

fn main() -> io::Result<()>{
	let args = std::env::args().collect::<Vec<String>>();
	let archivo = File::open(args[1].clone())?;
	let lector = BufReader::new(archivo);

	let mut texto = vec![];
	for linea in lector.lines() {
		texto.push(isize::from_str(&(linea?)).unwrap());
	}

	let mut posiciones: Vec<usize> = (0..texto.len()).collect();
	
	println!("{texto:?}");
	mover(&mut texto, &mut posiciones, 0);
	println!("{texto:?}");

	Ok(())
}

fn mover(vec: &mut Vec<isize>, pos: &mut Vec<usize>, indice: usize) {
	let posicion = pos[indice];
	let movimiento = vec[posicion];
	if movimiento == 0 {
		return;
	}
	if movimiento > 0 {
		let nueva_posicion = (movimiento + (posicion as isize)) as usize % vec.len();
		dbg!(nueva_posicion);
		pos[indice] = nueva_posicion;
		dbg!(movimiento as usize + posicion);
		for i in (posicion + 1)..=(movimiento as usize + posicion) {
			dbg!(i);
			let p = i as usize % vec.len();
			dbg!(p);
			dbg!(pos[p]);
			pos[p] -= 1;
			dbg!(pos[p]);
			let p1 = if p != 0 {p - 1} else {vec.len() - 1};
			dbg!(vec[p1]);
			vec[p1] = vec[p];
		}
		vec[nueva_posicion] = movimiento;
	} else {
		let max = movimiento + (posicion as isize);
		let nueva_posicion = if max > 0 {max as usize} else {(max + vec.len() as isize) as usize};
		//
		dbg!(nueva_posicion);
		pos[indice] = nueva_posicion;
		for i in ((posicion + 1)..=(movimiento as usize + posicion)).rev() {
			dbg!(i);
			let p = i as usize % vec.len();
			dbg!(p);
			dbg!(pos[p]);
			pos[p] -= 1;
			dbg!(pos[p]);
			let p1 = if p != 0 {p - 1} else {vec.len() - 1};
			dbg!(vec[p1]);
			vec[p1] = vec[p];
		}
		vec[nueva_posicion] = movimiento;
	}
}

