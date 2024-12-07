import numpy as np

def crop_2d_image(image, ori, range):
    """
    ori(y,x)
    offset(height,width)
    """
    # Extract origin and offset
    ori_y, ori_x = ori
    height, width = range

    # Compute the crop bounds
    start_y = max(0, ori_y)  # Ensure origin is within bounds
    start_x = max(0, ori_x)
    end_y = min(image.shape[0], ori_y + height)  # Ensure the crop does not exceed the image dimensions
    end_x = min(image.shape[1], ori_x + width)

    # Crop the image
    cropped_image = image[start_y:end_y, start_x:end_x]
    
    return cropped_image

def norm_data(data):
    """
    normalize data to have mean=0 and standard_deviation=1
    """
    mean_data=np.mean(data)
    std_data=np.std(data, ddof=1)
    #return (data-mean_data)/(std_data*np.sqrt(data.size-1))
    return (data-mean_data)/(std_data)


def ncc(data0, data1):
    """
    normalized cross-correlation coefficient between two data sets

    Parameters
    ----------
    data0, data1 :  numpy arrays of same size
    """
    return (1.0/(data0.size-1)) * np.sum(norm_data(data0)*norm_data(data1))

def get_ncc_point_to_whole(pos,feats_map:np.ndarray):
    """
    calculate the ncc between feature at pos and the other features in feat_list
    return the ncc_map, notice: only accept "square"feature list

    Parameters
    ----------
    pos: the position of the sample point on ori_feats_map
    ori_feats: a feature_list 
    """
    template=feats_map[pos[0],pos[1]]
    
    ncc_list=[]
    for i in range(feats_map.shape[0]):
        for j in range(feats_map.shape[1]):
            # my_tools.plot([temp])
            temp=feats_map[i,j]
            ncc_list.append(ncc(template,temp))
    ncc_map=np.array(ncc_list)
    shape=feats_map.shape[:-1]
    ncc_map=ncc_map.reshape(shape)
    return ncc_map
