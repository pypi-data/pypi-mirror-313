import numpy as np

ILLUREGION = slice(None,1032), slice(1,1057)
OVERSCANA =  slice(1032,None), slice(None)
OVERSCANB =  slice(None, 1032), slice(1059,None)

def detrend(fid):
    im = fid[0].data
    return im[ILLUREGION] - im[OVERSCANA].mean()


def detrend_full_overscan(fid):
    im = fid[0].data
    res = im - np.mean(im[OVERSCANA], axis=0) #[:-100]
    return np.subtract(res[ILLUREGION].T, np.mean(res[OVERSCANB], axis=1)).T
