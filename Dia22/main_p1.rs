use std::fs::File;
use std::io::{self, BufReader, prelude::*};

type INT = isize;

#[derive(PartialEq, Eq, Copy, Clone, Debug)]
enum Loseta {
	VACIO,
	PARED,
	NADA,
}

impl Loseta {
	pub fn from_caracter(c: char) -> Self {
		match c {
			'.' => Loseta::VACIO,
			'#' => Loseta::PARED,
			' ' => Loseta::NADA,
			_ => panic!()
		}
	}
}

#[derive(Clone, Copy, Debug)]
enum Direccion {
	ARRIBA,
	IZQUIERDA,
	ABAJO,
	DERECHA,
}
use Direccion::*;

impl Direccion {
	pub fn vector(&self) -> (INT, INT) {
		match self {
			ARRIBA => (0, -1),
			IZQUIERDA => (-1, 0),
			ABAJO => (0, 1),
			DERECHA => (1, 0),
		}
	}
	
	pub fn numero(&self) -> INT {
		match self {
			ARRIBA => 3,
			IZQUIERDA => 2,
			ABAJO => 1,
			DERECHA => 0,
		}
	}

	pub fn girar_derecha(&self) -> Self {
		match self {
			ARRIBA => DERECHA,
			IZQUIERDA => ARRIBA,
			ABAJO => IZQUIERDA,
			DERECHA => ABAJO,
		}
	}

	pub fn girar_izquierda(&self) -> Self {
		match self {
			ARRIBA => IZQUIERDA,
			IZQUIERDA => ABAJO,
			ABAJO => DERECHA,
			DERECHA => ARRIBA,
		}
	}
}

fn main() -> io::Result<()> {
	let args = std::env::args().collect::<Vec<String>>();
	let archivo = File::open(args[1].clone())?;
	let lector = BufReader::new(archivo);
	let mut mapa: Vec<Vec<Loseta>> = vec![];
	let lineas = lector.lines().map(|l| l.as_ref().unwrap().clone()).collect::<Vec<_>>();
	let mut max_x = 0;
	let max_y = lineas.len() - 2;

	for j in 0..lineas.len() - 1 {
		let linea = &lineas[j];
		let linea = linea.chars().map(|c| Loseta::from_caracter(c)).collect::<Vec<_>>();
		max_x = std::cmp::max(max_x, linea.len());
		mapa.push(linea);
	}
	mapa = mapa.iter().map(|v| {
		let mut x = v.clone();
		while x.len() != max_x {
			x.push(Loseta::NADA);
		}
		x
	}).collect();
	let ultima_linea = lineas.last().unwrap().clone().chars().collect::<Vec<_>>();

	let l = alex(ultima_linea);
	let mut pos_actual = {
		let mut res = None;
		for i in 0..lineas[0].len() {
			if mapa[0][i] == Loseta::VACIO {
				res = Some(i);
				break;
			}
		}
		if let Some(r) = res {
			(r as INT, 0)
		} else {
			panic!()
		}
	};
	let mut dir_actual = Direccion::DERECHA;

	for acc in &l {
		match *acc {
			Token::GiroDer => dir_actual = dir_actual.girar_derecha(),
			Token::GiroIzq => dir_actual = dir_actual.girar_izquierda(),
			Token::Mov(m) => {
				for _ in 0..m {
					pos_actual = proximo(pos_actual, dir_actual, &mapa, (max_x as isize, max_y as isize));
				}
			}
		}
	}

	let pos_real = (pos_actual.0 + 1, pos_actual.1 + 1);
	println!("{}", 1000*pos_real.1 + 4*pos_real.0 + dir_actual.numero());
	Ok(())
}

fn alex(linea: Vec<char>) -> Vec<Token> {
	let mut res = vec![];
	let mut co = 0;

	for i in 0..linea.len() {
		match linea[i] {
			'R' => {
				if co != i {
					let str = linea[co..i].iter().collect::<String>();
					let num = INT::from_str_radix(&str, 10).unwrap();
					res.push(Token::Mov(num));
				}
				co = i + 1;
				res.push(Token::GiroDer);
			},
			'L' => {
				if co != i {
					let str = linea[co..i].iter().collect::<String>();
					let num = INT::from_str_radix(&str, 10).unwrap();
					res.push(Token::Mov(num));
				}
				co = i + 1;
				res.push(Token::GiroIzq);
				
			}, 
			_ => {}
		}
	}
	if co != linea.len() {
		let str = linea[co..].iter().collect::<String>();
		let num = INT::from_str_radix(&str, 10).unwrap();
		res.push(Token::Mov(num));
	}
	
	res
}

#[derive(Debug)]
enum Token {
	GiroDer,
	GiroIzq,
	Mov(INT)
}

fn proximo(pos: (INT, INT), dir: Direccion, mapa: &Vec<Vec<Loseta>>, limites: (INT, INT)) -> (INT, INT) {
	let (vec_x, vec_y) = dir.vector();
	let (prev_x, prev_y) = pos;
	let (mut x, mut y) = pos;
	let (limite_x, limite_y) = limites;
	let res = loop {
		x = x + vec_x;
		if x < 0 {x = limite_x - 1}
		if x >= limite_x {x = 0}
		y = y + vec_y;
		if y < 0 {y = limite_y - 1}
		if y >= limite_y {y = 0}
		let l = mapa[y as usize][x as usize];
		match l {
			Loseta::VACIO => break (x, y),
			Loseta::PARED => break (prev_x, prev_y),
			_ => {}
		}
	};
	res
}
