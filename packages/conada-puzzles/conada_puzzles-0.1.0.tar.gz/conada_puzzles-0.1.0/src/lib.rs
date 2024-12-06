use pyo3::{exceptions::PyValueError, prelude::*};
use std::collections::HashMap;
use std::usize;
use std::sync::Arc;
use rand::seq::SliceRandom;
use rand::thread_rng;
use tokio::runtime::Runtime;
use futures;

/// A Python class implemented in Rust.
#[pyclass]
struct Planes {
    #[pyo3(get, set)]
    passengers: u64,
    #[pyo3(get, set)]
    seats: u64,
    #[pyo3(get, set)]
    cols: Vec<char>,
}

#[pymethods]
impl Planes {
    #[new]
    #[pyo3(signature = (passengers=100, seats=100, cols="ABCDEF".to_string()))]
    fn new(passengers: Option<u64>, seats: Option<u64>, cols: Option<String>) -> PyResult<Self> {
        let p = Planes{
            passengers: passengers.expect("Expected passengers"),
            seats: seats.expect("Expected seats"), 
            cols: cols.expect("Expected cols for each row on the plane").chars().collect(),
        };
        if p.passengers > p.seats {
            Err(PyValueError::new_err("Can't have more seats than passengers."))
        } else {
            Ok(p)
        }
    }

    fn run_simulation(&self) -> bool {
        let assigned_seating = self.generate_seating();

        let mut open_seats: Vec<String> = assigned_seating.values().cloned().collect();
        let mut seat: String = "00".to_string();
        for p in 1..=self.passengers {
            if (p == 1) || ( !open_seats.contains(&assigned_seating[&p].to_string()) ) {
                seat = open_seats.choose(&mut thread_rng()).unwrap().to_string();
                let index = open_seats.iter().position(|x| *x == seat).unwrap();
                open_seats.remove(index);
            } else {
                seat = assigned_seating[&p].clone();
                let index = open_seats.iter().position(|x| *x == seat).unwrap();
                open_seats.remove(index);
            }
        }
        if seat == assigned_seating[&self.passengers] {
            true
        } else {
            false
        }
    }

    fn run_simulations(&self, iterations: u64) -> f64 {
        let planes = Arc::new(self.clone());

        let runtime = Runtime::new().expect("Failed to create Tokio runtime");

        let success_rate = runtime.block_on(async {
            let mut tasks = Vec::new();

            for _ in 0..iterations {
                let simulation = Arc::clone(&planes);
                tasks.push(tokio::spawn(async move { simulation.run_simulation() }));
            }

                let results = futures::future::join_all(tasks).await;
                let num_success = results.into_iter().filter(|res| matches!(res, Ok(true))).count();
            num_success as f64 / iterations as f64
        });

        success_rate
    }
    
    fn generate_seating(&self) -> HashMap<u64, String> {
        // Generate available seats
        let mut available_seats = Vec::new();
        for i in 0..self.seats {
            available_seats.push(format!("{}{}", (i+6 / 6), self.cols.get((i % 6) as usize).unwrap()));
        }

        // Randomize the seating
        let mut rng = thread_rng();
        available_seats.shuffle(&mut rng);

        // Assign seating
        let mut seating = HashMap::new();
        for i in 1..=self.passengers {
            seating.insert(i, available_seats.get((i-1) as usize).expect("Seat on a plane").to_string());
        }
        seating
    }

}

impl Clone for Planes {
    fn clone(&self) -> Self {
        Planes {
            passengers: self.passengers,
            seats: self.seats,
            cols: self.cols.clone(),
        }
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn conada_puzzles(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Planes>()?;
    Ok(())
}


