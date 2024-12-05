import glob
import numpy as np
import os
from stardiceonline.processing import read_headers
from stardiceonline.archive.file_tools import *
import astropy.io.fits as pyfits
import astropy.wcs

class SummaryPlots(object):
    def __init__(self, directory):
        self.directory = directory
        if os.path.exists(f'{directory}/summary_plots.npy'):
            self.summary = [tuple(e) for e in np.load(f'{directory}/summary_plots.npy')]
            self.expnum = set(self.get_summary()['EXPNUM'])
        else:
            self.summary = []
            self.expnum = set([])
        self.update()

    def update(self):
        catalogs = glob.glob(f'{self.directory}/*photometric_cat.npy')
        if catalogs:
            catalogs.sort()
            for _c, c in enumerate(catalogs):
                print(f'Processing file {_c}/{len(catalogs)}', end='\r')
                self.add_exposure(cat2expnum(os.path.basename(c)))
            np.save(f'{self.directory}/summary_plots.npy', self.get_summary())
        
    def add_exposure(self, expnum):
        if expnum not in self.expnum:
            h = pyfits.getheader(expnum2filename(self.directory, expnum))
            try:
                cat = np.load(expnum2filename(self.directory, expnum, 'catalogs'))
                if len(cat) == 0:
                    cat = None
            except IOError:
                cat = None
            except TypeError:
                cat = np.atleast_1d(cat)
            except Exception:
                print(f'Unexpected exception processing {self.directory}')
                raise
            try:
                wcs = astropy.wcs.WCS(expnum2filename(self.directory, expnum, 'wcs'))
            except IOError:
                wcs = None

            self.summary.append(read_headers.read_all(h, cat, wcs))
            self.expnum.add(expnum)
            
    def get_summary(self):
        if len(self.summary) == 0:
            return self.summary
        else:
            return np.rec.fromrecords(self.summary, names=read_headers.all_keys)
    
if __name__ == '__main__':
    s = SummaryPlots('/data/STARDICE/stardiceot1/2023_03_28/')
    nt = s.get_summary()
