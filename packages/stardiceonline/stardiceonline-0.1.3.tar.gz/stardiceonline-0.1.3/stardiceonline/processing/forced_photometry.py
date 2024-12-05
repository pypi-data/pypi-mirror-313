#!/usr/bin/env python3
import astropy.io.fits as pyfits
import astropy.wcs
import glob
import numpy as np
import os
import stardiceonline.processing.image
import stardiceonline.processing.catalog
from stardiceonline.processing.detrending import detrend_full_overscan
from stardiceonline.tools import match

import reference_catalog
import astrometric_model

def forced_photometry(fname, args):
    basename = fname.replace('_photometric_cat_astrom.npy','')

    with pyfits.open(f'{basename}.fits', memmap=False) as fid:# memmap prevents proper garbage collection
        header = fid[0].header
        im = stardiceonline.processing.image.Image(detrend_full_overscan(fid))

    image_cat = np.load(f'{basename}_photometric_cat_astrom.npy')
    wcs = astropy.wcs.WCS(f'{basename}_photometric_cat.wcs')
    field = header['MOUNTTARGET']

    # Match to the gaia catalog
    reference_cat = reference_catalog.get_gaia_catalog_from_label(field, radius_value=30., row_limit=50000, outputdir="./")
    matched_catalog, matched_catalog_ref = reference_catalog.match_image_and_refcat(image_cat, reference_cat, wcs)

    # Fit a sky->pixel transformation for the image
    transfo = astrometric_model.Transfo()
    params = transfo.starting_point(wcs)
    bestfit, goods = transfo.fit(matched_catalog, matched_catalog_ref, params)

    #save the result
    np.save(f'{basename}_transform.npy', bestfit)
    
    # Compute the position of Gaia objects
    x, y = transfo(bestfit, reference_cat['ra'], reference_cat['dec'])
    
    # Keep only objects in the footprint
    x, y = np.array(x), np.array(y)
    inframe = (x < im.data.shape[1]) & (y <  im.data.shape[0]) & (x > 0) & (y > 0)

    # Forms the catalog
    reference_cat.add_columns([x, y], names=['x', 'y'])
    keys = ['alt', 'az', 'mjd', 'exptime', 'filter', 'pressure', 'temperature', 'humidity', 'focuspos', 'mounttemp']
    keynames = ['MOUNTALT', 'MOUNTAZ', 'MOUNTMJD', 'cameraexptime', 'filterwheelfilter', 'weatherAir pressure [hPa]', 'weatherAir temperature [C]', 'weatherRelative humidity [%]', 'focuserposition', 'raritantemperature']
    reference_cat.add_columns([np.full(len(x), header[k]) for k in keynames], names=keys)

    #Forced photometry at computed position
    forced_cat = stardiceonline.processing.catalog.ImageObjects(None, radius=args.radius, cat=reference_cat[inframe], additionnal_header_keys={})
    forced_cat.build_apercat(im.data, np.zeros_like(im.data), np.zeros(im.data.shape, dtype='int32'), prefix='', index='SOURCE_ID')
    
    np.save(f'{basename}_forcedphot_cat_astrom.npy', forced_cat.cat)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('catalog', type=str, help='calibrated.npy', nargs='+')
    parser.add_argument('-s', '--show', action='store_true',
                        help= "Display control plots")
    parser.add_argument('-r', '--radius', metavar='N', type=float, action='store', nargs='+', default=np.logspace(np.log10(3), np.log10(50), 10).round(1),
                        help= "Perform aperture photometry in the given radii")
    
    args = parser.parse_args()

    res = []
    failed_images = []
    for _f, fname in enumerate(args.catalog):
        basename = fname.replace('_photometric_cat_astrom.npy','')
        forced_photometry(fname, args)
        print(f'Processing image {basename} ({_f+1}/{len(args.catalog)})')
    
        if args.show:
            import matplotlib.pyplot as plt
            index = match.match(forced_cat.cat, image_cat, xy=True, project=False, arcsecrad=20*3600)
            c1 = forced_cat.cat[index[index != -1]]
            c2 = image_cat[index != -1]
            plt.figure('photometry comparison')
            plt.plot(c1['apfl_7.70'], c2['apfl_7.70'] - c1['apfl_7.70'], 'o')
            plt.xlabel('apfl_7.70 (forced)')
            plt.ylabel('free - forced')
            plt.figure('astrometric residuals')
            plt.plot(c1['x'] - c2['gwx'], c1['y'] - c2['gwy'], '+')
            plt.xlabel('x_gaia - gwx [pixels]')
            plt.ylabel('y_gaia - gwy [pixels]')
            plt.show()

        # TODO
        # gérer la contamination des ouvertures
        # carte de fond et variance
        # voir si les mouvements propre améliore l'astrometrie
        # itérer sur le match astrometrique
        # astrometric quality in plots
