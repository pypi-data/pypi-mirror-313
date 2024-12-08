use pyo3::prelude::*;

#[pymodule]
fn signal_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    println!("signal_rs module initialized");
    Ok(())
}



