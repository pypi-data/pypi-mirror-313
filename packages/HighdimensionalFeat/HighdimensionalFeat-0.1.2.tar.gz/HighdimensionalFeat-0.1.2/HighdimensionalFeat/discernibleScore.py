import numpy as np

def discerbile_vec(data, x):
    diff_dec = (data[x, -1] != data[:, -1])
    if diff_dec.any():
        data_filtered = data[diff_dec, :-1] - data[x, :-1]
        # data_filtered empty? 
        if data_filtered.size > 0:
            inVal = np.sum(np.max(data_filtered, axis=1))
        else:
            inVal = 0
    else:
        inVal = 0
    return inVal

def discernible_score(data, sample_left):
    NL = len(sample_left)
    ds_vector = np.zeros(NL)
    for i in range(NL):
        ds_vector[i] = discerbile_vec(data, sample_left[i])
    DS = np.sum(ds_vector) / NL if NL > 0 else 0
    return DS, ds_vector
