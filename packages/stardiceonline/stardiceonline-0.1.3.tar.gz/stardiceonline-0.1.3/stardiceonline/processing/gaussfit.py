import scipy.optimize
import numpy as np
from .ctoolbox import gaussian2d, gaussian2d_der

def normgauss(sigma):
    return 2 * np.pi * sigma ** 2


def vignette(x, y, sigma, nsig, shape):
    #radius = sigma * np.sqrt(-2 * np.log(A))
    radius = sigma * nsig
    xmin = max(0, int(x - radius))
    xmax = min(shape[1], int(x + radius))
    ymin = max(0, int(y - radius))
    ymax = min(shape[0], int(y + radius))
    windowed = (xmin == 0) or (xmax == shape[1]) or (ymin == 0) or (ymax ==  shape[0])
    #print radius, xmax-xmin, ymax - ymin
    return xmin, xmax, ymin, ymax, windowed


def gaussian(x, y, sigma, A, im):
    xmin, xmax, ymin, ymax, windowed = vignette(x, y, sigma, 5, im.shape)
    xim = (np.arange(xmin, xmax) - x).reshape((1, -1))
    yim = (np.arange(ymin, ymax) - y).reshape((-1, 1))
    #xim = (np.arange(im.shape[1]) - x).reshape((1, -1))
    #yim = (np.arange(im.shape[0]) - y).reshape((-1, 1))
    #r = xim * yim / sxy
    alpha = -0.5 / sigma ** 2
    xim *= xim * alpha
    yim *= yim * alpha
    xim = A * np.exp(xim)
    yim = np.exp(yim)
    im[ymin:ymax, xmin:xmax] += xim * yim

def gaussfit(V, x0, y0, A0, sigma0, S, grid, maxfev=10, weight=None, back=True):
    """Least-Square fit of Gaussian shape to 2D histogram

    In contrast to gaussian_weighted_moment below, this can accomodate
    holes, non-null background...

    If weight is None, use inverse sky_variance as weight
    otherwise, sky_variance (S) is only used to compute the errors.
    """
    w = np.sqrt(1/S) if weight is None else np.sqrt(weight)
    #grid = grid[:-1]
    if back:
        def residuals(X):
            return ((V.T - gaussian2d(X, grid)) * w).ravel()
    
        def dr(X):
            Gd = gaussian2d_der(X, grid)
            Gd *= w[:,:,np.newaxis]
            return -Gd.reshape((-1, 7))#/sigma
        X0 = x0, y0, 0.5 / sigma0 ** 2, 0.5 / sigma0 ** 2, 0, A0, 0
    else:
        def residuals(X):
            return ((V.T - gaussian2d(np.hstack([X,0]), grid)) * w).ravel()
        
        def dr(X):
            Gd = gaussian2d_der(np.hstack([X,0]), grid)
            Gd *= w[:,:,np.newaxis]
            return -Gd.reshape((-1, 7))[:,:-1]
        X0 = x0, y0, 0.5 / sigma0 ** 2, 0.5 / sigma0 ** 2, 0, A0

    X, covx, infodict, mesg, val = scipy.optimize.leastsq(residuals, X0, Dfun=dr,
                                                          full_output=True,
                                                          maxfev=maxfev)
    r = residuals(X)
    dof = len(r) - len(X)
   
    if weight is not None:
        J = dr(X)
        VW = S.flatten() * (w.flatten()**2)
        Jleft = VW[:,None]*J # another option is Jleft = (VW*J.T).T
        try:
            covx = np.linalg.pinv(np.dot(J.T, Jleft))
        except (np.linalg.LinAlgError, ValueError):
            pass
    if covx is None:
        return [np.nan] * len(X), [np.nan] * len(X), np.nan, dof, np.nan, r
    else:
        covx *= (r ** 2).sum() / float(dof)
    return X, covx, (r ** 2).sum(), dof, V, r

def gaussian_weighted_moment_variance(data, segm, weightmap, s, gain=None):
    ''' Variance of the Gaussian weighted position and shape estimate
    '''
    det = s['gwmxx'] * s['gwmyy'] - s['gwmxy'] * s['gwmxy']
    if det <= 0 or np.isnan(det):
        s['vgwx'] = np.nan
        s['vgwy'] = np.nan
        s['vgwxy'] = np.nan
        s['unconverged'] = True
        return s
    xmin, xmax, ymin, ymax, s['windowed'] = vignette(s['gwx'], s['gwy'], np.sqrt(np.sqrt(det)), 4, data.shape)
    cut = slice(ymin, ymax), slice(xmin, xmax)
    _x, _y = np.mgrid[xmin:xmax, ymin:ymax]
    _x = _x.T.ravel()
    _y = _y.T.ravel()
    dx = _x - s['gwx']
    dy = _y - s['gwy']
    wxx = s['gwmyy'] / det
    wyy = s['gwmxx'] / det
    wxy = -s['gwmxy'] / det
    wg = wxx * dx * dx + wyy * dy * dy + 2 * wxy * dx * dy
    goods = wg < 16
    #print 'used : %f' % (goods.sum()/float(len(goods)))
    
    seg = segm[cut].ravel()[goods]
    s['contaminated'] = ((seg != 0) & (seg != s['objid'])).any()
    
    var = weightmap[cut].ravel()[goods]
    s['hasbads'] = (var == 0).any()
    var = 1/var
    if gain is not None:
        var += data[cut].ravel()[goods] / gain

    wg = np.exp(-0.5 * wg[goods])
    wgi = wg * data[cut].ravel()[goods]
    f = np.sum(wgi)
        
    wg *= wg
    dx = dx[goods]
    dy = dy[goods]

    f *= f * 0.25 # factor 2 in the estimate
    s['vgwx'] = (wg * dx * dx * var).sum()
    s['vgwy'] = (wg * dy * dy * var).sum()
    s['vgwxy'] = (wg * dx * dy * var).sum()
    s['vgwx'] /= f
    s['vgwy'] /= f
    s['vgwxy'] /= f

    return s
