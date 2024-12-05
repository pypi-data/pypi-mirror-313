import healpy
import numpy as np
from stardiceonline.tools.metadatamanager import MetaDataManager
from stardiceonline.tools.config import config
import tqdm
import gzip
import os

manager = MetaDataManager()

md5sum = manager.get_data('gaia/_MD5SUM.txt', "https://cdn.gea.esac.esa.int/Gaia/gdr3/Spectroscopy/xp_continuous_mean_spectrum/_MD5SUM.txt")

def parse_md5sum(fn):
    """Use md5sum file to get the full list of files.

    :param str fn: md5sum file from https://cdn.gea.esac.esa.int/Gaia/gdr3/Spectroscopy/xp_continuous_mean_spectrum
    :return int list bins: first pixels
    :return str list ranges: list of pixel range used in filenames
    """
    with open(fn) as fid:
        lines = fid.readlines()
    ranges = [
        l.split("XpContinuousMeanSpectrum_")[-1].split(".csv.gz")[0] for l in lines
    ]
    bins = [int(b.split("-")[0]) for b in ranges]
    return bins, ranges


def get_pixlist(ras, decs, level=8):
    """Return list of healpix pixel matching ra, dec coordinate of a
    given catalog.

    :param arrays:  ras, decs coordinates of the 4 corners of the field
    :param int level: Gaia spectra are registered with healpix level 8 (nside=256)
    :return list pixlist: list of healpix pixels (in [0, 786431])
    """
    pixlist = []
    nside = healpy.order2nside(level)
    pixlist = list(np.unique([healpy.ang2pix(nside, ra, dec, lonlat=True, nest=True) for ra, dec in zip(ras, decs)]))
    return pixlist

def get_pix_range(ra, dec):
    """Return a list of pixel ranges matching indexing of gaia 36XX files.
    :param list ra:  ra
    :param list dec: dec
    :return str list ranges: list of pixel range covered by sky corrdinates
    """
    pixlist = get_pixlist(ra, dec)

    # todo span range
    bins, ranges = parse_md5sum(md5sum)
    range_index = np.digitize(pixlist, bins) - 1
    range_index = np.unique(range_index)
    return [ranges[i] for i in range_index]

def retrieve_gaia_data(pixel_range):
    """Load Gaia spectra.

    :param str pixel_range: pixel range
    :param str gaia_dir: location of calibrated spectra
    :return dataframe calibrated_spectra: source_id, flux, flux_error
    :return array sampling: wavelength in angstrom
    """
    fname = os.path.join(config['archive.local'], 'gaia', f'XpSampledMeanSpectrum_{pixel_range}.npz')
    if os.path.exists(fname):
        res = np.load(fname)
        return res['meta'], res['flux']
    else:
        rawname = f'XpSampledMeanSpectrum_{pixel_range}.csv.gz'
        sampled = manager.get_data(f'gaia/{rawname}', f"https://cdn.gea.esac.esa.int/Gaia/gdr3/Spectroscopy/xp_sampled_mean_spectrum/{rawname}")
        meta, flux = read_gaia(sampled)
        np.savez(fname, meta=meta, flux=flux)
        return meta, flux

def read_gaia(fname):
    fid = gzip.GzipFile(fname)
    meta = []
    flux = []
    for line in fid:
        if line[0] == 35 or line[0] == 115:
            continue
        l = line.replace(b'[', b'').replace(b']', b'').replace(b'"', b'').split(b',')
        meta.append((int(l[0]), float(l[2]), float(l[3])))
        flux.append([float(e) for e in l[4:347]])
    return np.rec.fromrecords(meta, names=['source_id', 'ra', 'dec']), np.array(flux, dtype=np.float32)

if __name__ == '__main__':
    # test by querying the location of G191B2B
    pranges = get_pix_range([76.37757540733], [52.83108869489])
    #for prange in pranges:
    #    fname = f'XpContinuousMeanSpectrum_{prange}.csv.gz'
    #    continuous = manager.get_data(f'gaia/{fname}', f"https://cdn.gea.esac.esa.int/Gaia/gdr3/Spectroscopy/xp_continuous_mean_spectrum/{fname}")
    #    fname = f'XpSampledMeanSpectrum_{prange}.csv.gz'
    #    sampled = manager.get_data(f'gaia/{fname}', f"https://cdn.gea.esac.esa.int/Gaia/gdr3/Spectroscopy/xp_sampled_mean_spectrum/{fname}")

    #fid = gzip.GzipFile(sampled)
    #toto = read_gaia(fid)
    #import pandas as pd
    #import ast
    #toto = pd.read_csv(fid, comment='#', converters={'flux': lambda x: np.array(ast.literal_eval(x))})
    #toto = np.loadtxt(fid, delimiter=',', skiprows=1)
    meta, flux = retrieve_gaia_data(pranges[0])
    bf = np.atleast_1d(np.load('/home/betoule/ohp_archive/2024_10_10/IMG_0082508_transform.npy', allow_pickle=True))[0]
    from stardiceonline.processing import astrometric_model
    transfo = astrometric_model.Transfo()
    x, y = transfo(bf, meta['ra'], meta['dec'])
    plt.plot(x, y, '.')
    goods = (x < 1024) & (x > 0) & (y < 1024) & (y > 0)
    plt.plot(x[goods], y[goods], '.')
