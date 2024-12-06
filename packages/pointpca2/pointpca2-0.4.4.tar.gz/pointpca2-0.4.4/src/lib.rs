extern crate nalgebra as na;
extern crate numpy;
extern crate pointpca2_rs;
extern crate rayon;

mod utils;

use numpy::PyArray1;
use numpy::PyReadonlyArray2;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use utils::as_dmatrix;
use utils::build_thread_pool;

#[pyfunction]
fn compute_pointpca2<'py>(
    _py: Python<'py>,
    points_a: PyReadonlyArray2<'py, f64>,
    colors_a: PyReadonlyArray2<'py, u8>,
    points_b: PyReadonlyArray2<'py, f64>,
    colors_b: PyReadonlyArray2<'py, u8>,
    search_size: usize,
    max_workers: usize,
    verbose: bool,
) -> &'py PyArray1<f64> {
    let points_a = as_dmatrix(points_a);
    let colors_a = as_dmatrix(colors_a);
    let points_b = as_dmatrix(points_b);
    let colors_b = as_dmatrix(colors_b);
    let pool = build_thread_pool(max_workers);
    let pooled_predictors = pool.install(|| {
        pointpca2_rs::compute_pointpca2(
            points_a,
            colors_a,
            points_b,
            colors_b,
            search_size,
            verbose,
        )
    });
    let py_array = PyArray1::from_iter(_py, pooled_predictors.iter().cloned());
    py_array
}

#[pymodule]
fn pointpca2(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(compute_pointpca2, m)?)?;
    Ok(())
}
