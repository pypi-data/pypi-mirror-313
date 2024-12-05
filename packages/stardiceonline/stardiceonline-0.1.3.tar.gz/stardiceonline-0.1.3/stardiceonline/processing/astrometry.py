#!/usr/bin/env python
import numpy as np
import subprocess
import astropy.io.fits as pyfits
import astropy.wcs as wcs
from glob import glob

def write_xycat(cat, filename, w=1024, h=1024):
    results = np.rec.fromarrays([cat['gwx'], cat['gwy'], cat['apfl_5.60']], names=['X', 'Y', 'FLUX'])
    results = pyfits.BinTableHDU(results)
    results.header['EXTNAME'] = 'SOURCES'#           / name of this binary table extension            
    results.header['SRCEXT']  = 1 # / Extension number in src image                  
    results.header['IMAGEW']  = w # / Input image width                              
    results.header['IMAGEH']  = h #/ Input image height                             
    results.header['ESTSIGMA'] = 7.071068 #/ Estimated source image variance                
    results.header['DPSF'] = 1. #/ image2xy Assumed gaussian psf width            
    results.header['PLIM'] = 8. #/ image2xy Significance to keep                  
    results.header['DLIM'] = 1. #/ image2xy Closest two peaks can be              
    results.header['SADDLE'] = 5. #/ image2xy Saddle difference (in sig)            
    results.header['MAXPER'] = 1000 #/ image2xy Max num of peaks per object           
    results.header['MAXPEAKS'] = 10000 #/ image2xy Max num of peaks total                
    results.header['MAXSIZE'] = 2000 #/ image2xy Max size for extended objects         
    results.header['HALFBOX'] = 100 #/ image2xy Half-size for sliding sky window      
    results.header['REMLINEN'] = 0 #/ Number of sources removed by "removelines.py"  
    if filename:
        results.writeto(filename, overwrite=True)
    return results

def astrometry(cat, w=1024, h=1024, radec=[], silent=True, basefilename=''):
    tmpname = f'{basefilename}_astrom.fits'
    write_xycat(cat, tmpname, w, h)
        
    astrom_com = ['solve-field','-L', '30', '-H', '34', '-u', 'arcminwidth', tmpname, '--overwrite', '-p']
    if radec:
        astrom_com += ['--ra', str(radec[0]), '--dec', str(radec[1]), '--radius', '5']
    if silent:
        stdout = subprocess.DEVNULL
    else:
        print((' '.join(astrom_com)))
        stdout = subprocess.STDOUT
    try:
        subprocess.check_call(astrom_com, stdout=stdout, stderr=stdout)
        subprocess.check_call(['mv', f'{basefilename}_astrom.wcs', f'{basefilename}.wcs'])
    finally:
        subprocess.check_call(['rm'] + glob(f'{basefilename}_astrom*') , stdout=stdout)
    w = wcs.WCS(f'{basefilename}.wcs')
    if w.wcs.ctype[0]:
        return w
    else:
        raise ValueError(f'Expnum {cat["expnum"][0]} for Field {cat["target"][0]} in band {cat["band"][0]} did not solve')

def radec_catalog(w, cat):
    ra, dec = (w.all_pix2world(np.array([cat['gwx'], cat['gwy']]).T, 0)).T
    return ra, dec

def main(filename, args):
    cat = np.load(filename)
    goods = ~cat['unconverged'] & ~cat['windowed']# & (cat['expnum'] == exp)# & (-2.5 * np.log10(cat['apfl_5.60']) <-11)
    c = cat[goods]
    c_ = c[np.argsort(-2.5*np.log10(c['apfl_5.60']))][:30]
    ra, dec = c_['mountra'], c_['mountdec']
    
    if args.brut_force:
        w = astrometry(c_, 1100, 1100, basefilename=filename.replace('.npy', ''), silent=not args.verbose)
    else:
        w = astrometry(c_, 1100, 1100, radec=(np.mean(ra), np.mean(dec)), basefilename=filename.replace('.npy', ''), silent=not args.verbose)
        
    ra, dec = radec_catalog(w, c)
    c['ra'] = ra
    c['dec'] = dec

    outfilename = filename.replace('.npy', '_astrom.npy')
    np.save(outfilename, c)
    print(f'New astrometric catalog {outfilename} for field {cat["target"][0]} in band {cat["band"][0]}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('Find astrometric solutions for the provided catalogs using astrometry.net solve-field.')
    parser.add_argument('input_catalogs', type=str, help='photometry.npy', nargs='+')
    parser.add_argument('-v', '--verbose', action='store_true', help='Display the messages from solve-field')
    parser.add_argument('-b', '--brut-force', action='store_true', help='Do not use the mount indication as a guess, try to solve all-sky instead')
    
    args = parser.parse_args()

    for filename in args.input_catalogs:
        print(f'Processing {filename}')
        main(filename, args)
