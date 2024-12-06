import os
from typing import Union, Tuple, Optional
import numpy as np
import functools
import multiprocessing

from simba.utils.checks import check_if_valid_rgb_tuple, check_valid_boolean, check_int, check_file_exist_and_readable, check_if_dir_exists, check_valid_array
from simba.utils.enums import Formats
from simba.utils.read_write import get_video_meta_data, get_fn_ext, find_core_cnt, remove_a_folder



def egocentric_video_aligner(frm_range: np.ndarray,
                              video_path: Union[str, os.PathLike],
                              temp_dir: Union[str, os.PathLike],
                              video_name: str,
                              centers: np.ndarray,
                              rotation_vectors: np.ndarray,
                              target: Tuple[int, int],
                              fill_clr: Tuple[int, int, int] = (255, 255, 255),
                              verbose: bool = False):

    pass

class EgocentricVideoRotator():
    def __init__(self,
                 video_path: Union[str, os.PathLike],
                 centers: np.ndarray,
                 rotation_vectors: np.ndarray,
                 anchor_location: np.ndarray,
                 verbose: bool = True,
                 fill_clr: Tuple[int, int, int] = (0, 0, 0),
                 core_cnt: int = -1,
                 save_path: Optional[Union[str, os.PathLike]] = None):

        check_file_exist_and_readable(file_path=video_path)
        self.video_meta_data = get_video_meta_data(video_path=video_path)
        check_valid_array(data=centers, source=f'{self.__class__.__name__} centers', accepted_ndims=(2,), accepted_axis_1_shape=[2,], accepted_axis_0_shape=[self.video_meta_data['frame_count']], accepted_dtypes=Formats.NUMERIC_DTYPES.value)
        check_valid_array(data=rotation_vectors, source=f'{self.__class__.__name__} rotation_vectors', accepted_ndims=(3,), accepted_axis_0_shape=[self.video_meta_data['frame_count']], accepted_dtypes=Formats.NUMERIC_DTYPES.value)
        check_valid_array(data=anchor_location, source=f'{self.__class__.__name__} anchor_location', accepted_ndims=(1,), accepted_axis_0_shape=[2], accepted_dtypes=Formats.NUMERIC_DTYPES.value)
        check_valid_boolean(value=[verbose], source=f'{self.__class__.__name__} verbose')
        check_if_valid_rgb_tuple(data=fill_clr)
        check_int(name=f'{self.__class__.__name__} core_cnt', value=core_cnt, min_value=-1, unaccepted_vals=[0])
        if core_cnt > find_core_cnt()[0] or core_cnt == -1: self.core_cnt = find_core_cnt()[0]
        else: self.core_cnt = core_cnt
        video_dir, self.video_name, _ = get_fn_ext(filepath=video_path)
        if save_path is not None:
            self.save_dir = os.path.dirname(save_path)
            check_if_dir_exists(in_dir=self.save_dir, source=f'{self.__class__.__name__} save_path')
        else:
            save_path = os.path.join(video_dir, f'{self.video_name}_rotated.mp4')
        self.video_path, self.save_path = video_path, save_path
        self.centers, self.rotation_vectors = centers, rotation_vectors
        self.verbose, self.fill_clr, self.anchor_loc = verbose, fill_clr, anchor_location

    def run(self):
        temp_dir = os.path.join(self.save_dir, 'temp')
        if not os.path.isdir(temp_dir):
            os.makedirs(temp_dir)
        else:
            remove_a_folder(folder_dir=temp_dir)
            #os.makedirs(temp_dir)
        frm_list = np.arange(0, self.video_meta_data['frame_count'])
        frm_list = np.array_split(frm_list, self.core_cnt)
        frm_list = [(cnt, x) for cnt, x in enumerate(frm_list)]



        print(f"Creating rotated video {self.video_name}, multiprocessing (chunksize: {1}, cores: {self.core_cnt})...")
        with multiprocessing.Pool(self.core_cnt, maxtasksperchild=100) as pool:
            constants = functools.partial(egocentric_video_aligner,
                                          temp_dir=temp_dir,
                                          video_name=self.video_name,
                                          video_path=self.video_path,
                                          centers=self.centers,
                                          rotation_vectors=self.rotation_vectors,
                                          target=self.anchor_loc,
                                          verbose=self.verbose,
                                          fill_clr=self.fill_clr)
            for cnt, result in enumerate(pool.imap(constants, frm_list, chunksize=1)):
                print(f"Rotate batch {result}/{self.core_cnt} complete...")
            pool.terminate()
            pool.join()

        pass




# if __name__ == "__main__":
#     from simba.utils.data import egocentrically_align_pose
#     from simba.utils.read_write import read_df
#
#     DATA_PATH = r"C:\Users\sroni\OneDrive\Desktop\rotate_ex\data\501_MA142_Gi_Saline_0513.csv"
#     VIDEO_PATH = r"C:\Users\sroni\OneDrive\Desktop\rotate_ex\videos\501_MA142_Gi_Saline_0513.mp4"
#     SAVE_PATH = r"C:\Users\sroni\OneDrive\Desktop\rotate_ex\videos\501_MA142_Gi_Saline_0513_rotated.mp4"
#
#     ANCHOR_LOC = np.array([250, 250])
#
#     df = read_df(file_path=DATA_PATH, file_type='csv')
#     bp_cols = [x for x in df.columns if not x.endswith('_p')]
#     data = df[bp_cols].values.reshape(len(df), int(len(bp_cols)/2), 2).astype(np.int32)
#
#     _, centers, rotation_vectors = egocentrically_align_pose(data=data, anchor_1_idx=6, anchor_2_idx=2, anchor_location=ANCHOR_LOC, direction=0)
#
#     rotater = EgocentricVideoRotator(video_path=VIDEO_PATH, centers=centers, rotation_vectors=rotation_vectors, anchor_location=ANCHOR_LOC, save_path=SAVE_PATH)
#     rotater.run()
#
#
#


