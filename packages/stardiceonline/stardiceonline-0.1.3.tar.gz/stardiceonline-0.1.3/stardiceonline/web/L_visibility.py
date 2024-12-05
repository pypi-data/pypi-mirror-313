# -*- coding: utf-8 -*-

"""
===================================================================
Determining and plotting the altitude/azimuth of a celestial object
===================================================================

Used for observations at OHP
Arguments order : object name, date (year-month-day), time (hour:min:sec)
If date and time are not given, the code take the actual time (with daytime.now)

If you ask to observe an object between midnight and 8am, the code considers
that "midnight" is today date (or the date you gave), but between 8 and midnight
it considers that you want to observe the object during the coming night, and
so "midnight" is tomorrow date (or the date after the one you gave).

Inspired by Erik Tollerud and Kelle Cruz example
"""

import numpy as np
import matplotlib.pyplot as plt
import astropy.visualization
import astropy.units 
import astropy.time 
import astropy.coordinates 
import matplotlib.dates 
import datetime
import sys
import os
import stardiceonline.tools.orgfiles
import stardiceonline.tools.metadatamanager



# For the latter, use a nicer set of plot
# parameters and set up support for plotting/converting quantities.
plt.style.use(astropy.visualization.astropy_mpl_style)
astropy.visualization.time_support(scale="utc", format="iso")


OHP_height = 650 * astropy.units.m
#OHP_lon = astropy.coordinates.Longitude('5d42m44s')
#OHP_lat = astropy.coordinates.Latitude('43d55m54s')
OHP_lon = astropy.coordinates.Longitude('5d42m48s') #- From IRIS
OHP_lat = astropy.coordinates.Latitude('43d55m51s') #- From IRIS
OHP_EARTH_LOCATION = astropy.coordinates.EarthLocation.from_geodetic(lat=OHP_lat, lon=OHP_lon, height=OHP_height)


#- utilities

#- For visibility 
def get_ohp_observation_frame(times):
    # Use `astropy.coordinates.astropy.coordinates.EarthLocation` to provide the location of OHP
    # and set the time to the date you want:
    # OHP : alt = 650m, lon = , lat = 43°55'54''
    return astropy.coordinates.AltAz(obstime=times, location=OHP_EARTH_LOCATION)

def get_ohp_midnight_from_dateobs(dateobs):
    """
    Before 8h00 UTC, considers that we are still during the observing night.
    After that, gives the observability for the night after (midnight is 0h of next day)
    """

    if dateobs == "now":
        obstime = datetime.datetime.utcnow()
    else:
        try:
            if "T" in dateobs:
                obstime = datetime.datetime.strptime(dateobs, "%Y-%m-%dT%H:%M:%S").astimezone(datetime.timezone.utc)
            else:
                obstime = datetime.datetime.strptime(dateobs, "%Y-%m-%d").astimezone(datetime.timezone.utc)
        except ValueError:
            raise ValueError("Wrong datetime format: use %Y-%m-%dT%H:%M:%S or %Y-%m-%d.")
    if 0 <= obstime.hour < 8:
        ohp_midnight = obstime.replace(obstime.year, obstime.month, obstime.day, 0, 0, 0, 0)
    else:
        ohp_midnight = obstime + datetime.timedelta(days=1)
        ohp_midnight = astropy.time.Time(ohp_midnight, scale='utc')
        ohp_midnight.format = "iso"
        obstime = astropy.time.Time(obstime, scale='utc')
    return obstime, ohp_midnight

class Visibility(object):
    """
    A class to provide visibility information for OHP    
    """

    def __init__(self, dateobs="now",
                 n_obs=300,
                 calspec=True,
                 moon=True,
                 planet=True,
                 mag_max=14,
                 delta_t=10):
        """
        calspec: loads the calspec stars
        moon : loads the moon
        planet : loads the other planets (including Sun)
        mag_max : V mag cut on the calspec data
        delta_t : +- interval around midnight
        
        """
        self.height = OHP_height
        self.lon = OHP_lon
        self.lat = OHP_lat
        self.earth_location = OHP_EARTH_LOCATION

        self.dateobs = dateobs
        self.n_obs = n_obs

        self.delta_t = delta_t
        self.set_time_and_frame()
        self.load_calspec(calspec=calspec, mag_max=mag_max)

        self.load_solar_system('Sun')
        if moon:
            self.load_solar_system('Moon')
        if planet:
            for name in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
                self.load_solar_system(name)

            
    def load_calspec(self, calspec=True, mag_max=14):
        if calspec:
            manager = stardiceonline.tools.metadatamanager.MetaDataManager()
            targets, _ = stardiceonline.tools.orgfiles.fromorg(manager.get_data('visibility.org', 'http://supernovae.in2p3.fr/stardice/stardiceot1/visibility.org'))            
            self.nt_calspec_full = targets
            
            i_ok = self.nt_calspec_full['V'] < mag_max
            self.nt_calspec = self.nt_calspec_full[i_ok]
        else:
            self.nt_calspec_full = None
            self.nt_calspec = None

    def find_calspec(self, name):
        nt = None
        if self.nt_calspec is not None:
            if name in self.nt_calspec['SIMBAD_NAME']:
                nt = self.nt_calspec[self.nt_calspec['SIMBAD_NAME'] == name][0]        
        return nt

    
    def set_time_and_frame(self):
        """
        Get the observing times and observing frames 
        """
        obstime, midnight_ohp = get_ohp_midnight_from_dateobs(self.dateobs)
        self.midnight_ohp = midnight_ohp
        self.delta_midnight = midnight_ohp + np.linspace(-self.delta_t, self.delta_t, self.n_obs) * astropy.units.hour
        self.observing_frame = astropy.coordinates.AltAz(obstime=self.delta_midnight, location=self.earth_location)


    def load_solar_system(self, name):
        d_mag = {"Mars":-2.3, "Venus":-4.6, "Jupiter":-2.7, "Saturn":-0.4, "Mercury":-2.2, "Sun":-26.8, "Moon":-12.7}
        if name == "Sun":
            f_load = astropy.coordinates.get_sun
        elif name == "Moon":
            f_load = astropy.coordinates.get_moon
        else:
            f_load = lambda time: astropy.coordinates.get_body(name, time)
        setattr(self, name+"_altaz", f_load(self.delta_midnight).transform_to(self.observing_frame))
        setattr(self, name+"_mag", d_mag[name])
                    
            
    def get_target(self, name):
        """
        Retuns the dictionary with name, magnitude and altaz astropy object
        """
        if name in ["Mars", "Venus", "Jupiter", "Saturn", "Mercury", "Sun", "Moon"]:
            d_target = {"name": name, "altaz": getattr(self, name+"_altaz"), 'mag':getattr(self, name+"_mag")}
        else:
            nt = self.find_calspec(name)
            if nt is not None:
                d_target = {"name": nt['SIMBAD_NAME'],
                            "altaz": astropy.coordinates.SkyCoord(ra=nt['RA'], dec=nt['DEC'], unit='deg').transform_to(self.observing_frame),
                            'mag':nt['V']}
            else:
                d_target = {"name": '',
                            "altaz": [],
                            'mag':nt['V']}
        return d_target
    

def get_sunrise(fake_self):
    """
    Attention, pas meilleure précision que n_obs
    """
    i_0 = int(fake_self.n_obs/2)
    alt = fake_self.Sun_altaz.alt[i_0:-1] # Sunrise happens at the end of the night
    
    i_sunrise = np.argmin(np.abs(alt)) + i_0 # Bellow the horizon alt < 0
    i_12 = np.argmin(np.abs(alt + 12 * astropy.units.deg)) + i_0 #- when the sun is at -12
    i_18 = np.argmin(np.abs(alt + 18 * astropy.units.deg)) + i_0#- when the sun is at -18

    return fake_self.delta_midnight[i_sunrise].to_datetime(), fake_self.delta_midnight[i_12].to_datetime(), fake_self.delta_midnight[i_18].to_datetime()

def get_sunset(fake_self):
    """
    Attention, pas meilleure précision que n_obs
    """
    i_0 = int(fake_self.n_obs/2)
    alt = fake_self.Sun_altaz.alt[0:i_0] # Sunrise happens at the end of the night
    
    i_sunset = np.argmin(np.abs(alt)) 
    i_12 = np.argmin(np.abs(alt + 12 * astropy.units.deg))#- when the sun is at -12
    i_18 = np.argmin(np.abs(alt + 18 * astropy.units.deg))#- when the sun is at -18

    return fake_self.delta_midnight[i_sunset].to_datetime(), fake_self.delta_midnight[i_12].to_datetime(), fake_self.delta_midnight[i_18].to_datetime()


    


##----- Somewhat useful plot tricks
MARKERS    = ["+","v", "o","^", "<", ">", "1", "2", "3","4","s","p","*","D", "h"]
LINESTYLES = ["--", "-.", ":", "-"]
COLORS     = ["r", "g", "b", "m", "k"]

def get_color(i, colormap='gray', n_tot=30):
    cmap = plt.get_cmap(colormap)
    return cmap(i/n_tot)

def get_marker_string(i_c):
    color = COLORS[i_c % len(COLORS)]
    marker = MARKERS[(i_c//len(COLORS)) % len(MARKERS)] # int division: 2/3 == 0 
    return marker

def get_color_string(i_c):
    color = COLORS[i_c % len(COLORS)]
    marker = MARKERS[(i_c//len(COLORS)) % len(MARKERS)] # int division: 2/3 == 0 
    return color

def get_style_string(i_c):
    color = COLORS[i_c % len(COLORS)]
    marker = MARKERS[(i_c//len(COLORS)) % len(MARKERS)] # int division: 2/3 == 0 
    return color+marker


def get_linestyle_string(i_c):
    color = COLORS[i_c % len(COLORS)]
    linestyle = LINESTYLES[(i_c//len(COLORS)) % len(LINESTYLES)] # int division: 2/3 == 0 
    return linestyle

def get_linestyle_color_string(i_c):
    color = COLORS[i_c % len(COLORS)]
    linestyle = LINESTYLES[(i_c//len(COLORS)) % len(LINESTYLES)] # int division: 2/3 == 0 
    return color

    
