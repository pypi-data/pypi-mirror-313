import numpy as np
import time
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


def fast_feature_selection_ds(data):
    start_time = time.time()

    row, col = data.shape
    fea_slt = np.array([], dtype=int)  
    fea_left = np.arange(col - 1)  
    sam_left = np.arange(row)  

    # Obtaining discernible score for all samples
    _, ds_vector = discernible_score(data, sam_left)
    DSSamLeft = 0
    fea_redun = []  # To store redundant features
    sam_delete = []  # To store deleted samples

    while len(sam_left) > 0 and len(fea_left) > 0:
        tempDS = np.zeros(len(fea_left))
        for i, fea in enumerate(fea_left):
            selected_features = np.append(fea_slt, fea)  
            _, temp_ds_vec = discernible_score(data[:, np.append(selected_features, col-1)], sam_left)
            tempDS[i] = np.sum(temp_ds_vec) / len(sam_left)  # Calculating the average discernible score

        maxNum, maxInd = np.max(tempDS), np.argmax(tempDS)  
        fea_slt = np.append(fea_slt, fea_left[maxInd])  
        fea_left = np.delete(fea_left, maxInd)  # Removing the selected feature from the list of remaining features

        tempDS = np.delete(tempDS, maxInd)  # Removing the discernible score of the selected feature
        filter_mask = tempDS - DSSamLeft > 0.001  
        fea_left = fea_left[filter_mask]  

        fea_redun.append(len(fea_left))  # Updating the number of redundant features
        dsVector_diff = ds_vector[sam_left] - temp_ds_vec  # Calculating the difference in discernible score
        NDelSam = np.where(dsVector_diff <= 0.001)[0]
        sam_left = np.delete(sam_left, NDelSam)  # Removing redundant samples
        sam_delete.append(len(NDelSam))  # Updating the number of deleted samples

        DSSamLeft = maxNum  # Updating the total discernible score

    time_elapsed = time.time() - start_time  

    return fea_slt.tolist(), ds_vector, fea_redun, sam_delete, time_elapsed
