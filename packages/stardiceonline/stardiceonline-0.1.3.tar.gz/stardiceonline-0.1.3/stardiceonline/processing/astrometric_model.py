import jax.numpy as jnp
import numpy as np
from stardiceonline.processing import jaxfitter

def gnomonic_projection(params, ra, dec):
    ''' Projection on the plane tangent to a provided center

    Parameters:
    -----------
    params: pytree specifying the tangent point coordinates:
            - "ra_center": deg
            - "dec_center": deg
    ra: coordinate to project in deg
    dec: coordinate to project in deg

    Return:
    -------
    x, y: tangent plane coordinates in degrees
    '''
    ra_rad, dec_rad = jnp.radians(ra), jnp.radians(dec)
    rac, decc = jnp.radians(params['ra_center']), jnp.radians(params['dec_center'])
    s, c = jnp.sin(dec_rad), jnp.cos(dec_rad)
    c2 = jnp.cos(rac - ra_rad)
    d = jnp.sin(decc) * s + jnp.cos(decc) * c * c2
    x = (jnp.cos(decc) * jnp.sin(rac - ra_rad)) / d
    y = (jnp.sin(decc) * c - jnp.cos(decc) * s * c2) / d
    return jnp.degrees(x), jnp.degrees(y)


class Transfo():
    n_extra_pars = 3

    def __call__(self, params, ra, dec, sensor_center=(512, 512)):
        ''' Composed function chaining a tangent plane projection with polynomial corrections to absorb optical distortions

        Parameters:
        -----------
        params: pytree specifying the tangent point coordinates:
            - "ra_center": deg
            - "dec_center": deg
        ra: coordinate to project in deg
        dec: coordinate to project in deg

        Return:
        -------
        x, y: sensor coordinate in pixels
        '''
        alpha, delta = gnomonic_projection(params, ra, dec)
        #alpha = ra - params['ra500']
        #delta = dec - params['dec500']
        return (sensor_center[0] + params['fptrans_a'][0] * alpha + params['fptrans_a'][1] * delta + params['fptrans_a'][2] * alpha**2 + params['fptrans_a'][3] * delta**2 + params['fptrans_a'][4] * alpha * delta,
                sensor_center[1] + params['fptrans_b'][0] * alpha + params['fptrans_b'][1] * delta + params['fptrans_b'][2] * alpha**2 + params['fptrans_b'][3] * delta**2 + params['fptrans_b'][4] * alpha * delta,)
    
    def residuals(self, params):
        ''' Compute residuals for the current match set and given parameters
        '''
        x, y = self.matched_catalog['gwx'], self.matched_catalog['gwy']
        predx, predy = self(params, self.matched_catalog_ref['ra'], self.matched_catalog_ref['dec'])
        deltax, deltay = x-predx, y - predy
        return deltax, deltay
        
    def weighted_residuals(self, params):
        ''' Compute chi2 per star weighting the transformation residuals by measurement errors
        '''
        deltax, deltay = self.residuals(params)
        vx, vy, vxy = self.matched_catalog['vgwx']+0.1**2, self.matched_catalog['vgwy']+0.1**2, self.matched_catalog['vgwxy']
        chi2 = (vx * deltay**2 - 2 * vxy* deltax * deltay + vy * deltax**2) / (vx*vy - vxy**2)
        return chi2
        
    def likelihood(self, params, goods):
        ''' likelihood of the parameters for a selection of stars
        '''
        chi2 = self.weighted_residuals(params)
        return chi2[goods].sum()

    def starting_point(self, wcs):
        ''' Return a starting point for the current image given its wcs
        '''
        start = -np.linalg.inv(wcs.wcs.cd)
        ra0, dec0 = wcs.all_pix2world(np.array([[512], [512]]).T, 0).T
        params = {'ra_center': ra0,
                  'dec_center': dec0,
                  'fptrans_a': jnp.array([start[0, 0], start[0, 1]] + [0.,] * self.n_extra_pars),
                  'fptrans_b': jnp.array([start[1, 0], start[1, 1]] + [0.,] * self.n_extra_pars),
                  }
        return params

    def fit(self, matched_catalog, matched_catalog_ref, params, show=False):
        '''Fit a transformation between two matched catalogs starting from the given point

        Parameters:
        -----------
        
        matched_catalog: catalog providing the gaussian-weighted coordinates
              (gwx, gwy) of objects in the image as well as
              measurement errors
        matched_catalog_ref: catalog of positions on the sphere
        params: pytree, starting point for the transformation parameters

        Returns:
        --------
        bf: pytree, best fit parameters for the transformation
        '''
        self.matched_catalog = matched_catalog
        self.matched_catalog_ref = matched_catalog_ref
        goods = np.ones(len(self.matched_catalog), dtype=bool)
        oldgoods = np.zeros(len(self.matched_catalog), dtype=bool)
        while (oldgoods != goods).any():
            oldgoods = goods.copy()
            bf, losses = jaxfitter.fit_tncg(lambda p: self.likelihood(p, goods), params)
            chi2 = self.weighted_residuals(bf)
            goods = chi2 < (3*np.mean(chi2))
            print(f'{goods.sum()}/{len(goods)} measurements for a chi2/ndof of {chi2[goods].sum()/goods.sum()}')
        if show:
            import matplotlib.pyplot as plt
            plt.figure('loss')
            plt.plot(losses)
        return bf, goods

    def control_plots(self, params, goods=None):
        import matplotlib.pyplot as plt
        deltax, deltay = self.residuals(params)
        chi2 = self.weighted_residuals(params)
        if goods is None:
            goods = np.ones(len(chi2), dtype=bool)
        print(np.std(deltax[goods]), np.std(deltay[goods]))
        
        plt.figure('residuals')
        plt.plot(deltax[goods], deltay[goods], 'o')
        plt.plot(deltax[~goods], deltay[~goods], 'r+')
        plt.xlabel(r'$\Delta x$ [pixels]')
        plt.ylabel(r'$\Delta y$ [pixels]')

        plt.figure('chi2')
        plt.scatter(self.matched_catalog['gwx'][goods], self.matched_catalog['gwy'][goods], c=chi2[goods])
        plt.xlabel('gwx [pixels]')
        plt.xlabel('gwy [pixels]')
        c = plt.colorbar()
        c.set_label(r'$\chi^2$')

if __name__ == '__main__':
    import argparse
    import astropy.io.fits as pyfits
    import astropy.wcs
    import reference_catalog
    parser = argparse.ArgumentParser()
    parser.add_argument('catalog', type=str, help='calibrated.fits', nargs='+')
    parser.add_argument('-s', '--show', action='store_true',
                        help= "Display control plots")
    #parser.add_argument('-c', '--catenate', action='store_true',
    #                    help= "Output a single catalog with filename provided by"
    #                    "output_file. Default behavior is to output a catalog per image next"
    #                    "to the image")
    
    args = parser.parse_args()
    for _f, fname in enumerate(args.catalog):
        basename = fname.replace('_photometric_cat_astrom.npy','')
        print(f'Processing image {basename} ({_f+1}/{len(args.catalog)})')

        with pyfits.open(f'{basename}.fits', memmap=False) as fid:# memmap prevents proper garbage collection
            header = fid[0].header
            image_size = fid[0].data.shape
        image_cat = np.load(f'{basename}_photometric_cat_astrom.npy')
        wcs = astropy.wcs.WCS(f'{basename}_photometric_cat.wcs')

        field = header['MOUNTTARGET']
        reference_cat = reference_catalog.get_gaia_catalog_from_label(field, radius_value=30., row_limit=50000, outputdir="./")

        matched_catalog, matched_catalog_ref = reference_catalog.match_image_and_refcat(image_cat, reference_cat, wcs)

        T = Transfo()
        params = T.starting_point(wcs)
        bestfit, goods = T.fit(matched_catalog, matched_catalog_ref, params)
        
        if args.show:
            import matplotlib.pyplot as plt
            T.control_plots(bestfit, goods)
            plt.show()
        
        
