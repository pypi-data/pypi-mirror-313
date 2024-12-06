import numpy as np
from simba.utils.read_write import read_df
from simba.utils.data import egocentrically_align_pose
from numba import jit


@jit(nopython=True)
def center_rotation_warpaffine_vectors(rotation_vectors: np.ndarray, centers: np.ndarray):
    """ Create WarpAffine vectors for rotating a video around the center """
    results = np.full((rotation_vectors.shape[0], 2, 3), fill_value=np.nan, dtype=np.float64)
    for idx in range(rotation_vectors.shape[0]):
        R, center = rotation_vectors[idx], centers[idx]
        top = np.hstack((R[0, :], np.array([-center[0] * R[0, 0] - center[1] * R[0, 1] + center[0]])))
        bottom = np.hstack((R[1, :], np.array([-center[0] * R[1, 0] - center[1] * R[1, 1] + center[1]])))
        results[idx] = np.vstack((top, bottom))
    return results


@jit(nopython=True)
def align_target_warpaffine_vectors(centers: np.ndarray, target: np.ndarray):
    """ Create WarpAffine for placing original center at new target position """
    results = np.full((centers.shape[0], 2, 3), fill_value=np.nan, dtype=np.float64)
    for idx in range(centers.shape[0]):
        translation_x = target[0] - centers[idx][0]
        translation_y = target[1] - centers[idx][1]
        results[idx] = np.array([[1, 0, translation_x], [0, 1, translation_y]])
    return results




# DATA_PATH = r"C:\Users\sroni\OneDrive\Desktop\rotate_ex\data\501_MA142_Gi_Saline_0513.csv"
# VIDEO_PATH = r"C:\Users\sroni\OneDrive\Desktop\rotate_ex\videos\501_MA142_Gi_Saline_0513.mp4"
# SAVE_PATH = r"C:\Users\sroni\OneDrive\Desktop\rotate_ex\videos\501_MA142_Gi_Saline_0513_rotated.mp4"
# ANCHOR_LOC = np.array([250, 250])
#
# df = read_df(file_path=DATA_PATH, file_type='csv')
# bp_cols = [x for x in df.columns if not x.endswith('_p')]
# data = df[bp_cols].values.reshape(len(df), int(len(bp_cols)/2), 2).astype(np.int32)
#
# _, centers, rotation_vectors = egocentrically_align_pose(data=data, anchor_1_idx=6, anchor_2_idx=2, anchor_location=ANCHOR_LOC, direction=0)
# p = center_rotation_warpaffine_vectors(rotation_vectors=rotation_vectors, centers=centers)
# k = align_target_warpaffine_vectors(centers=centers, target=ANCHOR_LOC)