import pipelet3.socketrpc
from stardiceonline.tools.config import config
from stardiceonline.processing.detrending import OVERSCANA, ILLUREGION, OVERSCANB
import matplotlib.pyplot as plt
import numpy as np

plt.ion()

stardice = pipelet3.socketrpc.SecureRPCClient(f'http://127.0.0.1:{config["webapp.serverport"]}')
stardice.login('toto', 'titi')

#
# debugging functions
#
def detrend(im):
    res = im - np.mean(im[OVERSCANA], axis=0) #[:-100]
    return np.subtract(res[ILLUREGION].T, np.mean(res[OVERSCANB], axis=1)).T

def lamp(repeat=1, filter_sequence=['GRISM'], exptime=5, dark_before=1, dark_after=1, n_images=1, led=0, rate=50, ksphere=True):
    state = {
        'star152': False,
        'sphere': True,
        'ksphere': ksphere,
        'mount.TARGET': 'SPHERE',
        'ksphere.range': 2.e-4,
        'ksphere.nsamples': int(exptime * rate),
        'ksphere.timer': 1/rate,
        'ksphere.rate': 50/rate,
        'ps.volet': 'ON',
    }
    l = []
    for rep in range(repeat):
        for band in filter_sequence:
            state['camera.exptime'] = exptime
            state['filterwheel.filter'] = band
            state['sphere.led'] = 0
            for image in range(dark_before):
                l.append(state.copy())
            state['sphere.led'] = led
            for image in range(n_images):
                l.append(state.copy())
            state['sphere.led'] = 0
            for image in range(dark_after):
                l.append(state.copy())
    return l

def image(band='PINHOLE', exptime=0.1, full=False, show=True, log=True, volet='ON', focus_offset=0, state={}):
    image = stardice.image(exptime, band, volet, focus_offset, state)
    if not full:
        image = detrend(image['pixels'])
        if show:
            if log:
                plt.imshow(np.log10(image))
            else:
                plt.imshow(image)
    return image
