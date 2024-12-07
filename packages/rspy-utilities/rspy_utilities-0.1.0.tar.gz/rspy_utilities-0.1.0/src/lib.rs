use pyo3::prelude::*;
use pyo3::types::{PyIterator, PySet};

#[pyclass]
struct DistinctIter {
    iter: Py<PyIterator>,
    seen: Py<PySet>,
    key: Option<Py<PyAny>>,
}

impl Iterator for DistinctIter {
    type Item = PyResult<PyObject>;

    fn next(&mut self) -> Option<Self::Item> {
        Python::with_gil(|py| {
            let iter = self.iter.bind(py);
            while let Ok(item) = iter.call_method0("__next__") {
                let key_value = if let Some(ref k) = self.key {
                    match k.bind(py).call1((item.clone(),)) {
                        Ok(v) => v,
                        Err(e) => return Some(Err(e)),
                    }
                } else {
                    item.clone()
                };

                let seen = self.seen.bind(py);
                if !seen
                    .call_method1("__contains__", (key_value.clone(),))
                    .unwrap()
                    .extract::<bool>()
                    .unwrap()
                {
                    seen.call_method1("add", (key_value,)).unwrap();
                    match item.into_pyobject(py) {
                        Ok(obj) => return Some(Ok(obj.unbind())),
                        Err(e) => return Some(Err(e.into())),
                    }
                }
            }
            None
        })
    }
}

#[pyfunction]
#[pyo3(signature = (iterable, key=None))]
fn distinct<'py>(
    py: Python<'py>,
    iterable: &Bound<'py, PyAny>,
    key: Option<PyObject>,
) -> PyResult<Py<DistinctIter>> {
    let seen = PySet::empty(py)?;
    let iter = iterable.try_iter()?;

    let distinct_iter = DistinctIter {
        iter: iter.into_pyobject(py)?.unbind(),
        seen: seen.into_pyobject(py)?.unbind(),
        key,
    };

    Py::new(py, distinct_iter)
}

#[pymodule]
fn _rspy_utilities(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(distinct, m)?)?;
    Ok(())
}
#[pymethods]
impl DistinctIter {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&mut self) -> Option<PyObject> {
        self.next().transpose().ok().flatten()
    }
}
