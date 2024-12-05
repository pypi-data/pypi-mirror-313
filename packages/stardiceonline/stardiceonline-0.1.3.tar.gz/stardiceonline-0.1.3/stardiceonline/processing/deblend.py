import numpy as np
from . import gaussfit
from . import ctoolbox 
from . import catalog

def assign_pixel_to_obj(partseg, data, weights, segm, cut, nobj, id, newobj, s):
    '''Assign pixels to the most likely sub-source based on a crude
estimate of the flux contribution of each source

    The segmentation map is modified so that the first object keeps
    the original id and subsources get unused ids

    See assign_pixel_to_obj_em for something more sophisticated but
    also less reliable.

    '''
    ids = np.hstack([id, np.arange(nobj + 1, nobj + newobj)])
    x, y = np.mgrid[cut[1].start:cut[1].stop, cut[0].start:cut[0].stop]
    x = x.T
    y = y.T
    subcat = []
    V = data[cut]
    #grid = np.array([0, V.shape[1], 0, V.shape[0]])
    w = weights[cut]
    objest = []
    for i in range(newobj):
        s['blended'] = True
        s['objid'] = ids[i]
        mask = np.flatnonzero(partseg == (i+1))
        # Put back coordinates in the global frame
        catalog.isophotal_measurements(s, V.flat[mask], x.flat[mask], y.flat[mask], w=None)
        subcat.append(s.copy())
        det = s['mxx'] * s['myy'] - s['mxy'] * s['mxy']
        if (det <= 0):
            s['mxx'] = 1
            s['myy'] = 1
            s['mxy'] = 0
            det=1
        A = s['fiso'] / np.sqrt(det)
        _x = x - s['x']
        _y = y - s['y']
        arg = -0.5 * ((s['myy']/det) * _x * _x + (s['mxx']/det) * _y * _y - s['mxy']/det * _x * _y)
        objest.append(A*np.exp(arg))
    # Update the segmentation map
    objest = np.array(objest)
    newseg = ids[objest.argmax(axis=0)]
    footprint = segm[cut] == id
    segm[cut][footprint] = newseg[footprint]
    # We restart isophotal measurement so that they match the segmentation map
    # TODO We could also run the gaussian weighted stuff
    # isophotal_measurements(s, V.flat[mask], x[mask], y[mask], w=w.flat[mask])
    for i in range(newobj):
        mask = np.flatnonzero(segm[cut] == ids[i])
        # Put back coordinates in the global frame
        catalog.isophotal_measurements(subcat[i], V.flat[mask], x.flat[mask], y.flat[mask], w=None)
        det = subcat[i]['mxx'] * subcat[i]['myy'] - subcat[i]['mxy'] * subcat[i]['mxy']
        if (det <= 0):
            subcat[i]['mxx'] = 1
            subcat[i]['myy'] = 1
            subcat[i]['mxy'] = 0

    return segm, nobj + newobj - 1, subcat


def assign_pixel_to_obj_em(partseg, data, weights, segm, cut, nobj, id, newobj, s):
    '''Assign pixels to the most likely source based on a the estimated flux contribution of each source

    The segmentation map is modified so that the first object keeps
    the original id and subsources get unused ids

    '''
    x, y = np.mgrid[cut[1].start:cut[1].stop, cut[0].start:cut[0].stop]
    x, y = x.T, y.T
    V = data[cut]
    T, xc, yc, mxx, myy, mxy, converged = em(partseg, newobj, V, fit_center=False, plant=id==980)
    ids = np.hstack([id, np.arange(nobj + 1, nobj + newobj)])
    newseg = ids[T.argmax(axis=-1)]
    footprint = segm[cut] == id
    segm[cut][footprint] = newseg[footprint]
    subcat = []
    for i in range(newobj):
        s['blended'] = True
        s['objid'] = ids[i]
        mask = np.flatnonzero((newseg == ids[i]) & footprint)
        if not mask.any():
            print("Deblended source suppressed by em estimate")
            continue
        s['gwx'] = cut[1].start + yc[i]# Put back coordinates in the global frame
        s['gwy'] = cut[0].start + xc[i]
        s['gwmxx'] = myy[i]
        s['gwmyy'] = mxx[i]
        s['gwmxy'] = mxy[i]
        s['unconverged'] = not converged
        catalog.isophotal_measurements(s, V.flat[mask], x.flat[mask], y.flat[mask], w=weights[cut].flat[mask])
        subcat.append(s.copy())
    if id == 980:
        stop
    return segm, nobj + newobj - 1, subcat

def em(segm, nobj, vignette, fit_center=True, plant=False):
    ''' Expectation-Maximisation algorithm for gaussian mixture estimate

    Translating that into C would speed up, not called that often though
    '''
    x, y = np.mgrid[:vignette.shape[0],:vignette.shape[1]]
    x = x.ravel()[:, None]
    y = y.ravel()[:, None]
    #nobj = len(objs)
    val = vignette.ravel()
    n = val.sum()
    # Starting point: use the segmentation map produced by the
    # deblending algorithm as an estimate of the membership
    # probability.
    T = np.zeros((len(val), nobj))
    converged = False
    for i in range(nobj):
        #T[objs[i].ravel(), i] = 1.
        T[np.flatnonzero(segm == (i+1)), i] = 1.
        f=1
    muold = np.zeros(nobj * 5)
    for i in range(20):
        # M
        Tval = T * val[:, None]
        tau = Tval.sum(axis=0)
        if fit_center or i == 0:
            xc = np.sum(x * Tval, axis=0) / tau
            yc = np.sum(y * Tval, axis=0) / tau
        dx = x - xc
        dy = y - yc
        mxx =  np.sum(dx * dx * Tval, axis=0) / tau
        mxy =  np.sum(dx * dy * Tval, axis=0) / tau
        myy =  np.sum(dy * dy * Tval, axis=0) / tau
        mu = np.hstack([xc, yc, mxx, myy, mxy])
        if plant:
            print(mxx)
        #assert np.isfinite(xc).all()
        #print xc, yc, mxx, mxy, myy
        # E
        det = mxx * myy - mxy * mxy
        if (det <= 0).any():
            #print 'aieq'
            bads = det <= 0
            mxx[bads] = 1
            myy[bads] = 1
            mxy[bads] = 1
            det[bads] = 1
            #return T.reshape((vignette.shape) + (-1,))
        wxx = myy / det
        wyy = mxx / det
        wxy = -mxy / det
        wg = (wxx * dx * dx + wyy * dy * dy + wxy * dx * dy)
        f = tau * np.exp(-0.5 * wg)
        T = f / f.sum(axis=1)[:, None]
        if (np.abs(mu - muold) < 1e-2).all():
            #print 'converged'
            converged = True
            break
        else:
            muold = mu
        print((mxx, myy))
    return T.reshape((vignette.shape) + (-1,)), xc, yc, mxx, myy, mxy, converged

    
