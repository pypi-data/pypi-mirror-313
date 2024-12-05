#!/usr/bin/python
import numpy as np

deg2rad = deg2rad = np.pi / 180

def euclidian(x1, y1, x2, y2):
    return np.sqrt((np.array(x1) - np.array(x2)) ** 2 + (np.array(y1) - np.array(y2)) ** 2)

def haversine(ra1, dec1, ra2, dec2):
    dlambda = np.array(ra1 - ra2)
    return np.arccos(np.sin(dec1) * np.sin(dec2) + np.cos(dec1) * np.cos(dec2) * np.cos(dlambda))


def gnomonic_projection(ra, dec, center=None):
    ra_rad, dec_rad = ra * deg2rad, dec * deg2rad
    if center is None:
        center = ra_rad.mean(), dec_rad.mean()
    else:
        center = center[0] * deg2rad, center[1] * deg2rad
    s, c = np.sin(dec_rad), np.cos(dec_rad)
    c2 = np.cos(center[0] - ra_rad)
    d = np.sin(center[1]) * s + np.cos(center[1]) * c * c2
    x = (np.cos(center[1]) * np.sin(center[0] - ra_rad)) / d
    y = (np.sin(center[1]) * c - np.cos(center[1]) * s * c2) / d
    return x, y


class NearestNeighAssoc():
    """Solve the fixed-radius nearest neighbor search on a 2D cartesian
    lattice
    """
    def __init__(self, first=[], extension=[], radius=1):
        self.belongs = {}
        self.clusters = []
        self.radius = radius
        
        if extension:
            xmin, xmax, ymin, ymax = extension
            self.x_bins = np.arange(xmin - 0.01 * radius, xmax + 0.01 * radius, radius)
            self.y_bins = np.arange(ymin - 0.01 * radius, ymax + 0.01 * radius, radius)
        elif first:
            firstx, firsty = first
            xmin, xmax, ymin, ymax = firstx.min(), firstx.max(), firsty.min(), firsty.max()
            self.x_bins = np.arange(xmin - 0.01 * radius, xmax + 0.01 * radius, radius)
            self.y_bins = np.arange(ymin - 0.01 * radius, ymax + 0.01 * radius, radius)
            self.clusters = list(zip(firstx, firsty))
            i = np.digitize(firstx, self.x_bins)
            j = np.digitize(firsty, self.y_bins)
            for k in range(len(i)):
                ik, jk = i[k], j[k]
                self.belongs[(ik, jk)] = self.belongs.get((ik, jk), []) + [k]
        
            
    def append(self, x, y, metric=haversine):
        if not hasattr(self, 'x_bins'):
            xmin, xmax, ymin, ymax = x.min(), x.max(), y.min(), y.max()
            self.x_bins = np.arange(xmin - 0.01 * self.radius, xmax + 0.01 * self.radius, self.radius)
            self.y_bins = np.arange(ymin - 0.01 * self.radius, ymax + 0.01 * self.radius, self.radius)

        i = np.digitize(x, self.x_bins)
        j = np.digitize(y, self.y_bins)
        index = np.zeros(len(i))
        
        for k in range(len(i)):
            ik, jk = i[k], j[k]
            # gather the list of clusters in the neighborhood
            candidates = sum([self.belongs.get((i_n, j_n), []) for i_n in (ik - 1, ik, ik + 1) for j_n in (jk - 1, jk, jk + 1)],[])
            if candidates:
                distance = metric(x[k], y[k], [self.clusters[l][0] for l in candidates], [self.clusters[l][1] for l in candidates])
                l = distance.argmin()
            if candidates and distance[l] < self.radius:
                m = candidates[l]
                index[k] = m
                self.clusters[m][2] += 1
            else:
                clu_i = len(self.clusters)
                index[k] = clu_i
                self.clusters.append([x[k], y[k], 1])
                self.belongs[(ik, jk)] = self.belongs.get((ik, jk), []) + [clu_i]
        return index

    def match(self, x, y, metric=haversine):
        i = np.digitize(x, self.x_bins)
        j = np.digitize(y, self.y_bins)
        index = np.zeros(len(i), dtype='int')
        for k in range(len(i)):
            ik, jk = i[k], j[k]
            # gather the list of clusters in the neighborhood
            candidates = sum([self.belongs.get((i_n, j_n), []) for i_n in (ik - 1, ik, ik + 1) for j_n in (jk - 1, jk, jk + 1)],[])
            if candidates:
                distance = metric(x[k], y[k], [self.clusters[l][0] for l in candidates], [self.clusters[l][1] for l in candidates])
                l = distance.argmin()
            if candidates and distance[l] < self.radius:
                m = candidates[l]
                index[k] = m
            else:
                index[k] = -1
        return index
    
    def get_cat(self):
        clusters = np.rec.fromrecords(self.clusters, names=['ra', 'dec', 'n'])
        clusters['ra'] /= deg2rad
        clusters['dec'] /= deg2rad
        return clusters

def assoc(catalog, project=True, xy=False, radius=3e-4 * deg2rad):
    if project:
        x, y = gnomonic_projection(np.array(catalog['ra']), np.array(catalog['dec']))
#        x, y = gnomonic_projection(catalog['ra'], catalog['dec'])
    elif xy:
        x, y = np.array(catalog['x']), np.array(catalog['y'])
    else:
        x, y = stack['ra'] * deg2rad, stack['dec'] * deg2rad
    assoc =  NearestNeighAssoc(radius=radius)
    index = assoc.append(x, y, metric=euclidian if (project or xy) else haversine)
    clusters = assoc.get_cat()
    return index.astype(int), clusters

def match(refcat, cat, project=True, xy=False, arcsecrad=1):
    def _arr(x): 
        return np.array(x)
    if project:
        xref, yref = gnomonic_projection(_arr(refcat['ra']), _arr(refcat['dec']), 
                                         center=[refcat['ra'].mean(), refcat['dec'].mean()])
        x, y = gnomonic_projection(_arr(cat['ra']), _arr(cat['dec']), 
                                   center=[refcat['ra'].mean(), refcat['dec'].mean()])
    elif xy:
        xref, yref = _arr(refcat["x"]), _arr(refcat["y"])
        x, y = _arr(cat["x"]), _arr(cat["y"])
    else:
        xref, yref = _arr(refcat['ra']) * deg2rad, _arr(refcat['dec']) * deg2rad
        x, y = _arr(cat['ra']) * deg2rad, _arr(cat['dec']) * deg2rad
    assoc =  NearestNeighAssoc(first=[xref, yref], radius=arcsecrad/3600. * deg2rad)
    index = assoc.match(x, y, metric=euclidian if (project or xy) else haversine)
    return index

def radius_to_nside(radius):
    """Find the smallest nside for wich a circle of radius radius is
    contained within an healpy pixel.
    
    radius: in radian
    """
    npix = 4 * np.pi / (2 * radius) ** 2
    order = int(np.ceil(np.log2(np.sqrt(npix / 12))))
    return 2 ** order

class NearestNeighAssocHealpy():
    """Solve the fixed-radius nearest neighbor search on a 2D Healpy
    lattice. Good for full-sky match.

    """
    
    def __init__(self, first=[], radius=np.pi / 180./ 3600.):
        import healpy
        self.belongs = {}
        self.clusters = []
        self.radius = radius
        self.nside = radius_to_nside(radius)
        
        if first:
            firstra, firstdec = first[0] * deg2rad, first[1] * deg2rad
            self.clusters = list(zip(firstra, firstdec))
            i = healpy.ang2pix(self.nside, np.pi/2 - firstdec, firstra)
            for k in range(len(i)):
                self.belongs[i[k]] = self.belongs.get(i[k], []) + [k]
        
            
    def append(self, ra, dec, metric=haversine):
        import healpy
        ra_rad, dec_rad = np.array(ra * deg2rad), np.array(dec * deg2rad)
        i = healpy.ang2pix(self.nside, np.pi/2 - dec_rad, ra_rad)
        index = np.zeros(len(i), dtype='int')
        
        for k in range(len(i)):
            ik = i[k]
            # gather the list of clusters in the neighborhood
            neighpix = list(healpy.get_all_neighbours(self.nside, ik)) + [ik]
            candidates = sum([self.belongs.get(i_n, []) for i_n in neighpix if neighpix != -1],[])
            if candidates:
                distance = metric(ra_rad[k], dec_rad[k], [self.clusters[l][0] for l in candidates], [self.clusters[l][1] for l in candidates])
                l = distance.argmin()
            if candidates and distance[l] < self.radius:
                m = candidates[l]
                index[k] = m
                self.clusters[m][2] += 1
            else:
                clu_i = len(self.clusters)
                index[k] = clu_i
                self.clusters.append([ra_rad[k], dec_rad[k], 1])
                self.belongs[ik] = self.belongs.get(ik, []) + [clu_i]
        return index

    def match(self, ra, dec, metric=haversine):
        import healpy
        ra_rad, dec_rad = np.array(ra * deg2rad), np.array(dec * deg2rad)
        i = healpy.ang2pix(self.nside, np.pi/2 - dec_rad, ra_rad)
        index = np.zeros(len(i), dtype='int')
        for k in range(len(i)):
            ik = i[k]
            # gather the list of clusters in the neighborhood
            neighpix = list(healpy.get_all_neighbours(self.nside, ik)) + [ik]
            candidates = sum([self.belongs.get(i_n, []) for i_n in neighpix if neighpix != -1],[])
            if candidates:
                distance = metric(ra_rad[k], dec_rad[k], [self.clusters[l][0] for l in candidates], [self.clusters[l][1] for l in candidates])
                l = distance.argmin()
            if candidates and distance[l] < self.radius:
                m = candidates[l]
                index[k] = m
            else:
                index[k] = -1
        return index

    def get_cat(self):
        clusters = np.rec.fromrecords(self.clusters, names=['ra', 'dec', 'n'])
        clusters['ra'] /= deg2rad
        clusters['dec'] /= deg2rad
        return clusters
