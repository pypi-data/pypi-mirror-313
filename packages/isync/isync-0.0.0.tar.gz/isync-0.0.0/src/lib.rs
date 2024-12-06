use pyo3::prelude::{pymodule, PyModule, PyResult, Python};

#[pymodule]
fn _isync(_py: Python, module: &PyModule) -> PyResult<()> {
    module.setattr("__version__", env!("CARGO_PKG_VERSION"))?;
    module.setattr("__doc__", env!("CARGO_PKG_DESCRIPTION"))?;
    Ok(())
}
