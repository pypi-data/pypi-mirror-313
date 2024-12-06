use instruction_decoder::Decoder;
use pyo3::{exceptions::PyValueError, prelude::*};

/// A Python module implemented in Rust.
#[pymodule]
fn pyinstruction_decoder(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyDecoder>()?;
    Ok(())
}

#[pyclass]
struct PyDecoder(Decoder);

#[pymethods]
impl PyDecoder {
    #[new]
    fn py_new(instruction_set_tomls: Vec<String>) -> PyResult<Self> {
        match Decoder::new(&instruction_set_tomls) {
            Ok(d) => Ok(Self(d)),
            Err(errs) => Err(PyValueError::new_err(errs)),
        }
    }

    fn decode_from_string(&self, instruction: String, bit_width: usize) -> PyResult<String> {
        match self.0.decode_from_string(instruction.as_str(), bit_width) {
            Ok(s) => Ok(s),
            Err(s) => Err(PyValueError::new_err(s)),
        }
    }

    fn decode(&self, instruction: u128, bit_width: usize) -> PyResult<String> {
        match self.0.decode(instruction, bit_width) {
            Ok(s) => Ok(s),
            Err(s) => Err(PyValueError::new_err(s)),
        }
    }

    fn decode_from_bytes(&self, instruction: Vec<u8>, bit_width: usize) -> PyResult<String> {
        match self.0.decode_from_bytes(instruction, bit_width) {
            Ok(s) => Ok(s),
            Err(s) => Err(PyValueError::new_err(s)),
        }
    }
}
