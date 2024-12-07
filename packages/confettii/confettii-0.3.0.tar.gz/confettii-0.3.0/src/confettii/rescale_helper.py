import numpy as np
from scipy.ndimage import zoom

def get_hr_mask(lr_mask,indexs,roi_size,scale,zoom_order=0):
    """
    roi is defined via indexs +roi_size
    """
    lr_indexs=[int(idx/scale)for idx in indexs]
    # lr_roi_size=[int(roi/scale)for roi in roi_size]
    lr_roi_size = [max(int(roi / scale), 1) for roi in roi_size]
    z,y,x=lr_indexs
    z_size,y_size,x_size=lr_roi_size

    # print(f"hr_index:{indexs}, lr_index:{lr_indexs}")
    # print(f"lr_roi_size:{lr_roi_size}")
    # print(f"target_roi_size:{roi_size}")

    #mask in order (z,y,x)
    lr_mask_roi=lr_mask[z:z+z_size,y:y+y_size,x:x+x_size]
    zoom_factors=[t/s for t,s in zip(roi_size,lr_roi_size)]
    zoomed_mask_roi=zoom(lr_mask_roi,zoom=zoom_factors,order=zoom_order)
    zoomed_mask_roi=np.squeeze(zoomed_mask_roi)


    return zoomed_mask_roi