import numpy as np

def bool_loc_1d(x_sel, x_all): 
    
    idx = []
    for x0 in x_all:
        if x0 in x_sel:
            idx.append(True)
        else:
            idx.append(False) 
    idx = np.array(idx).squeeze()
    
    return idx

