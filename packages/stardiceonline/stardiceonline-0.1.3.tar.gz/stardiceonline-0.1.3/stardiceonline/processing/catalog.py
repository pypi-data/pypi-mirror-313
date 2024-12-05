import numpy as np
from .robuststat import mad
from . import gaussfit
from . import ctoolbox
#from croaks import NTuple, rec_stack
from . import deblend

seeing2sigma = 1. / np.sqrt(8. * np.log(2))

def fwhm2alpha(fwhm, beta):
    return fwhm / (2. * np.sqrt((2.**(1./beta) - 1.)))

def alpha2fwhm(alpha, beta):
    return alpha * (2. * np.sqrt((2.**(1./beta) - 1.)))

def sigma2fwhm(sigma):
    return sigma * np.sqrt(8 * np.log(2))

def fwhm2sigma(fwhm):
    return fwhm / np.sqrt(8 * np.log(2))

def moffat(r2, alpha, beta):
    return  (beta - 1) / (np.pi * alpha ** 2) * (1 + r2/alpha ** 2) ** (-beta)

def moffat_flux(R, alpha, beta):
    ''' Integrated flux up to a given radius
    '''
    return 1 - (1 + R**2/alpha**2) ** (1-beta)

def imoffat(x, alpha, beta):
    return np.sqrt((x * np.pi * (alpha * alpha) / (beta - 1))**(-1 / beta) - 1) * alpha


def seg2obj(seg_map):
    """ Transform the segmentation map into a list of pixel list
    """
    npix = len(seg_map.ravel())
    objmask = seg_map.ravel() > 0
    objs = seg_map.ravel()[objmask].astype(int)
    pixindex = np.arange(npix)[objmask]
    s = np.argsort(objs)
    n = np.bincount(objs)
    n = n[n != 0]
    l = []
    p = 0
    for i in n:
        l.append(pixindex[s[p:p + i]])
        p = p + i
    return l

def obj2slice(obj, shape):
    '''Transform list of pixels into vignettes

    '''
    y = obj // shape[1]
    x = obj % shape[1]
        
    return x, y, (slice(y.min(),y.max()+1), slice(x.min(),x.max()+1))


def isophotal_measurements(s, val, x, y, w=None, prefix=""):
    '''Compute catalog flux, barycentre and 2nd moments in the isophotal

    '''     
    # Flux in the isophotal
    fiso = np.sum(val)
    s['fiso'] = fiso
    # Area of the isophotal
    s['isoar'] = len(val)
    # Flux in the brightest pixel
    s['fluxmax'] = val.max()
    # Barycentre
    s['x'] = np.sum(x * val) / fiso
    s['y'] = np.sum(y * val) / fiso
    # Centered second moments
    mxx = np.sum(x ** 2 * val) / fiso - s['x'] ** 2
    s[prefix+'mxx'] = mxx
    myy = np.sum(y ** 2 * val) / fiso - s['y'] ** 2
    s[prefix+'myy'] = myy
    mxy = np.sum(y * x * val) / fiso - s['x'] * s['y']
    s[prefix+'mxy'] = mxy
    if w is not None:
        s['efiso'] = 1/np.sqrt(w.sum())
        s['sx'] = np.sqrt(np.sum(x * x / w))
        s['sy'] = np.sqrt(np.sum(y * y / w))
        s['rhoxy'] = np.sum(x * y / w) / (s['sx'] * s['sy'])
            
def gaussfit_to_moments(res):
    '''Convert parameters of a Gaussian shape to second moments

    '''
    _a, _b, _c =  2 * res['galpha'], 2 * res['gbeta'], res['ggamma']
    invdet = 1/(_a * _b - _c * _c)
    mxx = _b * invdet
    myy = _a * invdet
    mxy = - _c * invdet
    a = np.sqrt(0.5 * (mxx + myy) + np.sqrt(0.25 * (mxx - myy) ** 2 + mxy ** 2))
    b = np.sqrt(0.5 * (mxx + myy) - np.sqrt(0.25 * (mxx - myy) ** 2 + mxy ** 2))
    angle = 0.5 * np.arctan2(2 * mxy, mxx - myy)
    e = np.sqrt(1 - (b/a)**2)
    sigma = invdet ** (0.25)
    val = [mxx, myy, mxy, sigma, a, b, angle, e]
    keys = ['gmxx', 'gmyy', 'gmxy', 'gsigma', 'ga', 'gb', 'gangle', 'ge']
    if 'gmxx' in res.dtype.names:
        for k, v in zip(keys, val):
            res[k] = v
    else:
        return np.rec.fromarrays(val, names=keys)

def moments_to_ellipse_param(cat, prefix=''):
    ''' Convert centered second order moments to ellipse parameters
    '''
    mxx, myy, mxy = cat[prefix+'mxx'], cat[prefix+'myy'], cat[prefix+'mxy']
    cat[prefix+'a'] = np.sqrt(0.5 * (mxx + myy) + np.sqrt(0.25 * (mxx - myy) ** 2 + mxy ** 2))
    cat[prefix+'b'] = np.sqrt(0.5 * (mxx + myy) - np.sqrt(0.25 * (mxx - myy) ** 2 + mxy ** 2))
    cat[prefix+'angle'] = 0.5 * np.arctan2(2 * mxy, mxx - myy)
    return cat
    
    
def find_stars_clump(cat, nsig=2, snr_min=20, show=False, prefix='gw'):
    ''' Look for a clump in the ellipse parameters distribution
    '''
    #highsnr = cat['gA'] / cat['egA'] > snr_min
    highsnr = cat['fiso'] / cat['efiso'] > snr_min
    glitches = (cat[prefix+'b'] < 1)
    nana = np.isnan(cat[prefix+'a'])
    nanb = np.isnan(cat[prefix+'b'])

    retain = highsnr & ~glitches & ~nana & ~nanb

    _a = cat[prefix+'a'][retain]
    _b = cat[prefix+'b'][retain]

    a = np.median(_a)
    b = np.median(_b)
    sa = mad(_a)
    sb = mad(_b)
    bads = (abs(_a - a) > nsig * sa) | (abs(_b - b) > nsig * sb)
    wrong = bads
    while wrong.any():
        a, sa = _a[~bads].mean(), _a[~bads].std()
        b, sb = _b[~bads].mean(), _b[~bads].std()
        new_bads = (abs(_a - a) > nsig * sa) | (abs(_b - b) > nsig * sb)
        wrong = new_bads != bads
        bads = new_bads
    
    #print(('stars clump location a=%f +- %f, b=%f +- %f' % (a, sa, b, sb)))
    if show:
        import matplotlib.pyplot as plt
        #print((retain.sum()))
        plt.scatter(cat[prefix+'a'][retain], cat[prefix+'b'][retain], alpha=0.2)
        plt.errorbar(a, b, xerr=[nsig * sa], yerr=[nsig*sb], marker='s', color='k')
        plt.show()
    return a, sa, b, sb

def pixeldeconvol(data):
    '''Deconvolve the image from the pixel window function

    In other terms, this turn the integral of flux over the pixel area
    into a dirac sampling of the underlying continuous function. This
    allow proper application of Bickerton & Lupton 2013 photometry.
    '''
    KX = np.fft.fftfreq(data.shape[0], 1)
    KY = np.fft.fftfreq(data.shape[1], 1)
    kx,ky = np.meshgrid(KY, KX)
    pwf = np.sinc(kx)*np.sinc(ky)
    I = np.fft.fft2(data)
    return np.real(np.fft.ifft2(I/pwf))

def freqs(n):
    KX = np.fft.fftfreq(n, 1)
    kx,ky = np.meshgrid(KX, KX)
    k = np.sqrt(kx * kx + ky * ky)
    return kx, ky, k

def airy(k, rad):
    import scipy.special as special
    airy = rad * special.j1(2.0 * np.pi * rad * k) / k
    airy[0,0] = np.pi * rad * rad
    return airy

def phase(kx, ky, x, y):
    return np.exp(-1.0j*2.0*np.pi*(x*kx + y*ky))

def bickerture_wij(phase, airy):
    wijShift = np.fft.ifft2(phase*airy)
    return np.fft.fftshift(wijShift).real

def names2aperture(cat):
    apertures = [a.split('_')[-1] for a in cat.dtype.names if a[:5] == 'apfl_']
    radius = np.array([float(a) for a in apertures])
    return apertures, radius

def cat2segmap(cat, shape, level, flux_field='tot_flux', prefix='gw', index="objid"):
    '''Draw a theoretical segmentation map accounting for detection level
    and measured object shape

    '''
    segmap = np.zeros(shape, 'i4')
    nskip = 0
    for s in cat:
        x, y = s[prefix+'x'], s[prefix+'y']
        det = s['gwmxx'] * s['gwmyy'] - s['gwmxy'] * s['gwmxy']
        wxx = s['gwmyy'] / det
        wyy = s['gwmxx'] / det
        wxy = -s['gwmxy'] / det
        A = s[flux_field] / (2*np.pi * det)
        #if A < level:
        #    nskip += 1
        #    continue
        # rxx = np.sqrt(2*np.log(A / level) / wxx)
        # ryy = np.sqrt(2*np.log(A / level) / wyy)
        # xmin = max(0, int(np.floor(x-rxx)))
        # xmax = min(shape[1], int(np.ceil(x+rxx)))
        # ymin = max(0, int(np.floor(y-ryy)))
        # ymax = min(shape[0], int(np.ceil(y+ryy)))
        # if ymin>ymax or xmin>xmax:
        #     nskip += 1
        #     continue
        # _x, _y = np.mgrid[xmin:xmax, ymin:ymax]
        # _x = _x.T
        # _y = _y.T
        # dx = _x - x
        # dy = _y - y
        # wg = wxx * dx * dx + wyy * dy * dy + 2 * wxy * dx * dy
        # prof = np.exp(-0.5 * wg)
        if 1: # moffat profile
            beta = 2.2
            alpha = fwhm2alpha(sigma2fwhm(np.sqrt(s["gwmxx"])), beta)/1.2
            radius = imoffat(level / s[flux_field], alpha, beta)
            if np.isnan(radius):
                nskip += 1
                continue
            xmin = max(0, int(np.floor(x-radius)))
            xmax = min(shape[1], int(np.ceil(x+radius)))
            ymin = max(0, int(np.floor(y-radius)))
            ymax = min(shape[0], int(np.ceil(y+radius)))
            if ymin>ymax or xmin>xmax:
                nskip += 1
                continue
            _x, _y = np.mgrid[xmin:xmax, ymin:ymax]
            _x = _x.T
            _y = _y.T
            dx = _x - x
            dy = _y - y
            r2 = dx**2+dy**2
            scale = (beta - 1) / (np.pi * alpha ** 2)
            prof = moffat(r2, alpha, beta)#/scale
        segmap[ymin:ymax,xmin:xmax][prof > (level / s[flux_field])] = s[index]
        
    #print(("skipped %d/%d"%(nskip, len(cat))))
    return segmap

class ImageObjects():
    ''' Image catalog
    '''
    basecat_format = [('x', float), ('y', float), ('sx', float), ('sy', float), ('rhoxy', float), ('ra', float), ('dec', float), ('fluxmax', float),
                      ('fiso', float), ('efiso', float), ('isoar', 'i4'),
                      ('mxx', float), ('myy', float), ('mxy', float), ('a', float), ('b', float), ('angle', float), ('objtype', 'i2'), ('objid', 'i4'), ('expnum', 'i4'), ('ccd', 'i2'), ('mjd', float)]
    gf_format = [('gx', float), ('gy', float), ('galpha', float), ('gbeta', float), ('ggamma', float), ('gA', float), ('gback', float)]
    gf_format += [('v' + f[0], float) for f in gf_format] + [('vgxy', float)]
    gf_format += [('gchi2', float), ('gdof', 'i4')]
    gf_format += [(f,float) for f in ['gmxx', 'gmyy', 'gmxy', 'gsigma', 'ga', 'gb', 'gangle', 'ge']]
    gw_format = [(f, float) for f in ['gwx', 'gwy', 'gwmxx', 'gwmyy', 'gwmxy','vgwx', 'vgwy', 'vgwxy']]
    gw_format += [(f, bool) for f in ['contaminated', 'hasbads', 'windowed', 'unconverged', 'blended', 'glitch', 'saturated']]
    gw_format += [(f, float) for f in ['gwa', 'gwb', 'gwangle']]
    types = {'star': 0,
             'galaxy': 1,
             'glitch': 3}

    def __init__(self, seg_map, min_isoar=7, radius=[], cat=None, additionnal_header_keys={}):
        def guess_format(v):
            if isinstance(v, float):
                return float
            elif isinstance(v, int):
                return int
            else:
                return 'S50'
    
        self.radii = radius
        self.cat_format = self.basecat_format + self.gw_format
        self.cat_format += [('ap%s_%.2f' % (suf, rad), float) for rad in self.radii for suf in ['fl', 'var', 'other', 'bad']]
        self.cat_format += [(k, guess_format(v)) for k,v in additionnal_header_keys.items()]
        self.additionnal_header_keys = additionnal_header_keys

        if seg_map is not None:
            self.seg_map = seg_map
            # Slicing the segmentation map into a list of pixel per star
            self.l = seg2obj(seg_map)
            self.cat = None
            self.min_isoar = min_isoar
        else:
            #self.cat = cat
            self.cat_format = [(k, v) for k,v in cat.dtype.descr]#list(cat.dtype.fields.items())]
            self.cat_format += [('ap%s_%.2f' % (suf, rad), float) for rad in self.radii for suf in ['fl', 'var', 'other', 'bad']]
            
            self.cat = np.zeros(len(cat), dtype=self.cat_format)
            for field in list(cat.dtype.fields.keys()):
                self.cat[field] = cat[field]
                #aperture, self.radii = names2aperture(cat)
            
    def build_segcat(self, back_subtracted, weights=None, skyvar=None, gain=None):
        """Top level routine to turn the segmentation map into a catalog,
        no deblending performed (see deblended catalog for another top-level routine
        
        Quantities are computed in the isophotal (see isophotal_measurement)
        """
        l = self.l
        if weights is None:
            if skyvar is not None:
                weights = np.full(back_subtracted.shape, 1./skyvar)

        self.im_heigt, self.im_width = back_subtracted.shape 
        # initialising an empty catalog
        nstars = len(l)
        cat = np.zeros(nstars, dtype=self.cat_format)

        # Loop on each star
        for _s, s in enumerate(cat):
            ind = l[_s]
            s['objid'] = self.seg_map.flat[ind[0]]
            # Get the pixels value and weights
            val = back_subtracted.flat[ind]
            if weights is not None:
                w = weights.flat[ind]
            else:
                w = None
            # Corresponding list of pixel coordinates
            y = ind // back_subtracted.shape[1]
            x = ind % back_subtracted.shape[1]

            isophotal_measurements(s, val, x, y, w=w)
            
        cat = moments_to_ellipse_param(cat)
        for k in self.additionnal_header_keys:
            cat[k] = self.additionnal_header_keys[k]
        self.cat = cat
        return cat

    def deblended_catalog(self, data, weights, levels, gain=None, threshold=5e-3, sat=None):
        l = self.l
        nobj = len(l)
        cat = []
        S = np.zeros(1, dtype=self.cat_format)[0]
        for i, ind in enumerate(l, 1):
            # Get the pixels value and weights
            val = data.flat[ind]
            # Corresponding list of pixel coordinates
            y = ind // data.shape[1]
            x = ind % data.shape[1]
            cut = slice(y.min(),y.max()+1), slice(x.min(),x.max()+1)
            
            s = S.copy()
            s['objid'] = self.seg_map.flat[ind[0]]
            flux = val.sum()

            if sat is not None:
                s['saturated'] = np.any(sat[cut])

            if len(val) < self.min_isoar:
                # Measuring anything is going to be hard
                # We consider this as a glitch
                w = weights.flat[ind]
                s['glitch'] = True
                isophotal_measurements(s, val, x, y, w=w)
                cat.append(s)
                continue
            
            partseg, newobj = ctoolbox.deblend(data, self.seg_map, cut, self.seg_map.flat[ind[0]], levels,  threshold * flux)

            if newobj > 1:
                self.seg_map, nobj, subcat = deblend.assign_pixel_to_obj(partseg, data, weights, self.seg_map, cut, nobj, i, newobj, S.copy())
                #self.seg_map, nobj, subcat = deblend.assign_pixel_to_obj_em(partseg, data, weights, self.seg_map, cut, nobj, i, newobj, S.copy())
                cat.extend(subcat)
            else:
                w = weights.flat[ind]
                isophotal_measurements(s, val, x, y, w=w)
                ctoolbox.gaussian_weighted_moments(data, s)
                #if i == 743:#796:
                #    stop
                gaussfit.gaussian_weighted_moment_variance(data, self.seg_map, weights, s, gain=gain)
                cat.append(s)
        self.cat = np.hstack(cat)
        for k in self.additionnal_header_keys:
            self.cat[k] = self.additionnal_header_keys[k]
            #print(self.additionnal_header_keys)
        moments_to_ellipse_param(self.cat)
        moments_to_ellipse_param(self.cat, 'gw')
        return self.seg_map, nobj, np.hstack(cat)

    def build_gaussfitcat(self, back_subtracted, skyvar, show=False, nsigma=5, maxfev=15, segm=None, weight=None):
        sigma0 = self.seeing_estimate() * seeing2sigma
        if np.isscalar(skyvar):
            skyvar = skyvar*np.ones(back_subtracted.shape)
        if show:
            import matplotlib.pyplot as plt
            f_source = plt.figure()
            f_res = plt.figure()
            nplot = np.ceil(np.sqrt(len(self.cat)))

        for _s, s in enumerate(self.cat, 1):

            # prepare vignettes
            grid = gaussfit.vignette(s["x"], s["y"], sigma0, nsigma, back_subtracted.shape)
            S = skyvar[grid[2]:grid[3], grid[0]:grid[1]].T
            I = back_subtracted[grid[2]:grid[3], grid[0]:grid[1]]
            if weight is not None:
                w = (weight[grid[2]:grid[3], grid[0]:grid[1]].T).copy()
                if segm is not None:
                    o = segm[grid[2]:grid[3], grid[0]:grid[1]].T
                    selec = np.logical_and(o!=0, o!=_s) 
                    w[selec] = 0
            
            # do the fit
            X, covx, chi2, dof, V, residu = gaussfit.gaussfit(I, s['x'], s['y'], s['fluxmax'], sigma0, S, grid, maxfev=maxfev, weight=weight if weight is None else w)
            if np.isnan(chi2):
                vgxy = np.nan
            else:
                vgxy = covx[0,1]
                covx = np.diag(covx)
            
            for (f,t), v in zip(self.gf_format, np.r_[X, covx, vgxy, chi2, dof]):
                self.cat[f][_s-1] = v
                
            if show:
                ax = f_source.add_subplot(nplot, nplot, _s)
                ax.imshow(V, interpolation='none')
                ax = f_res.add_subplot(nplot, nplot, _s)
                ax.imshow(residu.reshape(V.shape), interpolation='none')
        gaussfit_to_moments(self.cat)

    def build_emcat(self, back_subtracted, weights, segm):
        null = (np.nan,) * 8 + (False,) * 3 + (True,)
        for _s, s in enumerate(self.cat):
            # prepare vignettes
            if s['isoar'] < self.min_isoar:
                for (f, t), r in zip(self.gw_format, null):
                    self.cat[_s][f] = r
            else:
                ctoolbox.gaussian_weighted_moments(back_subtracted, s)
                if mom[-1] == 0 and mom[2] > 0 and mom[3] > 0:
                    v = gaussfit.gaussian_weighted_moment_variance(back_subtracted, segm, weights, mom[0], mom[1], mom[2], mom[3], mom[4], s['objid'])
                else:
                    v = (np.nan,) * 3 + (False,) * 3 + (True,)
                res = mom[:-1] + v + (mom[-1],)
                for (f, t), r in zip(self.gw_format, res):
                    self.cat[_s][f] = r
        moments_to_ellipse_param(self.cat, prefix='gw')
        
    def build_apercat(self, data, var, segm, prefix="gw", index='objid'):
        for _s, s in enumerate(self.cat):
            #if s['glitch'] or s['unconverged'] or s['blended']:
            #    continue
            for radius in self.radii:
                suff = '_%.2f' % radius
                res = ctoolbox.circular_aperture(data, var, segm, s[index],
                                                 s[prefix+'x'], s[prefix+'y'], radius)
                s['apfl' + suff] = res.flux
                s['apvar' + suff] = res.variance
                s['apother' + suff] = res.other
                s['apbad' + suff] = res.bad

    def bickerture(self, data, var, segm, n=32, rmax=8, prefix='gw', sat=None, index='objid'):
        I = pixeldeconvol(data)
        kx, ky, k = freqs(n)
        radii = [r for r in self.radii if r < rmax]
        airys = [airy(k, radius) for radius in radii]
        for _s, s in enumerate(self.cat):
            #if s['glitch'] or s['unconverged'] or s['blended']:
            #    continue
            x, y = s[prefix+'x'], s[prefix+'y']
            if (int(x) - n//2) < 0 or (int(x) +n//2) > data.shape[1]:
                s["windowed"] = True
                continue # todo set a flag
            if (int(y) - n//2) < 0 or (int(y) +n//2) > data.shape[0]:
                s["windowed"] = True
                continue
            vignette = slice(int(y)-n//2,int(y)+n//2), slice(int(x)-n//2,int(x)+n//2)
            V = I[vignette]
            W = var[vignette]
            O = segm[vignette]
            O = (O != 0) & (O != s[index])
            B = ~np.isfinite(W)

            if sat is not None:
                s['saturated'] = np.any(sat[vignette])

            
            ph = phase(kx, ky, x%1, y%1)
            for _r, radius in enumerate(radii):
                suff = '_%.2f' % radius
                wij = bickerture_wij(ph, airys[_r])
                T = wij * V
                s['apfl' + suff] = (wij * V).sum()
                s['apvar' + suff] = ((wij * W)[~B]).sum()
                s['apother' + suff] = (T[O]).sum()
                s['apbad' + suff] = (T[B]).sum()
                
    def identify(self, nsigma=2, prefix='gw'):
        self.cat['objtype'] = self.types['galaxy']
        #glitches = np.isnan(self.cat['gb']) | (self.cat['gb'] < 1)
        glitches = self.cat['unconverged'] | self.cat['contaminated'] | self.cat['blended'] | self.cat['windowed'] | self.cat['glitch'] | self.cat['hasbads']
        self.cat['objtype'][glitches] = self.types['glitch']
        a, sa, b, sb = find_stars_clump(self.cat[~glitches], nsig=nsigma, snr_min=20, prefix=prefix)
        stars = (np.abs(self.cat[prefix + 'a'] - a) < nsigma * sa) & (np.abs(self.cat[prefix + 'b'] - b) < nsigma * sb) & ~glitches
        self.cat['objtype'][stars] = self.types['star']
        
    def seeing_estimate(self):
        ''' Return an estimate of the FWHM in pixels
        '''
        if self.cat['objtype'].any():
            stars = self.cat['objtype'] == self.types['star']
            sigma = self.cat['gsigma'][stars].mean()
            fwhm = sigma / seeing2sigma
            #print(('Accurate gaussian seeing estimate fwhm=%f, sigma=%f' % (fwhm, sigma))) 
        else:
            glitches = (self.cat['b'] < 1) | (self.cat['isoar'] < 10)
            retain  = ~glitches & (self.cat['fiso'] > 100000 )
            if retain.sum()==0:
                retain  = ~glitches & (self.cat['fiso'] > 90000 )
            flux_ratio = np.nanmedian(self.cat['fluxmax'][retain] / self.cat['fiso'][retain])

            sigma = np.sqrt( -0.5 / (np.log(1.-np.pi*flux_ratio) ))
            #retain = ~glitches & (self.cat['efiso
            #sigma = np.nanmedian(np.sqrt(self.cat['a'][~glitches] * self.cat['b'][~glitches]))
            fwhm = sigma / seeing2sigma
            #print(('Temporary rough seeing estimate fwhm=%f, sigma=%f' % (fwhm, sigma))) 
        return fwhm

    def get_glitch_list(self):
        glitches = self.objtype == self.types['glitch']
        return np.hstack([l for l, g in zip(self.l, glitches) if g])

    
    def add_to_cat(self, fields, data):
        import numpy.lib.recfunctions as recf
        self.cat = recf.append_fields(self.cat, fields, data, usemask=False) 
            
    def write_cat(self, filename):
        self.cat.view(NTuple).tofile(filename)

