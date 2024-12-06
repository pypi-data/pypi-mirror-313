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