import numpy as np
import time
from HDDFeatures.discernibleScore import discernible_score
from HDDFeatures.increDiscernibleScore import incre_discernible_score

def incre_feature_selection_ds(data, U, curr_ds_vector, fea_slt):
    start_time = time.time()

    row1, col = data.shape
    row2 = U.shape[0]
    sam_left1 = np.arange(row1)
    sam_left2 = np.arange(row2)
    fea_left = np.setdiff1d(np.arange(col - 1), fea_slt)  # Removing already selected features
    NRF = []
    NRS = []

    _, add_ds_vector = discernible_score(U, sam_left2)
    in_ds, in_ds_vec, in_add_ds_vec = incre_discernible_score(data, U, sam_left1, sam_left2, curr_ds_vector, add_ds_vector)
    _, add_fea_ds_vec = discernible_score(U[:, np.append(fea_slt, col-1)], sam_left2)
    in_fea_ds, _, _ = incre_discernible_score(data[:, np.append(fea_slt, col-1)], U[:, np.append(fea_slt, col-1)], sam_left1, sam_left2, curr_ds_vector, add_fea_ds_vec)

    if in_ds - in_fea_ds <= 0.001:
        in_fea_slt = fea_slt
    else:
        add_fea = []
        left_sam_ds = 0
        num_curr = 1
        while len(fea_left) > 0 and (len(sam_left1) + len(sam_left2)) > 0:
            temp_in_ds = np.zeros(len(fea_left))
            for i, fea in enumerate(fea_left):
                selected_features = np.append(fea_slt, fea)
                _, fea_ds_vec = discernible_score(U[:, selected_features], sam_left2)
                _, ds_vec = discernible_score(data[:, selected_features], sam_left1)
                temp_in_ds[i], _, _ = incre_discernible_score(data[:, selected_features], U[:, selected_features], sam_left1, sam_left2, ds_vec, fea_ds_vec)
            max_num, max_ind = np.max(temp_in_ds), np.argmax(temp_in_ds)
            add_fea = np.append(add_fea, fea_left[max_ind])
            mask = temp_in_ds - left_sam_ds < 0.001
            
            # Update the mask to ensure its size matches fea_left after removal
            mask = np.delete(mask, max_ind)
            fea_left = np.delete(fea_left, max_ind)
            fea_left = fea_left[mask]
            NRF.append(len(fea_left))
            del_sam1 = in_ds_vec - temp_in_ds[max_ind] <= 0.001
            del_sam2 = in_add_ds_vec - temp_in_ds[max_ind] <= 0.001
            sam_left1 = np.delete(sam_left1, np.where(del_sam1)[0])
            sam_left2 = np.delete(sam_left2, np.where(del_sam2)[0])
            NRS.append(np.sum(del_sam1) + np.sum(del_sam2))
            left_sam_ds = max_num
            num_curr += 1

        in_fea_slt = np.unique(np.append(fea_slt, add_fea))

    time_elapsed = time.time() - start_time
    return in_fea_slt, NRF, NRS, time_elapsed
