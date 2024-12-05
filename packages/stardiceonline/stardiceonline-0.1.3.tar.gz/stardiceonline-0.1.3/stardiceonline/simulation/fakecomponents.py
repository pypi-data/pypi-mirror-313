import jax
import jax.numpy as jnp
import numpy as np
from stardiceonline.tools.config import config
from stardiceonline.tools.metadatamanager import MetaDataManager
from stardiceonline.processing import astrometric_model
from stardiceonline.simulation import gaia

import scipy
import os
import glob
transfo = astrometric_model.Transfo()

manager = MetaDataManager()

transmissions = np.load(manager.get_data('stardice_full_pupil_dr5.npy', 'http://supernovae.in2p3.fr/stardice/stardiceot1/stardice_full_pupil_dr5.npy'))

wl = jnp.arange(336,1021,2)

def gaussian_2d(xy, x0, y0, flux, sigma):
    x, y = xy
    return flux * jnp.exp(-(((x - x0)**2 + (y - y0)**2) / (2 * sigma**2)))

def draw_star(xy, star_params):
    x0, y0, flux, sigma = star_params
    return gaussian_2d(xy, x0, y0, flux, sigma)

vmap_draw = jax.vmap(draw_star, in_axes=(None, 0))

def illuregiontoshape(illuregion):
    return (illuregion[0][1] - illuregion[0][0]), (illuregion[1][1] - illuregion[1][0])

def framedef(illuregion):
    shape = illuregiontoshape(illuregion)
    def f(x, y):
        return (x >= 0) & (x < shape[0]) & (y >=0) & (y < shape[1])
    return f

def pixel_area_arcsec2(pixel_size_microns, focal_length_mm):
    # Convert pixel size to mm
    pixel_size_mm = pixel_size_microns * 1e-3
    
    # Convert to arcseconds
    theta_arcsec = (pixel_size_mm / focal_length_mm) * 206265
    
    # Calculate area in arcsec²
    area_arcsec2 = theta_arcsec ** 2
    
    return area_arcsec2

    
class Component():
    def __init__(self, static):
        self.static = static
        
    def process_state(self,state):
        return {}
    
    def process_image(self, image, state, sources):
        return image
    
    def process_sources(self, sources, state):
        return sources

    def process_psf(self, psf, state):
        return psf, state


class FakeMount(Component):
    def process_state(self, state):
        return {'fptrans_a': jnp.array([ 2.1089346e+03, -1.1738972e+01,  4.0282936e+00, -3.3291507e-01,
                                4.2525875e+01]),
                'fptrans_b': jnp.array([  11.205614, 2108.7246  ,  -48.857784,   -4.316577,    3.11636 ]),
                'dec_center': jnp.array([52.800373]),
                'ra_center': jnp.array([76.383095])}

class FakeCamera(Component):
    def process_image(self, image, state, sources):
        shape = self.static['shape']
        noise = jax.random.normal(state['key'], shape) * state['readout_noise'] + state['bias']
        return jnp.uint16((image + noise)/state['gain'])

    def process_state(self, state):
        return {'pixel_size_micron':13.5,
                'readout_noise': 5,
                'bias': 250, #e-
                'gain': 1.2,
                'exptime': state['exptime'],
                }
    def process_sources(self, sources, state):
        sources['spectra'] = sources['spectra'] * (wl*1e-9 / (scipy.constants.c * scipy.constants.h) * state['exptime'])
        sources['flux'] = sources['spectra'].sum(axis=1)*2 #nm
        return sources
    
class FakeSky(Component):
    def __init__(self, static):
        ''' 
        pixel_area in arcsec^2
        '''
        self.static = static
        self.coef = {
            'u': jnp.array([  0.89148842,  11.87538592]),
            'g': jnp.array([  0.89148842,  11.87538592]),
            'r': jnp.array([  0.87013466,  12.2014959 ]),
            'i': jnp.array([  0.85605964,  12.05601565]),
            'z': jnp.array([  0.8970776 ,  11.79488411]),
            'y': jnp.array([  0.8970776 ,  11.79488411]),
        }
        self.inframe = framedef(self.static['illuregion'])
        illushape = illuregiontoshape(self.static['illuregion'])
        x = jnp.arange(0, illushape[0])
        y = jnp.arange(0, illushape[1])
        self.xy = jnp.meshgrid(y, x)

    def background_level(self, band, sunalt):
        ''' Return background brightness in mag/arcsec^2
        ''' 
        brightness = jnp.exp(jnp.polyval(self.coef[band], sunalt))
        return brightness

    def process_state(self, state):
        return {'background_level':self.background_level(state['band'], state['sunalt']),}
    
    def process_image(self, image, state, sources):
        shape = self.static['shape']
        stars_params = jnp.array([sources['x'], sources['y'], sources['flux'], jnp.full(len(sources['x']), 1.5)]).T
        # Draw all stars at once
        star_field = vmap_draw(self.xy, stars_params).sum(axis=0) + state['background_level']  # Sum contributions from all stars

        poisson_real = jax.random.poisson(state['key'], star_field)
        (a, b), (c,d) = self.static['illuregion']
        return image.at[a:b,c:d].add(poisson_real)

    def process_sources(self, sources, state):
        pranges = gaia.get_pix_range([state['ra_center']], [state['dec_center']])
        meta, flux = gaia.retrieve_gaia_data(pranges[0])
        x, y = transfo(state, meta['ra'], meta['dec'])
        goods = self.inframe(x, y)
        return {'x': x[goods],
                'y': y[goods],
                'spectra': flux[goods,:]}
        
class FakeNewton(Component):
    def process_state(self, state):
        return {'focal_length_m': 1.6,
                'diameter_m': 40e-2,
                'transmission': jnp.interp(wl, transmissions['wl'], transmissions[state['band']])}

    def process_sources(self, sources, state):
        sources['spectra'] = sources['spectra'] * state['transmission'] * (state['diameter_m']**2/4/jnp.pi)
        return sources

class FakeMeteo():
    def __init__(self):
        self.meteo_log_dir = os.path.expanduser(config['simu.meteolog'])
        self.logs = glob.glob(os.path.join(self.meteo_log_dir, 'meteo*.csv'))
        self.logs.sort()
        self.currentlog = self.read_log(self.logs[0])
        
    def get_meteo(self):
        return dict(zip(self.currentlog.dtype.names, self.currentlog[0]))
    
    def read_log(self, fname):
        values = []
        with open(fname, 'r') as fid:
            for line in fid.readlines():
                if line.startswith('#'):
                    keys = line[1:].split(',')
                else:
                    values.append(line.split(','))
        return np.rec.fromrecords(values, names=keys)
    
