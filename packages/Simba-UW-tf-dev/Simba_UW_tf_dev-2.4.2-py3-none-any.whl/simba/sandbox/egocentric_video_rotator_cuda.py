import os
from typing import Union, Tuple, Optional
import numpy as np
import functools
import multiprocessing
import cv2

from simba.utils.checks import check_if_valid_rgb_tuple, check_valid_boolean, check_int, check_file_exist_and_readable, check_if_dir_exists, check_valid_array, check_valid_tuple
from simba.utils.enums import Formats
from simba.utils.read_write import get_video_meta_data, get_fn_ext, find_core_cnt, remove_a_folder, read_frm_of_video, concatenate_videos_in_folder, read_df
from simba.utils.printing import SimbaTimer, stdout_success
from simba.utils.data import egocentrically_align_pose




DATA_PATH = r"/mnt/c/Users/sroni/OneDrive/Desktop/rotate_ex/data/501_MA142_Gi_Saline_0513.csv"
VIDEO_PATH = r"/mnt/c/Users/sroni/OneDrive/Desktop/rotate_ex/videos/501_MA142_Gi_Saline_0513.mp4"
SAVE_PATH = r"/mnt/c/Users/sroni/OneDrive/Desktop/rotate_ex/videos/501_MA142_Gi_Saline_0513_rotated.mp4"
ANCHOR_LOC = np.array([250, 250])

df = read_df(file_path=DATA_PATH, file_type='csv')
bp_cols = [x for x in df.columns if not x.endswith('_p')]
data = df[bp_cols].values.reshape(len(df), int(len(bp_cols)/2), 2).astype(np.int32)

_, centers, rotation_vectors = egocentrically_align_pose(data=data, anchor_1_idx=6, anchor_2_idx=2, anchor_location=ANCHOR_LOC, direction=0)