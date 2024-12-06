import cv2
import numba
import numpy as np


@numba.jit(nopython=True)
def warp_affine_numpy(frames, rotation_matrices):
    N, H, W, C = frames.shape
    warped_frames = np.zeros_like(frames)

    # Create empty arrays for coordinates
    y_coords = np.zeros((H, W), dtype=np.int32)
    x_coords = np.zeros((H, W), dtype=np.int32)

    # Manually generate coordinate grids (equivalent to np.meshgrid)
    for i in range(H):
        for j in range(W):
            y_coords[i, j] = i
            x_coords[i, j] = j

    # Create a new coordinate grid for the transformed coordinates
    new_x = np.zeros((H, W), dtype=np.int32)
    new_y = np.zeros((H, W), dtype=np.int32)

    # Apply transformations to each frame
    for i in range(N):
        frame = frames[i]
        rotation_matrix = rotation_matrices[i]

        # Affine matrix (rotation and scaling) and translation vector
        affine_matrix = rotation_matrix[:2, :2]
        translation = rotation_matrix[:2, 2]

        # Apply the affine transformation to the coordinate grid
        for r in range(H):
            for c in range(W):
                # Apply the affine transformation
                new_x_val = affine_matrix[0, 0] * x_coords[r, c] + affine_matrix[0, 1] * y_coords[r, c] + translation[0]
                new_y_val = affine_matrix[1, 0] * x_coords[r, c] + affine_matrix[1, 1] * y_coords[r, c] + translation[1]

                # Manually clip the coordinates to ensure valid indices (without np.clip)
                new_x[r, c] = min(max(new_x_val, 0), W - 1)
                new_y[r, c] = min(max(new_y_val, 0), H - 1)

        # Assign transformed pixel values to the warped frame, one pixel at a time
        for r in range(H):
            for c in range(W):
                for ch in range(C):  # For each channel (RGB)
                    warped_frames[i, new_y[r, c], new_x[r, c], ch] = frame[y_coords[r, c], x_coords[r, c], ch]

    return warped_frames


from simba.utils.read_write import read_df, read_img_batch_from_video_gpu
from simba.utils.data import egocentrically_align_pose
from simba.sandbox.warp_numba import center_rotation_warpaffine_vectors, align_target_warpaffine_vectors

DATA_PATH = r"/mnt/c/Users/sroni/OneDrive/Desktop/rotate_ex/data/501_MA142_Gi_Saline_0513.csv"
VIDEO_PATH = r"/mnt/c/Users/sroni/OneDrive/Desktop/rotate_ex/videos/501_MA142_Gi_Saline_0513.mp4"
SAVE_PATH = r"/mnt/c/Users/sroni/OneDrive/Desktop/rotate_ex/videos/501_MA142_Gi_Saline_0513_rotated.mp4"
ANCHOR_LOC = np.array([300, 300])

df = read_df(file_path=DATA_PATH, file_type='csv')
bp_cols = [x for x in df.columns if not x.endswith('_p')]
data = df[bp_cols].values.reshape(len(df), int(len(bp_cols)/2), 2).astype(np.int64)
data, centers, rotation_matrices = egocentrically_align_pose(data=data, anchor_1_idx=6, anchor_2_idx=2, anchor_location=ANCHOR_LOC, direction=180)
imgs = read_img_batch_from_video_gpu(video_path=VIDEO_PATH, start_frm=0, end_frm=100)

rot_matrices_center = center_rotation_warpaffine_vectors(rotation_vectors=rotation_matrices, centers=centers)
rot_matrices_align = align_target_warpaffine_vectors(centers=centers, target=ANCHOR_LOC)

imgs_centered = warp_affine_numpy(frames=imgs, rotation_matrices=rot_matrices_center)
imgs_centered = warp_affine_numpy(frames=imgs_centered, rotation_matrices=rot_matrices_align)