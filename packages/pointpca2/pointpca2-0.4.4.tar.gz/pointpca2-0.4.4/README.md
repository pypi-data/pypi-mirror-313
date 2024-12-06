# PointPCA2 - Python Lib
#### A seamless Python integration to the Rust implementation of PointPCA2

This project aims to integrate Python to [pointpca2-rs](https://github.com/akaTsunemori/pointpca2-rs), enabling the use of Python's comprehensive data science tools combined to the performance provided by the Rust implementation of PointPCA2.

## Setup
### From PyPI
```bash
pip install pointpca2
# or
python -m pip install pointpca2
```

### From source
- **Prerequisites**
  - rustc == 1.77.2
  - anaconda3 >= 23.7.4

- **Build**
```bash
# Clone this repository
https://github.com/akaTsunemori/pointpca2-pylib.git

# cd into the project folder
cd pointpca2-pylib

# Setup and activate the conda environment
conda env create -f environment.yml
conda activate pointpca2-pylib

# Compile the project into a python module using maturin
maturin develop -r
```

## Usage
```python
import open3d as o3d
import numpy as np
import pointpca2

# Load both reference and test PCs
PC_REF_PATH = "examples/pcs/amphoriskos_vox10.ply"
pc_ref = o3d.io.read_point_cloud(PC_REF_PATH)
points_a, colors_a = np.asarray(pc_ref.points), np.asarray(pc_ref.colors)
PC_TEST_PATH = "examples/pcs/tmc13_amphoriskos_vox10_dec_geom01_text01_octree-predlift.ply"
pc_test = o3d.io.read_point_cloud(PC_TEST_PATH)
points_b, colors_b = np.asarray(pc_test.points), np.asarray(pc_test.colors)

# Compute the features (predictors) through the pointpca2 function
predictors = pointpca2.compute_pointpca2(
    points_a, colors_a, points_b, colors_b, search_size=81, verbose=True
)
print(*predictors)
```

## Contributing
Feel free to open any kind of issues and contributions related to this Python package. Issues related to the Rust implementation should be open on the [pointpca2-rs](https://github.com/akaTsunemori/pointpca2-rs) repository.

## Acknowledgments
- [pointpca2-rs](https://github.com/akaTsunemori/pointpca2-rs) - An implementation of PointPCA2 in Rust

## License
MIT License

---

> GitHub [@akaTsunemori](https://github.com/akaTsunemori)
