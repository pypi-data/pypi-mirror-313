import pickle
import numpy as np
import astropy.wcs

header_keys = ['DATE-OBS', 'EXPTYPE', 'EXPNUM', 'cameratrigdelay', 'filterwheelfilter', 'PSVOLET', 'focuserposition', 'cameratemperature', 'cameraexptime', 'cameragain', 'camerahspeed', 'cameravspeed', 'camerashutter_mode', 'cameraclosing_time', 'cameraopening_time', 'cameragainvalue', 'camerahspeedvalue', 'cameravspeedvalue', 'MOUNTX', 'MOUNTY', 'mountDELTA', 'MOUNTTAU', 'MOUNTHA', 'MOUNTDEC', 'MOUNTMJD', 'MOUNTRA', 'MOUNTALT', 'MOUNTAZ', 'mountSIDEREALTIME', 'mountTARGET', 'raritantemperature', 'raritanhumidity', 'domeAZIMUTH', 'domePOSITION', 'domeADJUST', 'domeMACHINE_STATE', 'DOMERFID', 'DOMEIDX', 'domeTHPOS', 'domeOBSPOS', 'DOMEDIR']

catalog_keys = ['skylev', 'skyvar', 'seeing', 'nstars']
all_keys = header_keys + catalog_keys + ['ra_center', 'dec_center']

def convert(s):
    try:
        val = float(s)
        return val
    except ValueError:
        return s
    except TypeError:
        return float('NaN')
    
def seeing(cat):
    stars = cat['objtype'] == 0
    return np.median(np.sqrt(cat[stars]['a'] * cat[stars]['b']))

catalog_functions = {
    'seeing': seeing,
    'skylev': lambda cat: cat['skylev'][0],
    'skyvar': lambda cat: cat['skyvar'][0],
    'nstars': lambda cat: np.sum(cat['objtype'] == 0),
    }


def field_center(wcs):
    if wcs is None:
        return [float('NaN'), float('NaN')]
    else:
        ra, dec = wcs.all_pix2world(np.array([[512], [512]]).T, 0).T
        return [ra[0], dec[0]]

def read_header_file(filename):
    res = []
    with open(filename, 'rb') as fid:
        while True:
            try:
                toto = pickle.load(fid)
                res.append(tuple(toto.values()))
            except EOFError:
                break
    return np.rec.fromrecords(res, names = list(toto.keys()))

def read_header(h, keys=header_keys):
    if keys is None:
        keys = list(h.keys())
    return [convert(h[n]) if n in h else float('NaN') for n in keys]

def read_all(h, cat, wcs):
    return read_header(h) + [catalog_functions[k](cat) if cat is not None else float('NaN') for k in catalog_keys] + field_center(wcs)

def read_headers(filenames):
    import astropy.io.fits as pyfits
    res = []
    for _f, f in enumerate(filenames, 1):
        print(f'processing file {_f}/{len(filenames)}', end='\r')
        h = pyfits.getheader(f)
        res.append(read_header(h, keys=header_keys))
    return np.rec.fromrecords(res, names=header_keys)

def summary(filenames):
    import astropy.io.fits as pyfits
    res = []
    for _f, f in enumerate(filenames, 1):
        print(f'processing file {_f}/{len(filenames)}', end='\r')
        h = pyfits.getheader(f)
        try:
            cat = np.load(f.replace('.fits', '_photometric_cat.npy'))
            if len(cat) == 0:
                cat = None
        except IOError:
            cat = None
        try:
            wcs = astropy.wcs.WCS(f.replace('.fits', '_photometric_cat.wcs'))
        except IOError:
            wcs = None
        res.append(read_all(h, cat, wcs))
    return np.rec.fromrecords(res, names=all_keys)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert header file to numpy array, or image headers to numpy array')
    parser.add_argument('filename', type=str, help='Pickle of headers or image files', nargs='+')
    parser.add_argument('-o', '--output-file', default="./headers.npy",
                        help= "Output numpy format to header file")
    
    args = parser.parse_args()
    if args.filename[0].endswith('.pkl'):
        res = read_header_file(args.filename[0])
    else:
        res = summary(args.filename)
        res.sort(order='EXPNUM')
    np.save(args.output_file, res)
