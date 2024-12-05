# -*- coding: utf-8 -*-
# +
import scipy.optimize as sc
import numpy as np
import matplotlib.pyplot as plt

import time
import astropy.time
import datetime
import skyfield.api
from stardiceonline.tools.config import config

load = skyfield.api.Loader(config['archive.local'])

from stardiceonline.pointing_model.fit_parameters import FitParameters
JULIAN_TRUNCATION = 2400000.5

from stardiceonline.pointing_model.implicit_threading import disable_implicit_threading
disable_implicit_threading()

def mjdnow():
    mjd_now = astropy.time.Time(datetime.datetime.utcnow()).mjd
    return mjd_now

def on_side(ha, dec, east):

    ''' Return the pointing so that the table is east of the pillar if east is true and west of the pillar otherwise

    Parameters:
    -----------
    ha: scalar or ndarray hour angle in decimal degrees
    dec: scalar or ndarray declination in decimal degrees
    east: scalar or ndarray boolean wether the pointing should start east (ha<90) or west (ha>90) of the pillar.
    
    All parameters must have same length
    Returns:
    --------
    ha, dec: same type as the input ha, dec
    '''
    def move_east(ha, dec):
        return ha - 180, 180 - dec
    def move_west(ha, dec):
        return ha + 180, 180 - dec
    
    ha, dec = flip_side(ha, dec)
    if np.isscalar(ha):
        if east and (ha > 90):
            ha, dec = move_east(ha, dec)
        elif not east and (ha < 90):
            ha, dec = move_west(ha, dec)
    else:    
        not_east_yet = east & (ha > 90)
        not_west_yet = ~east & (ha <90)
        ha[not_east_yet], dec[not_east_yet] = move_east(ha[not_east_yet], dec[not_east_yet])
        ha[not_west_yet], dec[not_west_yet] = move_west(ha[not_west_yet], dec[not_west_yet])
    return ha, dec

def flip_side(ha, dec):
    ''' Flip a pointing so that 0 <= ha < 180 (and -90<dec<270)
    
    Parameters:
    -----------
    ha, dec: scalars or array of same size providing hour angle and declination in decimal degrees

    Return:
    -------
    ha, dec: same as input but ensuring  0 <= ha < 180 (and -90<dec<270)
    '''
    ha = ha % 360
    if np.isscalar(ha):
        if ha > 180:
            ha -= 180
            dec = 180 - dec
    else:
        c = ha > 180
        ha[c] -= 180
        dec[c] = 180 - dec[c]
    dec = (dec + 90) % 360 - 90
    return ha, dec

def no_side(ra, dec):
    ''' Transform back the celestial coordinates to the normal convention (0<ra<360, -90<dec<90)

    '''
    ra = ra % 360
    dec = (dec + 180) % 360 - 180    
    if np.isscalar(ra):
        if dec > 90:
            ra -= 180
            dec = 180 - dec
    dec = (dec + 180) % 360 - 180
    ra = ra % 360
    return ra, dec

def same_side(ha1, ha2, dec2):
    ''' Flip the second set of coordinates to be on the same side than the first set
    '''
    c = (ha2 - ha1) > 1
    ha2[c] -= 180
    dec2[c] = 180 - dec2[c]

    c = ha2-ha1 < -1
    ha2[c] += 180
    dec2[c] = 180 - dec2[c]
    return ha2, dec2

def great_circle_distance(ha0, dec0, ha1, dec1):
    _ha0, _dec0, _ha1, _dec1 = np.radians([ha0, dec0, ha1, dec1])
    return np.degrees(np.arccos(np.sin(_dec0)*np.sin(_dec1) + np.cos(_dec0)*np.cos(_dec1)*np.cos(_ha0 - _ha1)))

# +
class PointingModel(object):
    '''Pointing model for the OHP mount

    This class provides transformations between 4 different sets of
    coordinates for the apparent position of the object in the sky
    sphere. Unless otherwise specified all angles are expressed in
    decimal degrees.
    
    icrs: Right ascension and declination of a night sky object in the ICRS frame

    radec: Apparent right ascension and declination of the object in
           the sky above the observatory at a given date (transformation from
           icrs is provided by the skyfield library)

    hadec: same position as radec (apparent) but as apparent hour angle and declination (relates to radec through sidereal time)
    altaz: same position as hadec and radec but in (altitude, azimuth) coordinates

    deltatau: the mount axes coordinates in decimal degrees

    '''
    def __init__(self, path_to_params=None):
        planets = load('de421.bsp')
        earth = planets['earth']
        #self.OHP_latitude = 43.932778
        #self.OHP_longitude = 5.712778
        self.latitude = 43.932630 # According to googlemap satellite view of the StarDICE dome
        self.longitude = 5.713622
        self.elevation = 660 # According to google earth elevation of the site is 557m the mount is slightly higher we round to 660m
        self.site = earth + skyfield.api.Topos(latitude_degrees = self.latitude, longitude_degrees = self.longitude, elevation_m=self.elevation)
        self.ts = load.timescale()
        self.params = FitParameters([('a', 4), ('b', 5)])
        self.cphi = np.cos(np.radians(self.latitude))
        self.sphi = np.sin(np.radians(self.latitude))
        if path_to_params is not None:
            model_params = np.load(path_to_params)            
            self.params.full[:] = model_params

    def save(self, path_to_params):
        np.save(path_to_params, self.params.full)
        
    def __call__(self, delta, tau):
        ''' Return the pointing model hour angle and declination given axis position

        Parameters
        ----------
        Delta: declination axis rotation in decimal degrees
        tau: polar axis rotation in decimal degrees

        Returns
        -------
        ha: pointing vector hour angle in decimal degrees
        dec: pointing vector declination in decimal degrees
        '''
        a = self.params['a'].full
        b = self.params['b'].full
        _tau = np.radians(tau)
        _delta = np.radians(delta)
        st = np.sin(_tau)
        ct = np.cos(_tau)
        cd = np.cos(_delta)
        sd = np.sin(_delta)
        td = sd/cd
        dec = _delta - a[0] + a[1] * ct + a[2] * st + a[3] * (self.sphi * cd - self.cphi * sd * ct)
        ha = (_tau - b[0]
              + (a[1] * st - a[2] * ct) * td
              - b[1]/cd
              + b[2]  * td
              - a[3] * self.cphi * st/cd
              - b[3] * (self.sphi* td + cd*ct)
              - _tau * b[4])
        
        return np.degrees(ha), np.degrees(dec)

    def sidereal_time(self, mjd=None):
        ''' Return the sidereal time for the mount position
        
        Parmeters:
        ----------
        mjd: modified julian date (if none, take the current time)

        Returns:
        --------
        LST: sidereal time in decimal degrees
        '''
        disable_implicit_threading()
        if mjd is None:
            mjd = mjdnow()
        time_jd = self.ts.ut1_jd(mjd + JULIAN_TRUNCATION)
        LST = (time_jd.gast * 360. / 24. + self.longitude)
        return LST
    
    def radec_to_hadec(self, ra, dec, mjd=None):
        ''' Convert apparent position from radec to hadec coordinates
        
        Parameters
        ----------
        ra: right ascension in decimal degrees
        dec: declination in decimal degrees
        mjd: modified julian date
        '''
        LST = self.sidereal_time(mjd)
        ha = (LST - ra)%360
        return ha, dec

    def hadec_to_radec(self, ha, dec, mjd=None):
        ''' Convert apparent position from hadec to radec coordinates
        
        Parameters
        ----------
        ha: hour angle in decimal degrees
        dec: declination in decimal degrees
        mjd: modified julian date
        '''
        LST = self.sidereal_time(mjd)
        ra = (LST - ha)%360
        return ra, dec

    def hadec_to_altaz(self, ha, dec):
        ''' Convert apparent position from hadec to altaz coordinates

        Parameters
        ----------
        ha: hour angle in decimal degrees
        dec: declination in decimal degrees
        Returns
        -------
        alt: altitude in decimal degrees
        az: azimuth in decimal degrees
        '''
        _ha, _dec = np.radians(ha), np.radians(dec)
        alt = np.arcsin(np.sin(_dec)*self.sphi+np.cos(_dec)*self.cphi*np.cos(_ha))
        A = np.arccos((np.sin(_dec) - np.sin(alt)*self.sphi)/(np.cos(alt)*self.cphi))
        az = np.select([np.sin(_ha) < 0], [np.degrees(A)], 360 - np.degrees(A))
        return np.array([np.degrees(alt), az])
    
    def altaz_to_hadec(self, alt, az):
        ''' Convert apparent position from altaz to hadec coordinates using current sidereal time.

        Parameters
        ----------
        alt: altitude in decimal degrees
        az: azimuth in decimal degrees
        Returns
        -------
        ha: hour angle in decimal degrees
        dec: declination in decimal degrees
        '''
        _alt, _az = np.radians(alt), np.radians(az)
        A = np.arctan2(-np.sin(_az) * np.cos(_alt),
                       -np.cos(_az) * self.sphi * np.cos(_alt) + np.sin(_alt) * self.cphi)
        ha = np.select([A > 0], [np.degrees(A)], np.degrees(A) + 360) % 360
        dec = np.arcsin(self.sphi * np.sin(_alt) + self.cphi * np.cos(_alt) * np.cos(_az))
        return np.array([ha, np.degrees(dec)])

    def train(self, grid_data):
        ''' fit pointing model parameters given a set of observed position with astrometrical solution
        RA,DEC field centers must be in J2000
        
        Parameters
        ----------
        grid_data: record array providing the following columns:
           - mra, mdec: mount target position in decimal degrees
           - ara, adec: astrometric solution in decimal degrees **J2000**
           - mjd: modified julian date of the observation
        '''
        tau, delta = grid_data['tau'], grid_data['delta'] #self.radec_to_hadec(grid_data['mra'], grid_data['mdec'], grid_data['mjd'])
        ara_apparent, adec_apparent = np.array([self.radec_J2000_to_radec_apparent(entry['ara'], entry['adec'], entry['mjd']) for entry in grid_data]).T
        aha, adec = self.radec_to_hadec(ara_apparent, adec_apparent, grid_data['MOUNTMJD'])
        
        def dist(p):
            self.params.free = p
            modelha, modeldec = self(delta, tau)
            distance = great_circle_distance(aha, adec, modelha, modeldec)
            return distance
        
        def error(p):
            distance = dist(p)
            return np.sum(distance**2)

        # fit
        x = sc.fmin_cg(error, self.params.free, full_output = True, maxiter=3000)
        p_best = np.copy(x[0])
        d = dist(p_best)
        modelha, modeldec = self(delta, tau)

        # covariance matrix computation
        W = np.diag(2*60*np.ones_like(d))**2  # 1/2 arcmin uncertainty
        epsilon = np.abs(1e-5 * self.params.free)
        epsilon[epsilon==0] = 1e-5
        J = np.zeros((d.size, epsilon.size))
        for ip, p in enumerate(self.params.free):
            p_temp = np.copy(p_best)
            p_temp[ip] += epsilon[ip]
            self.params.free = p_temp
            modelha_temp, modeldec_temp =  self(delta, tau)
            J_temp = dist(p_temp)/epsilon[ip]
            J_temp[np.isnan(J_temp)] = 0
            J[:,ip] = np.copy(J_temp)
        invcov = J.T @ W @ J
        cov = np.linalg.inv(invcov)
        self.params.free = p_best
        self.params.err = np.zeros_like(p_best)
        self.params.cov = cov
        for ip in range(len(p_best)):
            self.params.err[ip] = np.sqrt(cov[ip,ip])
        print("Reduced chisquare", (d @ W @ d)/(len(tau)-len(self.params.free)))
        print(f'root mean square distance: {np.sqrt((d**2).mean())*3600} arcsec')

        return tau, delta, aha, adec, modelha, modeldec, d

    def inverse_model(self, ha, dec):
        ''' Return axis positions given a required pointing vector

        Parameters
        ----------
        ha: pointing vector hour angle in decimal degrees
        dec: pointing vector declination in decimal degrees

        Returns
        -------
        Delta: declination axis rotation in decimal degrees
        tau: polar axis rotation in decimal degrees
        '''
        def func_to_solve(x):
            delta, tau = x[:len(x)//2], x[len(x)//2:]
            _ha, _dec = self(delta, tau)
            return np.hstack([_ha, _dec]) - np.hstack([ha, dec])
        
        x = sc.fsolve(func_to_solve, np.array([dec, ha]))
        delta, tau = x[:len(x)//2], x[len(x)//2:]
        return delta, tau

    def radec_to_deltatau(self, ra, dec, mjd=None, east=None):
        ''' Convenience fonction, apply the inverse model directly to radec coordinates

        Parameters
        ----------
        ra: right ascension in decimal degrees
        dec: declination in decimal degrees
        mjd: Modified julian date for the conversion to ha dec, if None use the current time

        Returns
        -------
        delta: declination axis rotation in decimal degrees
        tau: polar axis rotation in decimal degrees
        '''
        if mjd is None:
            mjd = mjdnow()
        ha, dec = self.radec_to_hadec(ra, dec, mjd)
        if east is None:
            ha, dec = flip_side(ha, dec)
        else:
            ha, dec = on_side(ha, dec, east)
        return self.inverse_model(ha, dec)

    
    def deltatau_to_wcs(self, delta, tau, mjd=None):
        ''' Convenience function, return the predicted wcs associated to mount coordinate

        This requires the pixel scale and camera orientation to be known

        Parameters
        ----------
        delta: mount polar axis coordinate in decimal degrees
        tau: mount declination axis coordinate in decimal degrees
        mjd: Modified julian date for the conversion to ha dec, if None use the current time
        
        Returns
        -------
        wcs: astropy.wcs object
        '''
        import astropy.wcs as wcs
        ha, dec = self(delta, tau)
        ra, dec = self.hadec_to_radec(ha, dec, mjd)
        ra, dec = no_side(ra, dec)
        w = wcs.WCS()
        w.wcs.ctype= ['RA---TAN--', 'DEC--TAN--']
        w.wcs.crval = np.array([ra, dec])
        w.wcs.crpix = np.array(self.field_center)
        flip = 1 if delta > 90 else -1
        w.wcs.cd = flip * self.pixel_scale * np.array([[np.cos(self.camera_angle),  -np.sin(self.camera_angle)],
                                                       [np.sin(self.camera_angle),  np.cos(self.camera_angle)]])
        return w

        
    def radec_J2000_to_radec_apparent(self, ra_J2000, dec_J2000, mjd=None, temperature_C=10, pressure_mbar=1004):
        """ Convert (ra,dec) in degrees and J2000 into apparent (ra,dec) using skyfield.
        It includes the equinox precession and atmospheric refraction.
        """
        if mjd is None:
            mjd = mjdnow()
        ### Skyfield corrections
        _ra = skyfield.units.Angle(degrees=ra_J2000)
        _dec = skyfield.units.Angle(degrees=dec_J2000)
        plate_center = skyfield.starlib.Star(ra=_ra, dec=_dec, epoch=self.ts.J2000)
        observer = self.site.at(self.ts.ut1_jd(mjd + JULIAN_TRUNCATION))
        obs = observer.observe(plate_center)
        alt, az, distance = obs.apparent().altaz(temperature_C=temperature_C, pressure_mbar=pressure_mbar)
        #print(alt.degrees, az.degrees)
        ### Récuperer les ra,dec correspondants
        ha_app, dec_app = self.altaz_to_hadec(alt.degrees, az.degrees)
        ra_apparent, dec_apparent = self.hadec_to_radec(ha_app, dec_app, mjd)
        #star_pos_corr = observer.from_altaz(alt_degrees=alt.degrees, az_degrees=az.degrees)
        #ra_apparent, dec_apparent, _ = star_pos_corr.radec()
        #ra_apparent = ra_apparent._degrees
        #dec_apparent = dec_apparent.degrees
        return ra_apparent, dec_apparent
    
    def plot_parameters(self):
        x = np.arange(len(self.params.free))
        fig = plt.figure()
        if hasattr(self.params, 'err'):
            plt.errorbar(x, self.params.free, yerr=self.params.err, linestyle='none', marker='+')
        else:
            plt.plot(x, self.params.free, linestyle='none', marker='+')
        plt.grid()
        xticks = []
        for key in ['a', 'b']:
            for ikey in range(len(self.params[key].free)):
                xticks.append(f'{key}[{ikey}]') 
        plt.xticks(x, xticks)
        plt.show()
    
    def plot_parameter_covariance(self):
        if hasattr(self.params, 'cov'):
            fig=plt.figure(figsize=(8,6))
            maxi = np.max(np.abs(self.params.cov))
            plt.imshow(self.params.cov,origin="lower",cmap="bwr",vmin=-maxi,vmax=maxi)
            plt.colorbar()
            plt.show()
        else:
            print('No covariance matrix attached to parameters.')
    

    
class PointingModel_Extended(PointingModel):
    '''Pointing model for the OHP mount

    This class provides transformations between 4 different sets of
    coordinates for the apparent position of the object in the sky
    sphere. Unless otherwise specified all angles are expressed in
    decimal degrees.
    
    icrs: Right ascension and declination of a night sky object in the ICRS frame

    radec: Apparent right ascension and declination of the object in
           the sky above the observatory at a given date (transformation from
           icrs is provided by the skyfield library)

    hadec: same position as radec (apparent) but as apparent hour angle and declination (relates to radec through sidereal time)
    altaz: same position as hadec and radec but in (altitude, azimuth) coordinates

    deltatau: the mount axes coordinates in decimal degrees

    '''
    def __init__(self, path_to_params=None):
        PointingModel.__init__(self, path_to_params=None)
        self.params = FitParameters([('a', 10), ('b', 9)])
        if path_to_params is not None:
            model_params = np.load(path_to_params)            
            self.params.full[:] = model_params

    def __call__(self, delta, tau):
        ''' Return the pointing model hour angle and declination given axis position

        Parameters
        ----------
        Delta: declination axis rotation in decimal degrees
        tau: polar axis rotation in decimal degrees

        Returns
        -------
        ha: pointing vector hour angle in decimal degrees
        dec: pointing vector declination in decimal degrees
        '''
        a = self.params['a'].full
        b = self.params['b'].full
        _tau = np.radians(tau)
        _delta = np.radians(delta)
        st = np.sin(_tau)
        ct = np.cos(_tau)
        cd = np.cos(_delta)
        sd = np.sin(_delta)
        td = sd/cd
        # weight torque on DEC axis
        torque_dec = np.cos(_delta-a[8])*self.sphi - ct * self.cphi * np.sin(_delta-a[8]) 
        # weight torque on HA axis
        torque_ha = ct * self.cphi
        # DEC to cancel torque on DEC axis
        delta_null_torque = np.arctan2(self.sphi/self.cphi,ct) + a[8]
        # Original Bui 2003 model
        dec = _delta - a[0] + a[1] * ct + a[2] * st + a[3] * torque_dec
        ha = (_tau - b[0]
              + (a[1] * st - a[2] * ct) * td
              - b[1] / cd
              + b[2] * td
              - a[3] * self.cphi * st / cd
              - b[3] * (self.sphi * td + cd * ct)
              - _tau * b[4])
        # Extensions to reduce residuals after november 2021 fits
        dec += a[6] * np.tanh((1+a[9])*(_delta-delta_null_torque))
        #dec += a[6]*(torque_norm-a[5]) + a[7]*np.sign(torque_norm-a[5])
        #dec += a[4]*(torque_norm-a[5])**2  + a[6]*torque_norm
        dec += a[4]*torque_dec**2  + a[5]*torque_dec  # weird... but reduce residuals... a[3] interplays with ha residuals but not a[5] 
        #dec += a[6]*np.sign(torque_dec)*ct  # clonk ?
        #dec += a[7]*np.sign(_delta - delta_null_torque - a[9])*ct
        dec += a[7]*st**2  # to keep but why ?
        ha += b[6] * np.tanh((1+b[7])*(_tau-np.pi/2-b[8])) # np.pi/2
        # ha += b[5]*(_tau-b[6])**2 
        #ha += b[7]*np.sign(_tau-np.pi/2)
        ha += b[5] * torque_ha  # weight torque on HA axis
        #ha += b[6] * np.sign(_tau-np.pi/2)  # clonk ?
        return np.degrees(ha), np.degrees(dec)

    
class PointingModel_Pal2015(PointingModel):
    '''Pointing model for the OHP mount from Pal 2015 arxiv:1507:05469

    This class provides transformations between 4 different sets of
    coordinates for the apparent position of the object in the sky
    sphere. Unless otherwise specified all angles are expressed in
    decimal degrees.
    
    icrs: Right ascension and declination of a night sky object in the ICRS frame

    radec: Apparent right ascension and declination of the object in
           the sky above the observatory at a given date (transformation from
           icrs is provided by the skyfield library)

    hadec: same position as radec (apparent) but as apparent hour angle and declination (relates to radec through sidereal time)
    altaz: same position as hadec and radec but in (altitude, azimuth) coordinates

    deltatau: the mount axes coordinates in decimal degrees

    '''
    def __init__(self, Lmax=2, path_to_params=None):
        PointingModel.__init__(self, path_to_params=None)
        npar = np.sum(2*np.arange(Lmax+1)+1)
        self.params = FitParameters([('a', npar), ('b', npar), ('c', npar), ('d', npar), 
                                     ('e', npar), ('i', npar), ('r', 1)]) # , ('gamma', 1), ('flex', 2)
        if Lmax > 0:
            self.params['i'].fix(2, 0)
            self.params['b'].fix(3, 0)
        if Lmax > 1:
            self.params['i'].fix(5, 0)
            self.params['i'].fix(6, 0)
            self.params['i'].fix(7, 0)
            self.params['a'].fix(7, 0)
            self.params['a'].fix(8, 0)
            self.params['b'].fix(8, 0)
        self.Lmax = Lmax
        if path_to_params is not None:
            model_params = np.load(path_to_params)            
            self.params.full[:] = model_params
    
    def __call__(self, delta, tau):
        ''' Return the pointing model hour angle and declination given axis position

        Parameters
        ----------
        Delta: declination axis rotation in decimal degrees
        tau: polar axis rotation in decimal degrees

        Returns
        -------
        ha: pointing vector hour angle in decimal degrees
        dec: pointing vector declination in decimal degrees
        '''
        r = self.params['r'].full
        # f = self.params['flex'].full
        # g = self.params['gamma'].full
        a = self.params['a'].full
        b = self.params['b'].full
        c = self.params['c'].full
        d = self.params['d'].full
        e = self.params['e'].full
        i = self.params['i'].full
        params = []
        for ipar, p in enumerate([a,b,c,d,e,i]):
            params.append([[p[0]]])
            if self.Lmax > 0:
                params[ipar].append([p[1], p[2], p[3]])
            if self.Lmax > 1:
                params[ipar].append([p[4], p[5], p[6], p[7], p[8]])
        _tau = np.radians(tau)
        _delta = np.radians(delta)
        
        st = np.sin(_tau)
        ct = np.cos(_tau)
        cd = np.cos(_delta)
        sd = np.sin(_delta)
        td = sd/cd

        # Original Pal 2015 model
        pointing  = np.array([ct*cd, st*cd, sd])
        zero = np.zeros_like(ct)
        p1 = np.array([zero, -sd, cd*st])
        p2 = np.array([sd, zero, -cd*ct])
        p3 = np.array([-cd*st,  cd*ct, zero])
        p4 = np.array([ sd*st, -sd*ct, zero])
        p5 = np.array([ sd*ct,  sd*st, -cd])
        p6 = np.array([-st,     ct,    zero])
        ps = [p1, p2, p3, p4, p5, p6]
        Ys = [[1]]
        if self.Lmax > 0:
            Y11 = cd * ct
            Y10 = sd
            Y1_1 = cd * st
            Ys.append([Y1_1, Y10, Y11])
        if self.Lmax > 1:
            Y22 = cd * cd * np.cos(2*_tau)
            Y21 = cd * sd * ct
            Y20 = 3 * sd * sd - 1
            Y2_1 = cd * sd * st
            Y2_2 = cd * cd * np.sin(2*_tau)
            Ys.append([Y2_2, Y2_1, Y20, Y21, Y22])
            
        # Extensions coming from the Buie 2003 paper 
        # (see stardice/docs/ohp_mount_refurbishment/torques.nb for their derivation)
        # p_gamma = g[0] * np.array([-ct * ct * sd + sd * st * st, -2 * ct * sd * st, cd * ct ])
        # p_l = f[1] * np.array([-cd * cd * ct * st - sd * st * self.sphi, cd * cd * ct * ct + ct * sd * self.sphi, zero])
        # p_e = f[0] * np.array([ ct * ct * self.cphi * sd * sd + self.cphi * st * st - cd * ct * sd * self.sphi,
        #                        -ct * self.cphi * st + ct * self.cphi * sd * sd * st - cd * sd * st * self.sphi,
        #                        -cd * ct * self.cphi * sd + cd * cd * self.sphi])
        p_r = r[0] * _tau * np.array([cd * st, cd * ct, zero])
        # pointing += p_e + p_l + p_gamma
        pointing += p_r
        
        for k in range(len(ps)):
            for L in range(self.Lmax+1):
                for m in range(0,2*L+1):
                    pointing += params[k][L][m]*Ys[L][m]*ps[k] 
        # convert to (ha,dec)            
        pointing /= np.linalg.norm(pointing, axis=0)
        modeldec = np.degrees(np.arcsin(pointing[2]))
        modelha = np.degrees(np.arctan2(pointing[1], pointing[0]))
        modelha, modeldec = flip_side(modelha, modeldec)
        return modelha, modeldec

    def plot_parameters(self):
        x = np.arange(len(self.params.free))
        fig = plt.figure(figsize=(12,6))
        plt.errorbar(x, self.params.free, yerr=self.params.err, linestyle='none', marker='+')
        plt.grid()
        xticks = []
        for key in ['r', 'a', 'b', 'c', 'd', 'e', 'i']: # 'gamma', 'flex', 
            for ikey in range(len(self.params[key].free)):
                xticks.append(f'{key}[{ikey}]') 
        plt.xticks(x, xticks)
        plt.show()



# -

def refraction(alt):
    ''' Compute the refraction according to Bennett formula
    
    Parameters
    ----------
    alt: Apparent altitude in degrees
    
    Returns
    -------
    R: refraction in arcmin
    '''
    return 1/np.tan(np.radians(alt + 7.31/(alt+4.4)))
