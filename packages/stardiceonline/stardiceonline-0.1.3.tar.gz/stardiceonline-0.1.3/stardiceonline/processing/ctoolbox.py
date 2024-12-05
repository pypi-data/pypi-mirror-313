"""Simple wrapper around the c function inpaint """

import numpy as np
import os
import ctypes
import stardiceonline
import glob

_lib = np.ctypeslib.load_library('ctools', stardiceonline.__path__[0])

_inpaint = _lib.inpaint
_inpaint.restype = None
_inpaint.argtypes = [
    np.ctypeslib.ndpointer(float, ndim=2, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ndpointer('i4',flags='aligned, contiguous'),
    ctypes.POINTER(np.ctypeslib.c_intp),
    np.ctypeslib.c_intp,
    np.ctypeslib.ctypes.c_double]

_segment = _lib.segment
_segment.restype = ctypes.c_int
_segment.argtypes = [
    np.ctypeslib.ndpointer(float, ndim=2, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ndpointer('i4', ndim=2, flags='aligned, contiguous, writeable'),
    ctypes.POINTER(np.ctypeslib.c_intp),
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double]

_minimap = _lib.minimap
_minimap.restype = ctypes.c_int
_minimap.argtypes = [
    np.ctypeslib.ndpointer(float, ndim=2, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ndpointer('i4', ndim=2, flags='aligned, contiguous, writeable'),
    ctypes.POINTER(np.ctypeslib.c_intp),
    ctypes.c_int,
    ctypes.c_int,
    np.ctypeslib.ndpointer(float, ndim=2, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ndpointer(float, ndim=2, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ndpointer('i4', ndim=2, flags='aligned, contiguous, writeable')
   ]

_neig_nr_full = _lib.neig_nr_full
_neig_nr_full.restype = ctypes.c_int
_neig_nr_full.argtypes = [
    np.ctypeslib.ndpointer(float, ndim=2, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ndpointer('i4', ndim=2, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ndpointer('i4', ndim=1, flags='aligned, contiguous, writeable'),
    ctypes.POINTER(np.ctypeslib.c_intp),
    np.ctypeslib.ctypes.c_int,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_int,
    ctypes.POINTER(np.ctypeslib.ctypes.c_double)]

_deblend_tree = _lib.deblend_tree
_deblend_tree.restype = ctypes.c_int
_deblend_tree.argtypes = [
    np.ctypeslib.ndpointer(float, ndim=2, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ndpointer('i4', ndim=2, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ndpointer('i4', ndim=1, flags='aligned, contiguous, writeable'),
    ctypes.POINTER(np.ctypeslib.c_intp),
    np.ctypeslib.ctypes.c_int,
    np.ctypeslib.ndpointer(float, ndim=1, flags='aligned, contiguous'),
    np.ctypeslib.ctypes.c_int,
    np.ctypeslib.ctypes.c_int,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_int,
    np.ctypeslib.ndpointer('i4', ndim=2, flags='aligned, contiguous, writeable')]

_gaussian2d = _lib.gaussian2d
_gaussian2d.restype = None
_gaussian2d.argtypes = [
    np.ctypeslib.ndpointer(float, ndim=2, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ctypes.c_int,
    np.ctypeslib.ctypes.c_int,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double]

_gaussian2d_der = _lib.gaussian2d_der
_gaussian2d_der.restype = None
_gaussian2d_der.argtypes = [
    np.ctypeslib.ndpointer(float, ndim=3, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ctypes.c_int,
    np.ctypeslib.ctypes.c_int,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double]

_gaussian_weighted_moments = _lib.gaussian_weighted_moments
_gaussian_weighted_moments.restype = ctypes.c_int
_gaussian_weighted_moments.argtypes = [
    np.ctypeslib.ndpointer(float, ndim=2, flags='aligned, contiguous, writeable'),
    #np.ctypeslib.ndpointer('i4', ndim=2, flags='aligned, contiguous, writeable'),
    ctypes.POINTER(np.ctypeslib.c_intp),
    ctypes.POINTER(np.ctypeslib.ctypes.c_double),
    ctypes.POINTER(np.ctypeslib.ctypes.c_double),
    ctypes.POINTER(np.ctypeslib.ctypes.c_double),
    ctypes.POINTER(np.ctypeslib.ctypes.c_double),
    ctypes.POINTER(np.ctypeslib.ctypes.c_double)]

class aperture(ctypes.Structure):
    _fields_ = [("flux", ctypes.c_double),
                ("variance", ctypes.c_double),
                ("other", ctypes.c_double),
                ("bad", ctypes.c_double)]

_circular_aperture = _lib.circular_aperture
_circular_aperture.restype = aperture
_circular_aperture.argtypes = [
    np.ctypeslib.ndpointer(float, ndim=2, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ndpointer(float, ndim=2, flags='aligned, contiguous, writeable'),
    np.ctypeslib.ndpointer('i4', ndim=2, flags='aligned, contiguous, writeable'),
    ctypes.POINTER(np.ctypeslib.c_intp),
    ctypes.c_int,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double,
    np.ctypeslib.ctypes.c_double]


def inpaint(data, mask):
    """ Fill holes in image by diffusing the border in the holes
    data: a n x m image.
    mask: the list of the nhole pixels to inpaint.
    """
    requires = ['CONTIGUOUS', 'ALIGNED']
    data = np.asanyarray(data)
    data = np.require(data, float, requires)
    mask = np.asanyarray(mask)
    mask = np.require(mask, 'i4', requires)
    _inpaint(data, mask, data.ctypes.shape, mask.size, 1)
    return data


def segment(data, threshold=None, isophot=None):
    """ Simple segmentation algorithm.
    data: a n x m image.
    segmap: the resulting segmentation map.
    """
    requires = ['CONTIGUOUS', 'ALIGNED']
    data = np.asanyarray(data)
    data = np.require(data, float, requires)
    segmap = np.zeros(data.shape, dtype='i4')
    segmap = np.require(segmap, 'i4', requires)
    if threshold is None:
        sigma = data.std()
        threshold = 10 * sigma
        if isophot is None:
            isophot = 3 * sigma
    elif isophot is None:
        isophot = threshold * 0.3
    nobj = _segment(data, segmap, data.ctypes.shape, threshold, isophot)
    return segmap, nobj

def deblend(data, segmap, cut, source_id, levels, fluxmin, new_id=0):
    """ Simple deblending algorithm.
    data: a n x m image.
    """
    vignette = np.ascontiguousarray(data[cut])
    segm = np.ascontiguousarray(segmap[cut])
    pixlist = np.flatnonzero(segm == source_id).astype('i4')
    
    levelmap = np.zeros(vignette.shape, dtype='i4')
    segm = np.zeros(vignette.shape, dtype='i4')
    
    nobj = _deblend_tree(vignette, levelmap, pixlist, vignette.ctypes.shape, len(pixlist), levels, 1, len(levels), fluxmin, new_id, segm)
    return segm, nobj

def gaussian2d_moments(s, grid):
    """ Warning: never tested
    Same as gaussian2d but with different parameters 
    s: must provide x, y, mxx, myy, mxy, fiso

    grid: index of the corners.
    """
    det = s['mxx'] * s['myy'] - s['mxy'] * s['mxy']
    A = s['fiso'] / np.sqrt(det)
    params = s['x'], s['y'], 0.5 * s['myy'] / det, 0.5 * s['mxx'] / det, -0.5 * s['mxy'] / det, A, 0
    return gaussian2d(params, grid)

def gaussian2d(params, grid):
    """ Draw a 2 dimensionnal gaussian.
    params: gaussian parameters.
    x0, y0, alpha, beta, gamma, A, b
    grid: index of the corners.
    """
    xmin, xmax, ymin, ymax, jk = grid
    x0, y0, alpha, beta, gamma, A, b = params
    Nx = xmax - xmin
    Ny = ymax - ymin
    x0 -= xmin
    y0 -= ymin
    patch = np.zeros((Nx, Ny), dtype=float)
    _gaussian2d(patch, Nx, Ny, x0, y0, alpha, beta, gamma, A, b)
    return patch

def gaussian2d_der(params, grid):
    """ Compute derivatives of a 2 dimensionnal gaussian.

    params: gaussian parameters.
    x0, y0, alpha, beta, gamma, A
    grid: index of the corners.
    """
    xmin, xmax, ymin, ymax, jk = grid
    x0, y0, alpha, beta, gamma, A, b = params
    Nx = xmax - xmin
    Ny = ymax - ymin
    x0 -= xmin
    y0 -= ymin
    patch = np.zeros((Nx, Ny, 7), dtype=float)
    _gaussian2d_der(patch, Nx, Ny, x0, y0, alpha, beta, gamma, A, b)
    return patch

def gaussian_weighted_moments(data, s):
    _xc = np.ctypeslib.ctypes.c_double(s['x'])
    _yc = np.ctypeslib.ctypes.c_double(s['y'])
    _mxxold = np.ctypeslib.ctypes.c_double(s['mxx'])
    _myyold = np.ctypeslib.ctypes.c_double(s['myy'])
    _mxyold = np.ctypeslib.ctypes.c_double(s['mxy'])
    byref = np.ctypeslib.ctypes.byref
    flag = _gaussian_weighted_moments(data, data.ctypes.shape, byref(_xc), byref(_yc), byref(_mxxold), byref(_myyold), byref(_mxyold))
    s['gwx'] = _xc.value
    s['gwy'] = _yc.value
    s['gwmxx'] = _mxxold.value
    s['gwmyy'] = _myyold.value
    s['gwmxy'] = _mxyold.value
    return s

def circular_aperture(flux, variance, segmentation, id, x, y, radius):
    """ Aperture photemetry
    flux: a n x m image.

    """
    return _circular_aperture(flux, variance, segmentation, flux.ctypes.shape, id, x, y, radius)

def minimap(data, segm, nside, deads=None):
    try:
        M = data.shape[0] // nside[0]
        N = data.shape[1] // nside[1]
    except:
        nside = [nside, nside]
        M = data.shape[0] // nside[0]
        N = data.shape[1] // nside[1]
    mean, std = np.zeros((M,N)), np.zeros((M,N))
    num = np.zeros((M,N), dtype='i4')
    mask = (segm != 0).astype('i4')
    if deads is not None:
        mask[deads] = 1
    _minimap(data, mask, data.ctypes.shape, nside[0], nside[1], mean, std, num)
    std /= 3
    mean[np.isnan(mean)] = np.nanmean(mean)
    std[np.isnan(std)] = np.nanmean(std)
    return mean, np.nanmean(std), std
