import re

re_expnum = re.compile('IMG_(\d*).fits')
re_catalog = re.compile('IMG_(\d*)_photometric_cat.npy')
re_astrom_catalog = re.compile('IMG_(\d*)_photometric_cat_astrom.npy')

def im2expnum(s):
    return int(re_expnum.findall(s)[0])

def cat2expnum(s):
    return int(re_catalog.findall(s)[0])

def astromcat2expnum(s):
    return int(re_astrom_catalog.findall(s)[0])

def expnum2filename(directory, expnum, kind='images'):
    end = {'images': '.fits',
           'catalogs': '_photometric_cat.npy',
           'astrom_catalogs': '_photometric_cat_astrom.npy',
           'wcs': '_photometric_cat.wcs'}[kind]
    return f'{directory}/IMG_{expnum:07d}{end}'
