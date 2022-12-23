use std::fs::File;
use std::io::{self, BufReader, prelude::*};
use std::collections::HashMap;
use std::str::FromStr;

type INT = i64;

#[derive(Clone)]
struct Mono {
	valor: Option<INT>,
	hijos: Option<([String; 2], Operacion)>
}

#[derive(Clone)]
enum Operacion {
	SUMA,
	RESTA,
	MULTIPLICACION,
	DIVISION,
}

impl Operacion {
	pub fn aplicar(&self, val1: INT, val2: INT) -> INT {
		match self {
			Self::SUMA => val1 + val2,
			Self::RESTA => val1 - val2,
			Self::MULTIPLICACION => val1 * val2,
			Self::DIVISION => val1 / val2,
		}
	}
	
	pub fn inversa(&self) -> Self {
		match self {
			Self::SUMA => Self::RESTA,
			Self::RESTA => Self::SUMA,
			Self::MULTIPLICACION => Self::DIVISION,
			Self::DIVISION => Self::MULTIPLICACION,
		}
	}
}

fn main() -> io::Result<()> {
	let args = std::env::args().collect::<Vec<String>>();
	let archivo = File::open(args[1].clone())?;
	let lector = BufReader::new(archivo);
	let mut mapa: HashMap<String, Mono> = HashMap::new();

	for linea_sin_tratar in lector.lines() {
		let res;
		let linea = linea_sin_tratar?;
		let nombre = String::from(&linea[0..4]);
		if (linea.as_bytes()[6] as char).is_numeric() {
			let valor = Some(INT::from_str(&linea[6..]).unwrap());
			res = Mono {
				valor,
				hijos: None
			};
		} else {
			let hijo_der = linea[6..10].to_string();
			let hijo_izq = linea[13..].to_string();
			let op = match &linea[11..12] {
				"+" => Operacion::SUMA,
				"-" => Operacion::RESTA,
				"*" => Operacion::MULTIPLICACION,
				"/" => Operacion::DIVISION,
				_ => panic!(),
			};
			res = Mono {
				valor: None,
				hijos: Some(([hijo_izq, hijo_der], op)),
			};
		}
		mapa.insert(nombre, res);
	}

	let resultado = computar("root".to_string(), &mapa);
	println!("{resultado}");
	
	Ok(())
}

fn computar(root: String, mapa: &HashMap<String, Mono>) -> INT {
	let mono_raiz = mapa.get(&root).unwrap();
	if let Some(val) = mono_raiz.valor {
		return val;
	}
	let hijos_y_op_wrap = mono_raiz.hijos.clone();
	let hijos_y_op = hijos_y_op_wrap.unwrap();
	let hijo_der = &hijos_y_op.0[0];
	let hijo_izq = &hijos_y_op.0[1];
	let op = &hijos_y_op.1;
	let val_der = computar(hijo_der.clone(), mapa);
	let val_izq = computar(hijo_izq.clone(), mapa);
	let val = op.aplicar(val_izq, val_der);
	val
}
