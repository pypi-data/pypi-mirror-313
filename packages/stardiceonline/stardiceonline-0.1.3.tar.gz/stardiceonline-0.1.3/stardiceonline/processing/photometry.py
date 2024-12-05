#!/usr/bin/env python3
import stardiceonline.processing.image
#import stardiceonline.processing.visu
import stardiceonline.processing.catalog

import numpy as np
from numpy.lib.recfunctions import rec_append_fields
import astropy.io.fits as pyfits
import astropy.wcs
import os
import glob

from stardiceonline.processing.detrending import *

def photometry(fname, args):
    fid = pyfits.open(fname, memmap=False) # memmap prevents proper garbage collection

    im = stardiceonline.processing.image.Image(detrend(fid))
        
    im.backsub(im.background_slow, nside=(129,132))
    weight = 1/im.varmap
    
    # Need a cosmic finder and hole filling
    segm, nobj = im.segment(nsig=4, nsig_isophot=2, filled=False)

    # produce the image catalog
    C = stardiceonline.processing.catalog.ImageObjects(segm, radius=args.radius, additionnal_header_keys={})
    levels = np.logspace(np.log10(20*im.sigmaback), np.log10(65000), 24)[1:-1]
    try:
        C.deblended_catalog(im.noback, weight, levels, gain=args.gain, sat=None, threshold=50e-2)
    except Exception as e:
        raise(e)
    # point source clump detection
    C.identify(nsigma=3)

    # aperture photometry
    if len(args.radius):
        C.build_apercat(im.noback, im.varmap, im.segm)


        C.cat['expnum'] = fid[0].header['EXPNUM']
        C.cat['mjd'] = float(fid[0].header['MOUNTMJD'])
        C.cat = rec_append_fields(C.cat, ['exptime', 'mountra', 'mountdec', 'band', 'skylev', 'skyvar', 'target'],
                          [np.full(len(C.cat), float(fid[0].header[hfield])) for hfield in ['cameraexptime', 'MOUNTRA', 'MOUNTDEC']]+[np.full(len(C.cat), fid[0].header['filterwheelfilter'], dtype='S5'), np.full(len(C.cat), im.skylev), np.full(len(C.cat), im.skyvar), np.full(len(C.cat), fid[0].header["mountTARGET"])])
        
    if not args.full:
        C.cat = C.cat[~C.cat['glitch']]
    filename = fname.replace('.fits', '_photometric_cat.npy')
    print(f'New catalog save at {filename} with {len(C.cat)} sources detected in field {fid[0].header["mountTARGET"]} in band {fid[0].header["filterwheelfilter"]}')
    np.save(filename, C.cat)

    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('image', type=str, help='calibrated.fits', nargs='+')
    parser.add_argument('-r', '--radius', metavar='N', type=float, action='store', nargs='+', default=np.logspace(np.log10(3), np.log10(50), 10).round(1),
                        help= "Perform aperture photometry in the given radii")
    parser.add_argument('-f', '--full', action='store_true',
                        help='Do not clean the output from glitches')
    parser.add_argument('-o', '--output_file', dest='output_file', default="./catalog.npy",
                        help= "Output catalog filename")
    #parser.add_argument('-K', '--header-keys', default=['filterwheelfilter', 'cameraexptime', 'MOUNTMJD', 'MOUNTRA', 'MOUNTDEC'], action='append',
    #help= "Gives additionnal header keys to add to the catalog")
    parser.add_argument('-G', '--gain', default=1.2, 
                        help= "Specify the sensor readout gain used in some uncertainty computation")
    
    args = parser.parse_args()

    res = []
    failed_images = []
    for _f, fname in enumerate(args.image):
        print(f'Processing image {fname} ({_f+1}/{len(args.image)})')
        photometry(fname, args)
