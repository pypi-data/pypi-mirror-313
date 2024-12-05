import numpy as np

def in_dis_vec(data, U, x, curr_val):
    row1 = data.shape[0]
    row, col = U.shape
    diff_dec = (data[x, col-1] != U[:, col-1])
    curr = np.ones(row, dtype=bool)
    in_val = np.sum(np.max(U[diff_dec, :-1] != data[x, :-1], axis=1))
    in_val = (in_val + curr_val*row1) / (row1 + row)
    return in_val

def incre_discernible_score(data, U, sam_left1, sam_left2, curr_ds_vector, add_ds_vector):
    NL1 = len(sam_left1)
    NL2 = len(sam_left2)
    in_ds_vec = np.zeros(NL1)
    in_add_ds_vec = np.zeros(NL2)
    
    for i in range(NL1):
        in_ds_vec[i] = in_dis_vec(data, U, sam_left1[i], curr_ds_vector[i])
    
    for i in range(NL2):
        in_add_ds_vec[i] = in_dis_vec(U, data, sam_left2[i], add_ds_vector[i])
    
    in_ds = np.sum(in_ds_vec) + np.sum(in_add_ds_vec)
    in_ds /= (NL1 + NL2)
    
    return in_ds, in_ds_vec, in_add_ds_vec
