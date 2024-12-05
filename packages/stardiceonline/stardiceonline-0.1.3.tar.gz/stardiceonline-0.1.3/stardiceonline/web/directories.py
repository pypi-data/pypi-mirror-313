import os
import glob
import bokeh.models
import astropy.io.fits as pyfits
import astropy.wcs
from stardiceonline.processing.detrending import *
import numpy as np
#from stardiceonline.archive import file_watcher
from watchdog.observers import Observer
import bisect
from stardiceonline.archive.file_tools import *
import logging
import numpy as np
from stardiceonline.tools.config import config

root_directory = config['archive.local']

product_types = ['expnum', 'catalog', 'astrom', 'offline', 'ir', 'spectrum']

class RobustHeader():
    def __init__(self, header):
        self.header = header

    def __getitem__(self, key):
        if key not in self.header:
            return 'NotFound'
        else:
            return self.header[key]

class ImageDirectory(object):
    def __init__(self, directory, rootdir):
        self.directory = directory
        self.rootdir = rootdir
        self._listing()
        self.observer = Observer()
        from pipelet3.external_events import CustomEventHandler
        self.observer.schedule(CustomEventHandler([self.new_file_callback], '*'),
                               directory, recursive=True)
        print(f'Watching for new files in directory {directory}')
        self.observer.start()  # Start the observer thread
        self.callbacks = []

    def stop(self):
        self.observer.stop()
        
    def _listing(self):
        listing = os.listdir(self.directory)
        for attr, regexp in [('images', re_expnum), ('catalogs', re_catalog), ('astrom_catalogs', re_astrom_catalog)]:
            setattr(self, attr, [i for i in listing if regexp.match(i)])
        self._update()
        
    def _update(self):
        for attr in ['images', 'catalogs', 'astrom_catalogs']:
            getattr(self, attr).sort()
        self.expnum = [im2expnum(i) for i in self.images]

    def summary(self):
        mi = self.expnum[0]
        ma = self.expnum[-1]
        data = np.zeros(ma-mi+1, dtype=[('expnum', int), ('catalog', f'U{len(self.catalogs[0])}'), ('astrom', f'U{len(self.astrom_catalogs[0])}'), ('offline', bool), ('ir', bool), ('spectrum', bool)])
        data['expnum'][np.array(self.expnum) - mi] = self.expnum
        for c in self.catalogs:
            data['catalog'][cat2expnum(c) - mi] = c
        for c in self.astrom_catalogs:
            data['astrom'][astromcat2expnum(c) - mi] = c
        goods = data['expnum'] > 0
        return dict(zip(product_types, [data[f][goods] for f in product_types]))
    
    def night(self):
        return os.path.basename(self.directory)

    def expnum2filename(self, expnum, kind='images'):
        return expnum2filename(self.directory, expnum, kind=kind)
        
    def __getitem__(self, expnum):

        if expnum < 0:
            return [], [], 'No images available for this night'
        ir = []
        ir_stream = []
        with pyfits.open(self.expnum2filename(expnum)) as fid:
            data = detrend(fid)
            header = RobustHeader(fid[0].header)
            if 'IR_STREAM' in fid:
                ir_stream = fid['IR_STREAM'].data
            if 'IR' in fid:
                ir = fid['IR'].data
        try:
            fname = self.expnum2filename(expnum, 'astrom_catalogs')
            fname2 = self.expnum2filename(expnum, 'catalogs')
            if os.path.exists(fname):
                catalog = np.atleast_1d(np.load(fname))
            elif os.path.exists(fname2):
                catalog = np.atleast_1d(np.load(fname2))
            else:
                catalog = []
        except IOError:
            catalog = []
        if os.path.exists(self.expnum2filename(expnum, 'wcs')):
            wcs = astropy.wcs.WCS(self.expnum2filename(expnum, 'wcs'))
        else:
            try:
                wcs = astropy.wcs.WCS(header)
            except:
                wcs = None
                logging.error(f'Mount WCS not available in image {expnum}')
        title = f'{self.directory}/IMG_{expnum:07d}.fits {header["filterwheelfilter"]}'
        #if 'mountTARGET' in header:
        title += f' {header["mountTARGET"]}'
        return data, catalog, title, header, wcs, ir, ir_stream

    def last(self):
        if len(self.expnum):
            return self.expnum[-1]
        else:
            return -1
        
    def next(self, expnum):
        try:
            i = self.expnum.index(expnum)
            return self.expnum[i+1]
        except ValueError:
            return self.expnum[-1]

    def prev(self, expnum):
        try:
            i = self.expnum.index(expnum)
            return self.expnum[i-1]
        except ValueError:
            return self.expnum[0]

    def orphans(self):
        available_catalogs = set([cat2expnum(c) for c in self.catalogs])
        missing_catalogs = list(set(self.expnum).difference(available_catalogs))
        available_astrom = set([astromcat2expnum(c) for c in self.astrom_catalogs])
        missing_astrom = available_catalogs.difference(available_astrom)
        return [('images', self.expnum2filename(expnum)) for expnum in missing_catalogs]\
            + [('catalogs', self.expnum2filename(expnum, 'catalogs')) for expnum in missing_astrom]
    
    def new_file_callback(self, filename):
        logging.debug(f'New file in directory {self.directory}: {filename}')
        basename = os.path.basename(filename)
        for attr, regexp in [('images', re_expnum), ('catalogs', re_catalog), ('astrom_catalogs', re_astrom_catalog)]:
            if regexp.match(basename):
                logging.info(f'new {attr} available: {filename}')
                l = getattr(self, attr)
                bisect.insort(l, basename)
                if attr == 'images':
                    bisect.insort(self.expnum, im2expnum(basename))
                self.rootdir.update()
                for c in self.callbacks:
                    c(attr, filename)
                #callbacks = self.callbacks.get(attr, [])
                #for c in callbacks:
                #    c(attr, filename)
                
class ImageDirectories(object):
    def __init__(self, root_directory):
        from stardiceonline.archive import archive
        self.root_directory = root_directory
        self.directory_names = [d for d in glob.glob(os.path.join(self.root_directory, '*')) if os.path.isdir(d) and os.path.basename(d) not in archive.local_archive.special]
        self.directory_names.sort()
        self.directories = [ImageDirectory(d, self) for d in self.directory_names]
        self.callbacks = []
        self.update()
        
    def update(self):
        self.source={'nights': [d.night() for d in self.directories]}
        for field in ['images', 'catalogs', 'astrom_catalogs']:
            self.source[field] = [len(getattr(d, field)) for d in self.directories]
        for c in self.callbacks:
            c()
            
    def get_source(self):
        directory_data = bokeh.models.ColumnDataSource(data=dict(**self.source))
        directory_data.selected.indices=[len(self.directories)-1]
        return directory_data

    def update_source(self):
        return dict(**self.source)
    
    def __getitem__(self, i):
        return self.directories[i]

    def set_callback(self, callback):
        self.callbacks = [callback]

    def set_children_callback(self, callback):
        for d in self.directories:
            d.callbacks = [callback]
            
    def orphans(self):
        return sum([d.orphans() for d in self.directories], [])

    def stop(self):
        for d in self.directories:
            d.stop()
        self.directories = []
            
image_dirs = ImageDirectories(root_directory)





