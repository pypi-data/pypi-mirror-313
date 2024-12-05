import pipelet3
import stardiceonline.processing.photometry
import stardiceonline.processing.astrometry
import stardiceonline.processing.led_photometry
import stardiceonline.processing.sphere_photometry
from stardiceonline.archive.archive import local_archive
from stardiceonline.tools.config import config
from pathlib import Path
import os
import numpy as np
import argparse
import re
import astropy.io.fits as pyfits
import ast
import warnings
warnings.filterwarnings("ignore")

default_photometry_params = argparse.Namespace()
default_photometry_params.radius = np.logspace(np.log10(3), np.log10(50), 10).round(1)
default_photometry_params.full = False # discard glitches from the catalog
default_photometry_params.gain = 1.2

default_astrometry_params = argparse.Namespace()
default_astrometry_params.verbose = False
default_astrometry_params.brut_force = False

def isflat(result):
    return result[2] == 'FLAT'

def isstar(result):
    return result[2] not in ['FLAT', 'TEST', 'LEDT152', 'SPHERE', 'EARTH']

def isled(result):
    return result[2] == 'LEDT152'

def issphere(result):
    return result[2] == 'SPHERE'

def sameband(result):
    return result[3]

def extract_image_number(path):
    pattern = r'IMG_(\d+)\.fits'
    match = re.search(pattern, path)
    if match:
        return int(match.group(1))  # Return the matched digits
    else:
        return None  # Return None if no match is found

def extract_image_header(path):
    header = pyfits.getheader(path)
    target = header.get('mountTARGET', None)
    band = header.get('filterwheelfilter', None)
    return target, band

#def list_directory(night):
#    path = Path(config['archive.local']) / night
#    imlist = list(path.glob('IMG*.fits'))
#    imlist.sort()
#    result = [(night, extract_image_number(im.name))+extract_image_header(im.as_posix()) for im in imlist]
#    return result

def list_directory(night):
    path = Path(config['archive.local']) / night
    imlist = list(path.glob('IMG*.fits'))
    imlist.sort()
    return [im.as_posix() for im in imlist]

def photometry(args):
    night, expnum, target, band = args
    fname = Path(config['archive.local']) / night / f'IMG_{expnum:07d}.fits'
    stardiceonline.processing.photometry.photometry(fname.as_posix(), default_photometry_params)
    return [(night, expnum, target, band)]

def astrometry(args):
    night, expnum, target, band = args
    fname = Path(config['archive.local']) / night / f'IMG_{expnum:07d}_photometric_cat.npy'
    stardiceonline.processing.astrometry.main(fname.as_posix(), default_astrometry_params)
    return [(night, expnum, target, band)]

def masterflat(args):
    pass
    #print(args)

    
def find_last_dark(night, fname):
    path = Path(config['archive.local']) / night
    imlist = list(path.glob('IMG*.fits'))
    imlist.sort()
    index = imlist.index(fname)
    #print(index)
    try:
        for im in imlist[index::-1]:
            header = pyfits.getheader(im.as_posix())
            led, vled = ast.literal_eval(header['star152led'])
            if vled == 0:
                return im
    except:
        return None
    return None

def find_last_dark_sphere(night, fname):
    path = Path(config['archive.local']) / night
    imlist = list(path.glob('IMG*.fits'))
    imlist.sort()
    index = imlist.index(fname)
    try:
        for im in imlist[index::-1]:
            header = pyfits.getheader(im.as_posix())
            sphereled = header['sphereled']
            if sphereled == 0:
                return im
    except:
        return None
    return None

def led_photometry(args):
    night, expnum, target, band = args
    fname = Path(config['archive.local']) / night / f'IMG_{expnum:07d}.fits'
    header = pyfits.getheader(fname.as_posix())
    led, vled = ast.literal_eval(header['star152led'])
    if vled == 0:
        return [(night, expnum, target, band, led, 'DARK')]
    else:
        dark = find_last_dark(night, fname)
        if dark is None:
            raise ValueError(f'Could not find preceding dark for image {fname})')
        else:
            stardiceonline.processing.led_photometry.main(fname.as_posix(), dark.as_posix(), default_photometry_params)
            return [(night, expnum, target, band, led, vled)]

def sphere_photometry(args):
    night, expnum, target, band = args
    fname = Path(config['archive.local']) / night / f'IMG_{expnum:07d}.fits'
    header = pyfits.getheader(fname.as_posix())
    led = int(header['sphereled'])
    if led == 0:
        return [(night, expnum, target, band, led, 'DARK')]
    else:
        dark = find_last_dark_sphere(night, fname)
        if dark is None:
            raise ValueError(f'Could not find preceding dark for image {fname})')
        else:
            stardiceonline.processing.sphere_photometry.main(fname.as_posix(), dark.as_posix(), default_photometry_params)
            return [(night, expnum, target, band, led)]


def forced_photometry(args):
    night, expnum, target, band = args
    fname = Path(config['archive.local']) / night / f'IMG_{expnum:07d}_photometric_cat_astrom.npy'
    stardiceonline.processing.forced_photometry.forced_photometry(fname.as_posix(), default_photometry_params)
    return [(night, expnum, target, band)]
    
def new_image(path):
    night = os.path.basename(os.path.dirname(path))
    expnum = extract_image_number(path)
    if expnum is None:
        return []
    else:
        return [(night, expnum) + extract_image_header(path)]

def match_expnum(tid, argument, value):
    return argument[1] == value


