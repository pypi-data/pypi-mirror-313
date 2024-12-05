#!/usr/bin/python
import astropy.io.fits as pyfits
from . import ctoolbox
import numpy as np
from .robuststat import robust_average
import logging
from .catalog import seeing2sigma
from . import minimap

        
class Image():
    def __init__(self, filename, dead=None, flat=None, ext=0):
        if isinstance(filename, str):
            self.fid = pyfits.open(filename)
            if 'DATASEC' in self.fid[ext].header:
                datasec = eval(self.fid[ext].header['DATASEC'].replace(':', ','))
                datasec = np.array(datasec)
                self.data = self.fid[0].data[datasec[2] - 1:datasec[3],
                                             datasec[0] - 1:datasec[1]]
                self.header = self.fid[ext].header
            else:
                self.data = self.fid[ext].data
                self.header = self.fid[ext].header
        else:
            self.data = filename
            self.header = {}
        
        self.noback = None
        self.skylev = None
        self.sigmaback = None
        self.skyvar = None
        self.dead = dead
        self.flat = flat
        self.bias = None
        self.dark = None
        
    def detrend(self, bias_model=None, dark_model=None, flat_model=None, force=False):
        for dtr in bias_model, dark_model, flat_model:
            if dtr is not None:
                dtr.apply(self, force=force)
        self.bias = bias_model
        self.flat = flat_model
        self.dark = dark_model

    def show(self, d, new=False):
        if new:
            d.set('frame new')
        d.set_np2arr(self.data)

    def croissance(self, g_params, r_min=2, r_max=100):
        """
        Francois:
        do the aperture photometry for different radii
        """
        radii = np.arange(r_min, r_max)
        croiss = np.zeros((len(radii), len(g_params)))
        for _a, a in enumerate(g_params):
            position = (a['x'], a['y'])
            for i, r in enumerate(radii):
                aperture = CircularAperture(position, r)
                croiss[i, _a] = aperture_photometry(self.data-self.skylev, aperture)[0][0]
        return np.rec.fromrecords(croiss.T, names=['ap%d' % ap for ap in range(r_min, r_max)])
        

    def background_fast(self, decimate=1000):
        """ Fast estimate of the background level and variance
        """
        self.skylev, mask, npixinv, self.skyvar = robust_average(
            self.data.ravel()[::decimate], axis=0, clip=3, mini_output=False)
        self.sigmaback = np.sqrt(self.skyvar)
        #print(('Fast background estimate m = %f, s = %f' % (self.skylev, self.sigmaback)))
        return self.skylev, self.skyvar
    
    def background_slow(self, nside=256, sigma_seg=3):
        if not hasattr(self, "segm"):
            self.segment(5, sigma_seg)
        self.miniback, self.sigmaback, self.minisigma = ctoolbox.minimap(self.data.astype(float),
                                                                         self.segm,
                                                                         deads=self.dead,
                                                                         nside=nside)
        
        #back = scipy.ndimage.zoom(self.miniback, nside, prefilter=False, order=3)
        back = minimap.interpolate(self.miniback, nside, self.data.shape)
        self.varmap = minimap.interpolate(self.minisigma**2, nside,
                                          self.data.shape, deg=1) #avoid <0 pixels
        self.skylev = np.nanmean(self.miniback)#.mean()
        #print(('Structured background estimate m = %f, s = %f' % (self.skylev, self.sigmaback)))
        return back, self.sigmaback

    def backsub(self, method=None, **keys):
        """ Subtract a background estimate
        """
        if method is None:
            method = self.background_fast
        back, sig = method(**keys)
        self.noback = self.data - back

    def fill_bads(self, start, bads=None):
        '''Inpainting of to ease deblening bad pixels DO NOT USE THE RESULT (filled) for photometry

        Why should we care for stars accross a bad pixel line ? Good
        question. In some case having a complete star catalog makes
        the astrometric match easier.
        '''
        if bads is None:
            bads =self.dead
        self.filled = ctoolbox.inpaint(start.copy(), bads[0] * start.shape[1] + bads[1])
        return self.filled
    
    def segment(self, nsig=10, nsig_isophot=5, filled=False):
        if self.noback is None:
            self.backsub()
        if filled:
            self.segm, self.nobj = ctoolbox.segment(self.filled.copy(), self.sigmaback * nsig, isophot=self.sigmaback * nsig_isophot)
        else:
            self.segm, self.nobj = ctoolbox.segment(self.noback.copy(), self.sigmaback * nsig, isophot=self.sigmaback * nsig_isophot)
        #print(('%d objects found in the segmentation process at %g, %g thresholds' % (self.nobj, nsig, nsig_isophot)))
        return self.segm, self.nobj

    # def deblend(self, segm, nobj, nsig, filled=True):
    #     l = seg2obj(segm)
    #     if filled:
    #         data = self.filled
    #     else:
    #         data = self.noback
    #     for i, ind in enumerate(l, 1):
    #         # Get the pixels value and weights
    #         if filled:
    #             val = self.filled.flat[ind]
    #         else:
    #             val = self.noback.flat[ind]
    #         # Corresponding list of pixel coordinates
    #         y = ind / self.noback.shape[1]
    #         x = ind % self.noback.shape[1]

    #         flux = val.sum()
    #         fluxmax = val.max()
    #         fluxmin = val.min()
    #         fluxmin = max(self.sigmaback, fluxmin)

    #         cut = slice(y.min(),y.max()+1), slice(x.min(),x.max()+1)

    #         #levels = np.linspace(fluxmin, fluxmax, 30)[1:-1]
    #         #levels = np.logspace(np.log10(fluxmin), np.log10(fluxmax), 30)[1:-1]
    #         levels = np.logspace(np.log10(5*self.sigmaback), np.log10(65000), 30)[1:-1]
    #         print i
    #         #if i == 1084:
    #         #    raise ValueError()
    #         partseg, newobj = ctoolbox.deblend(data, segm, cut, segm.flat[ind[0]], levels,  5e-3 * flux)
    #         print newobj
    #         #if newobj>5:
    #         #    raise ValueError()
    #         if newobj > 1:
    #             segm, nobj = deblend.assign_pixel_to_obj(partseg, data[cut], segm, cut, nobj, i, newobj)
    #     return segm, nobj
    
    def mask_dead(self):
        if self.dead is not None:
            self.data = ctoolbox.inpaint(self.data, self.dead)

    def gaussian_filtered(self, sigma, glitches=None, nsig=None, nsig_isophot=None):
        if self.dead is not None:
            self.noback[self.dead] = 0
        if glitches is not None:
            #print(('masking %d pixels identified as glitches' % len(glitches)))
            self.noback.flat[glitches] = 0
        #print(('convolving image with gaussian filter of sigma %f' % sigma))
        filtered = scipy.ndimage.filters.gaussian_filter(self.noback, sigma)
        if nsig is not None:
            decimate = 10000
            self.skylev_filtered, mask, npixinv, skyvar = robust_average(
                filtered.ravel()[::decimate], axis=0, clip=3, mini_output=False)
            self.sigma_filtered = np.sqrt(skyvar)
            #print(('Fast background estimate of the filtered map m = %f, s = %f' % (self.skylev_filtered, self.sigma_filtered)))
            segm, nobj = ctoolbox.segment(filtered, self.sigma_filtered * nsig, isophot=self.sigma_filtered * nsig_isophot)
            #print(('%d objects found in the segmentation process at %g, %g thresholds' % (nobj, nsig, nsig_isophot)))
            return segm, nobj
        else:
            return filtered

    def matched_filter(self, se_catalog):
        #bads = self.get_bads()
        #bads = np.hstack([bads, se_catalog.get_glitch_list()])
        #im = inpaint(self.data - self.skylev, bads)
        #im = np.fft.rfft2(im)
        im = np.fft.rfft2(self.data)
        sigma = se_catalog.seeing_estimate() * seeing2sigma
        #sigma = se_catalog.seeing_estimate()
        alpha = sigma ** 2 * 0.5

        k1 = 2 * np.pi * np.fft.rfftfreq(self.data.shape[1]).reshape((1, -1))
        k2 = 2 * np.pi * np.fft.fftfreq(self.data.shape[0]).reshape((-1, 1))

        k1 *= -alpha * k1
        k2 *= -alpha * k2
        k1 = np.exp(k1)
        k2 = np.exp(k2)
        im *= k1 * k2
        return Image(np.fft.irfft2(im))

    def get_bads(self):
        ccd = self.fid[0].header['EXTVER']
        fname = '/data/SNDICE2_STELLAR_OBS/detrend/dead/2003A.dead.0.36.02/ccd%02d.fits' % ccd
        badim = Image(fname)
        bads = np.where(badim.data.ravel())[0]
        return bads










