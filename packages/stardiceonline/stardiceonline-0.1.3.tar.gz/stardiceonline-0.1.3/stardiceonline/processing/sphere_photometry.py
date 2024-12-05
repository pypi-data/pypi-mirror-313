#from led_background import BackgroundModel
#from image_summary import Summary
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
import ast

from stardiceonline.processing.detrending import *

def monitoring_stats(im):
    header = pyfits.getheader(im)
    t = pyfits.getdata(im,'KSPHERE')
    return {
        'led': int(header['sphereled']),
        'sphere_mean': t['curr'].mean(),
        'sphere_std': t['curr'].std(),
        'sphere_n': len(t),
        'exptime': float(header['cameraexptime']),
        'mountra': float(header['MOUNTRA']),
        'mountdec': float(header['MOUNTDEC']),
        'band': header['filterwheelfilter'],
        'skylev': 0.,
        'skyvar': 0.,
    }, header
        

def main(fname, background, args):
    back = detrend_full_overscan(pyfits.open(background))
    data = detrend_full_overscan(pyfits.open(fname))
    radius = args.radius

    metadata, header = monitoring_stats(fname)
    im = stardiceonline.processing.image.Image(data-back)
    im.backsub(im.background_slow, nside=(129,132))
    segm, nobj = im.segment(nsig=4, nsig_isophot=2, filled=False)
    weight = 1/im.varmap
    C = stardiceonline.processing.catalog.ImageObjects(segm, radius=radius, additionnal_header_keys=metadata)
    levels = np.logspace(np.log10(20*im.sigmaback), np.log10(65000), 24)[1:-1]
    C.deblended_catalog(im.noback, weight, levels, gain=args.gain, sat=None, threshold=50e-2)
    C.build_apercat(im.noback, im.varmap, im.segm)
    
    C.cat['expnum'] = header['EXPNUM']
    C.cat['mjd'] = float(header['MOUNTMJD'])
    C.cat['skylev'] = im.skylev
    C.cat['skyvar'] = im.skyvar
    source = np.argmax(C.cat['fluxmax'])
    if not args.full:
        cat = np.atleast_1d(C.cat[source])
    else:
        cat = C.cat
    filename = fname.replace('.fits', '_photometric_cat.npy')
    print(f'New led catalog save at {filename} for led {cat["led"][0]} in band {cat["band"][0]}')
    np.save(filename, cat)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('image', type=str, help='calibrated.fits', nargs=2)
    parser.add_argument('-r', '--radius', metavar='N', type=float, action='store', nargs='+', default=np.logspace(np.log10(3), np.log10(50), 10).round(1),
                        help= "Perform aperture photometry in the given radii")
    parser.add_argument('-f', '--full', action='store_true',
                        help='Do not clean the output from glitches')
    parser.add_argument('-G', '--gain', default=1.2, 
                        help= "Specify the sensor readout gain used in some uncertainty computation")
    
    args = parser.parse_args()

    background, fname = args.image
    main(background, fname, args)
    #B = BackgroundModel.load('empty_background.npz')
    #s = Summary('/data/stardiceot1/2024_07_10/')
#    l = glob('/data/stardiceot1/2024_07_10/*.fits')
#    l.sort()
#    l = np.array(l[6:])
#    
#    headers = [pyfits.getheader(i) for i in l]
#    band = np.array([header['filterwheelfilter'] for header in headers])
#    goods = band == 'EMPTY'
#    #headers[goods]
#    
#    leds = np.array([eval(header['star152led']) for header in headers])
#    leds, vleds = leds[goods].T
#
#    def cond(im):
#        t = pyfits.getdata(im,1)
#        return len(t), t['V_R'].mean(), t['V_LED'].mean(), t['T_ADC'].mean(), t['T_DS1631'].mean(), t['V_R'].std()
#
#    meta = [cond(i) for i in l[goods]]
#    meta = np.rec.fromrecords(meta, names=['n', 'V_R', 'V_LED', 'T_ADC', 'T_DS1631', 'sigma_V_R'])
#    images = np.array([detrend_full_overscan(pyfits.open(i)) for i in l[goods]])
#    darks = vleds == 0
#    radius = np.logspace(np.log10(3), np.log10(50), 10).round(1)
#    result = []
#    for led in range(14):
#        D = np.mean(images[darks & (leds == led)], axis=0)
#        for I in images[~darks & (leds == led)]:g
#            im = imageproc.image.Image(I-D)
#            im.backsub(im.background_slow, nside=(129,132))
#            segm, nobj = im.segment(nsig=4, nsig_isophot=2, filled=False)
#            weight = 1/im.varmap
#            C = imageproc.catalog.ImageObjects(segm, radius=radius, additionnal_header_keys={'led':led})
#            levels = np.logspace(np.log10(20*im.sigmaback), np.log10(65000), 24)[1:-1]
#            try:
#                C.deblended_catalog(im.data, weight, levels, gain=args.gain, sat=None, threshold=50e-2)
#            except Exception as e:
#                print(e)
#                continue
#            C.build_apercat(im.data, im.varmap, im.segm)
#            source = np.argmax(C.cat['fluxmax'])
#            result.append(C.cat[source])
#    result = np.hstack(result)
#    
#    plt.plot(result['led'], result['apfl_7.70'], '+')
#    plt.axhline(100000, ls='--', color='k')
#    plt.xlabel('LED #')
#    plt.ylabel('Flux')
#    plt.tight_layout()
#
#    def join(*args, **keys):
#        return np.rec.fromarrays([nt[k] for nt in args for k in nt.dtype.names]+[keys[k] for k in keys], names=[k for nt in args for k in nt.dtype.names] + [k for k in keys])
#
#    fig = plt.figure('Monitoring')
#    ax1, ax2, ax3 = fig.subplots(3,1, sharex=True)
#    ax1.plot(result['led'][~dark], result['vled'][~dark], 'k.')
#    ax1.set_ylabel('$V_nom$ [V]')
#    ax2.plot(result['led'][~dark], result['V_R'][~dark]/2**24*2.5, 'k.')
#    ax2.set_ylabel(r'$V_R$ [V]')
#    vr = np.array([result['V_R'][~dark & (result['led'] == led)].mean() for led in range(14)])
#    vrs = np.array([result['V_R'][~dark & (result['led'] == led)].std() for led in range(14)])
#    ax3.plot(vrs/vr * 100, 'k.')
#    ax3.set_ylabel(r'$\sigma(V_R)/V_R$ [%]')
#    ax3.set_xlabel('LED #')
#    ax2.axhline(0.5, ls=':', color='k')
#    ax3.axhline(1e-1, ls=':', color='k')
#    ax3.set_yscale('log')
#    #ax2.set_yscale('log')
#    plt.tight_layout()
#    plt.show()
