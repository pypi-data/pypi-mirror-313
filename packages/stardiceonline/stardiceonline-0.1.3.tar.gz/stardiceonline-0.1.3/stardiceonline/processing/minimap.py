''' Tools to produce superpixellized images, background maps ...

'''
import numpy as np
import scipy.interpolate

def rebin(data, n=16, reduce=np.mean):
    return reduce(reduce(data.reshape((data.shape[0] // n, n,
                                       data.shape[1] // n, n)
                                      ), axis=1), axis=-1)

def minimap(im, segm, nside=256, deads=None):
    mask = segm != 0
    if deads is not None:
        mask[deads]=1
    im2 = np.ma.MaskedArray(im, mask=mask)
    im2 = im2.reshape((im2.shape[0] // nside, nside,
                        im2.shape[1] // nside, nside))
    mini = im2.mean(axis=1).mean(axis=-1)
    residual = (im2 - mini[:, None, :, None]).filled(0)
    im2.mask |= np.abs(residual) > 3 * residual.std()
    mini = im2.mean(axis=1).mean(axis=-1)
    #residual = (im2 - mini[:, None, :, None]).filled(0).reshape(*im.shape)
    #std = im2.std() / 0.986 
    stdmap = im2.std(axis=(1,3))
    std = stdmap.mean() / 0.986 # 3 sigma clip correction
    return mini.filled(mini.mean()), std, stdmap


def interpolate(im, nside, shape=None, deg=3):
    try:
        nside[0]
    except:
        nside = [nside, nside]
    if shape is None:
        shape = np.array(im.shape) * np.array(nside)
    x = np.arange(nside[0] // 2, shape[0], nside[0])
    y = np.arange(nside[1] // 2, shape[1], nside[1])
    S = scipy.interpolate.RectBivariateSpline(x, y, im, kx=deg, ky=deg)
    return S(np.arange(0.5, shape[0]), np.arange(0.5, shape[1]))

if __name__ == '__main__':
    import imageproc.image
    import imageproc.visu
    import imageproc.catalog
    import imageproc.instruments
    reload(imageproc.image)
    reload(imageproc.visu)
    reload(imageproc.catalog)
    reload(imageproc.instruments)
    from imageproc.image import Image
    from imageproc.catalog import ImageObjects
    
    im = Image('../src/calibrated.fits')
    #im.dead = np.where(pyfits.getdata('../src/dead.fits'))
    deads = im.instru.get_dead('../src/')
    segm, nobj = im.segment(5, 3)
    print(('found %d detection' % nobj))
    mini, sigmaback, residuals = minimap(im.data, segm, deads=deads)

    back = scipy.ndimage.zoom(mini.filled(), 256, prefilter=False, order=3)
    
    from imageproc.visu import Visu
    v = Visu()
    v.im(im.data * (segm == 0))
    v.im_new_frame(mini.filled())
    v.im_new_frame(back)
    #from imageproc.visu import Visu
    #from saunerie.robuststat import robust_average

