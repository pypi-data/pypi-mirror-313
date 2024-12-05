from getCalspec import is_calspec, Calspec
import astropy.io
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
from astropy import units as units
from astroquery.gaia import Gaia
import os
from stardiceonline.tools import match, config
import numpy as np

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


def is_simbad(target_label):
    """
    Check if a target label is present in the Simbad astronomical database.
    This function queries the Simbad astronomical database to check if a target with the specified label is present.
    It returns True if the target is found in Simbad and False otherwise.

    Args:
        target_label (str): The label or name of the target to check in the Simbad database.

    Returns:
        bool: True if the target is found in Simbad, False otherwise.

    Example:
        To check if a target label is present in the Simbad database:
        >>> is_present_in_simbad = is_simbad("M42")
    """
    return bool(Simbad.query_object(target_label))

def get_radec_from_label(target_label):    
    """Get radec coordinates by requesting Simbad from target labelimage

    Args:
        target_label (str): Label of the target

    Returns:
        ra_target, dec_target: Coordinates of the target in degrees.
    """

    if is_calspec(target_label):
        target_label = Calspec(target_label).query['Simbad_Name'].values[0]

    elif is_simbad(target_label):
        pass

    else: 
        raise ValueError(f"{target_label} is neither in Calspec or Simbad catalog.")

    simbad_query = Simbad.query_object(target_label)
    coord_simbad = f"{simbad_query['RA'][0]} {simbad_query['DEC'][0]}"
    radec_target = SkyCoord(coord_simbad, unit=(units.hourangle, units.deg))
    ra_target, dec_target = no_side(radec_target.ra.value, radec_target.dec.value)
    return ra_target, dec_target

def get_gaia_catalog_from_label(target_label, radius_value=25., row_limit=20000, outputdir=None):
    """Requests from Gaia a catalog of positions of stars in a cone centered on the target and a given radius value

    Args:
        target_label (string, optional): Label of the target.
        radius_value (float, optional): Radius of the cone centered on the target position. Radius is given in arcmin. Defaults to 25.
        row_limit (int, optional): Maximum limits of rows that the output catalog will contain. Defaults to 20000.
        outputdir (str, optional): Output directory at which the output astropy table will be saved. Defaults to "/data/STARDICE/spice_analysis/gaia_catalogs".

    Returns:
        gaia_cat (astropy.table.table.Table) : Gaia catalogs that contains informations about all the stars in a fiel of a cone centered on the target label coordinates, with a given radius.
        (ra_target, dec_target) ()
    """
    if outputdir is None:
        outputdir = os.path.join(config.config['archive.local'], 'gaia')
    savepath = os.path.join(outputdir, f"gaia_positions_{''.join(target_label.upper().split())}.dat")
    if os.path.isfile(savepath):
        gaia_cat = astropy.io.ascii.read(savepath)
    else:
        ra_target, dec_target = get_radec_from_label(target_label)
        Gaia.ROW_LIMIT = row_limit  # Ensure the default row limit.
        coord = SkyCoord(ra=ra_target, dec=dec_target, unit=(units.degree, units.degree), frame='icrs')
        radius = radius_value * units.arcmin
        gaia_job = Gaia.cone_search_async(coord, radius=radius, verbose=False, columns=['source_id', 'ra', 'dec', 'pmra', 'pmdec', 'ref_epoch', 'parallax', 'phot_variable_flag'])  
        gaia_cat = gaia_job.get_results()
        #ensure_dir(outputdir)
        astropy.io.ascii.write(gaia_cat, savepath, format="ecsv", overwrite=True)
    return np.asarray(gaia_cat)

def match_image_and_refcat(image_cat, reference_cat, wcs):
    '''Match entries in the image catalog to sources in a reference catalog

    Parameters:
    -----------

    image_cat: catalog containing the gaussian weighted positions (gwx,
               gwy) of the objects in the image
    reference_cat: catalog containing the radec coordinates of sources in the field
    wcs: image wcs providing transformation from pixels to radec_coordinates

    Returns:
    --------
    matched_catalog: subset of the input image_cat with counterparts in the reference_cat
    matched_catalog_ref: counterparts of matched_catalog in reference_cat
    '''
    ra, dec = (wcs.all_pix2world(np.array([image_cat['gwx'], image_cat['gwy']]).T, 1)).T
    image_cat['ra'] = ra
    image_cat['dec'] = dec
    
    index = match.match(reference_cat, image_cat, arcsecrad=5)
    matched_catalog = image_cat[index != -1]
    matched_catalog_ref = reference_cat[index[index != -1]]
    return matched_catalog, matched_catalog_ref
