import numpy as np
import time
from increFeatureSelectionDS import incre_feature_selection_ds

def incre_fea_slt_ds_filter_sam(data, U, curr_ds_vector, fea_slt):
    start_time = time.time()

    row1, _ = data.shape
    row2 = U.shape[0]
    combined_data = np.vstack((data, U))
    _, use_ds = np.unique(combined_data, axis=0, return_index=True)
    use_ds1 = use_ds[use_ds < row1]
    use_ds2 = use_ds[use_ds >= row1] - row1
    unuse_ds = row1 + row2 - len(use_ds)
    NRF = []
    NRS = []

    if len(use_ds2) == 0 or len(use_ds1) == 0:
        in_fea_slt = fea_slt
    else:
        in_fea_slt, NRF, NRS, _ = incre_feature_selection_ds(data[use_ds1, :], U[use_ds2, :], curr_ds_vector[use_ds1], fea_slt)

    time_elapsed = time.time() - start_time
    return in_fea_slt, unuse_ds, NRF, NRS, time_elapsed
