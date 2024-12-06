use na::DMatrix;
use numpy::PyReadonlyArray2;
use rayon::ThreadPool;
use rayon::ThreadPoolBuilder;

pub fn as_dmatrix<T>(x: PyReadonlyArray2<T>) -> DMatrix<T>
where
    T: numpy::Element + na::Scalar,
{
    let data: Vec<T> = x.as_array().iter().cloned().collect();
    DMatrix::from_row_slice(x.shape()[0], x.shape()[1], &data)
}

pub fn build_thread_pool(max_workers: usize) -> ThreadPool {
    let pool = ThreadPoolBuilder::new()
        .num_threads(max_workers)
        .build()
        .expect("Failed to build thread pool");
    pool
}
