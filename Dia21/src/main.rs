use std::fs::File;
use std::io::{self, BufReader, prelude::*};
use std::collections::HashMap;
use std::collections::HashSet;
use std::str::FromStr;
use std::fmt::{Debug, Formatter};

type INT = i64;

#[derive(Clone, Eq, PartialEq, Hash)]
struct Mono {
	nombre: String,
	valor: Option<INT>,
	hijos: Option<([String; 2], Operacion)>
}

impl Debug for Mono {
	fn fmt(&self, fmt: &mut Formatter<'_>) -> Result<(), std::fmt::Error>{
		write!(fmt, "{}", self.nombre)
	}
}

#[derive(Clone, Copy, Eq, PartialEq, Debug, Hash)]
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

	pub fn inversa(&self, primer: bool) -> Self {
		match (self, primer) {
			(Self::SUMA, _) => Self::RESTA,
			(Self::RESTA, _) => Self::SUMA,
			(Self::MULTIPLICACION, _) => Self::DIVISION,
			(Self::DIVISION, false) => Self::DIVISION,
			(Self::DIVISION, true) => Self::MULTIPLICACION,
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
				nombre: nombre.clone(),
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
				nombre: nombre.clone(),
				valor: None,
				hijos: Some(([hijo_izq, hijo_der], op)),
			};
		}
		mapa.insert(nombre, res);
	}
	let camino = camino("root", "humn", &mapa);
	// println!("{camino:?}");
	let root = mapa.get("root").unwrap();
	let hijo1 = mapa.get(&root.hijos.clone().unwrap().0[0]).unwrap();
	let hijo2 = mapa.get(&root.hijos.clone().unwrap().0[1]).unwrap();
	let (mono1, mono2) = if camino.contains(hijo1) {
		(hijo1, hijo2)
	} else {
		(hijo2, hijo1)
	};
	let res2 = computar(mono2.nombre.clone(), &mapa);
	let res = resolver(&mono1.nombre, &mapa, res2, &camino);
	println!("{res}");
	Ok(())
}

fn resolver(mono: &str, mapa: &HashMap<String, Mono>, valor_esperado: INT, no_resueltos: &HashSet<Mono>) -> INT {
	if mono == "humn" {
		return valor_esperado;
	}
	let mono_actual = mapa.get(mono).unwrap();
	if !no_resueltos.contains(mono_actual) {
		panic!();
	}
	if let Some(h) = &mono_actual.hijos {
		let hijo_izq = &h.0[0];
		let hijo_der = &h.0[1];
		let mono_izq = mapa.get(hijo_izq).unwrap();
		let orden = no_resueltos.contains(mono_izq);
		let (hijo_resuelto, hijo_sin_resolver) = if orden {
			(hijo_der, hijo_izq)
		} else {
			(hijo_izq, hijo_der)
		};

		// valor_esperado = valor_resuelto op valor_sin_resolver =>
		// valor_esperado iop valor_resuelto = valor_sin_resolver
		let valor_resuelto = computar(hijo_resuelto.clone(), mapa);
		let operacion = h.1;
		let operacion_inversa = operacion.inversa(!orden);
		let valor_necesario = if operacion_inversa == Operacion::DIVISION {
			if !orden {
				operacion_inversa.aplicar(valor_resuelto, valor_esperado)
			} else {
				operacion_inversa.aplicar(valor_esperado, valor_resuelto)
			}
		} else {
			operacion_inversa.aplicar(valor_esperado, valor_resuelto)
		};
		return resolver(hijo_sin_resolver, mapa, valor_necesario, no_resueltos);
	}
	panic!()
}

fn camino(inicio_i: &str, meta_i: &str, mapa: &HashMap<String, Mono>) -> HashSet<Mono>{
	let inicio = mapa.get(inicio_i).unwrap();
	let mut previos: HashMap<Mono, Mono> = HashMap::new();
	let mut abiertos = vec![inicio];

	while abiertos.len() != 0 {
		let actual = abiertos.pop().unwrap();
		let hijos = &actual.hijos;
		if let Some(h) = hijos {
			let hijo_izq = &h.0[0];
			let hijo_der = &h.0[1];
			let mono_izq = mapa.get(hijo_izq).unwrap();
			let mono_der = mapa.get(hijo_der).unwrap();
			previos.insert(mono_izq.clone(), actual.clone());
			previos.insert(mono_der.clone(), actual.clone());
			abiertos.push(mono_izq);
			abiertos.push(mono_der);
		}
	}

	let mut res = HashSet::new();
	let mut actual = mapa.get(meta_i).unwrap();
	res.insert(actual.clone());
	while actual != inicio {
		actual = previos.get(actual).unwrap();
		res.insert(actual.clone());
	}
	return res;
}

fn buscar(actual: Mono, meta: Mono, mapa: &HashMap<String, Mono>) {
	if actual == meta {
		println!("1392\\/");
	}
	if let Some(par) = actual.hijos {
		let hijo_izq = mapa.get(&par.0[0]).unwrap();
		let hijo_der = mapa.get(&par.0[1]).unwrap();
		buscar(hijo_izq.clone(), meta.clone(), mapa);
		buscar(hijo_der.clone(), meta.clone(), mapa);
	}
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
