import datetime
import logging
import time
from pipelet3 import socketrpc, rpc
import threading
import numpy as np
import gzip

def compress(im):
    compressed = dict(im)
    image, low, high = rescale(rebin(compressed.pop('image')))
    compressed.update({'data': gzip.compress(image.tobytes()),
                       'shape': image.shape,
                       'dtype': image.dtype,
                       'crop_scale': (low, high)})
    return compressed

def uncompress(im):
    uncompressed = {'image': np.frombuffer(gzip.decompress(im.pop('data')), dtype=im.pop('dtype')).reshape(im.pop('shape'))}
    uncompressed.update(im)
    return uncompressed 

def rebin(im, n=2):
    return im.reshape((im.shape[0]//n, n, im.shape[1]//2, n)).mean(axis=1).mean(axis=2)

def rescale(im):
    low, high = np.percentile(im[::4,::4].ravel(), [5, 95])
    return ((im - low)*(255/high)).clip(0,255).astype(np.uint8), low, high


class FancyWebcamServer(object):
    '''Stream Server for high dynamic range camera such as the ZWO ASI290MM
    '''
    def __init__(self, webcam, min_exp=1e-4, max_exp=10):
        self.cam = webcam
        self.exptime = min_exp
        self.full = {}
        self._set_exptime()
        self.running = True
        self.min_exp = min_exp
        self.max_exp = max_exp
        self.max_refresh_rate = 2 #Hz
        
    def _set_exptime(self):
        self.cam.set_exptime(self.exptime)
        
    def _dynamic_range_update(self):
        ''' Dynamically adjust the exposure time based on the last image brightness
        '''
        if self.small:
            x = self.small['crop_scale'][1]
            old = self.exptime
            if x >15000:
                self.exptime = self.exptime / 2
            elif (x < 5000):
                self.exptime = self.exptime * 2
            if self.exptime > self.max_exp:
                self.exptime = self.max_exp
            if self.exptime < self.min_exp:
                self.exptime = self.min_exp
            if old != self.exptime:
                self._set_exptime()

    def get_last(self, timestamp, compressed):
        if self.full['timestamp'] != timestamp:
            if compressed:
                return self.small
            else:
                return self.full
        else:
            return {}

    def _refresh_loop(self):
        while self.running and threading.main_thread().is_alive():
            try:
                #self.last_image = self.cam.take_frame()
                self.full ={
                    'image': self.cam.get_image(),
                    'timestamp': datetime.datetime.utcnow().isoformat(),
                    'exptime': self.exptime
                }
                self.small = compress(self.full)
                self._dynamic_range_update()
            except Exception as e:
                logging.error(e)
                self.full = {'image': None,
                             'timestamp': 'LOST',
                             'exptime': 1e-3
                             }
                #self.cam.connect()
                time.sleep(1)
            time.sleep(1/self.max_refresh_rate)
            
    def _start(self):
        threading.Thread(target=self._refresh_loop, daemon=True).start()

    def stop(self):
        self.running = False

class AbstractCameraZwoAsi():
    def __init__(self):
        import camera_zwo_asi
        self.cam = camera_zwo_asi.Camera(0)
        roi = self.cam.get_roi()
        roi.type = camera_zwo_asi.ImageType.raw16
        self.cam.set_roi(roi)
    
    def set_exptime(self, exptime):
        self.cam.set_control('Exposure', int(exptime * 1e6))

    def get_image(self):
        return self.cam.capture().get_image()

class AbstractZwoAsi():
    def __init__(self):
        import zwoasi
        import os
        if zwoasi.zwolib is None:
            zwoasi.init(os.path.join(os.environ['STARDICEPATH'], 'drivers/zwoasi/libASICamera2.so'))
        self.cam = zwoasi.Camera(0)
        self.cam.disable_dark_subtract()
        self.set_image_type(zwoasi.ASI_IMG_RAW16)

    def set_image_type(self, val):
        import zwoasi
        self.cam.set_image_type(val)
        self.nbytes = {zwoasi.ASI_IMG_RAW16:2, zwoasi.ASI_IMG_RAW8:1}[val]
        self._prepare_buffer()

    def _prepare_buffer(self):
        import zwoasi
        import ctypes
        self.whbi = zwoasi._get_roi_format(self.cam.id)
        self.shape = self.whbi[1], self.whbi[0]
        self.sz = self.whbi[0] * self.whbi[1] * self.nbytes
        self.buffer_1 = bytearray(self.sz)
        cbuf_type = ctypes.c_char * len(self.buffer_1)
        self.cbuf1 = cbuf_type.from_buffer(self.buffer_1)
        self.im1 = np.frombuffer(self.buffer_1, dtype='uint16')
    
    def set_exptime(self, exptime):
        import zwoasi
        self.exptime = int(exptime*1e6)
        self.cam.set_control_value(zwoasi.ASI_EXPOSURE, self.exptime)
        
    def get_image(self):
        import zwoasi
        r = zwoasi.zwolib.ASIStartExposure(self.cam.id, False)
        if r:
            logging.error(f'{r}')
            raise zwoasi.zwo_errors[r]
        time.sleep((self.exptime)*1e-6)
        i = 0
        while (self.cam.get_exposure_status() != 2):
            #print(('Data not ready %d ms' % i))
            time.sleep(0.01)
            i = i+10
        r = zwoasi.zwolib.ASIGetDataAfterExp(self.cam.id, self.cbuf1, self.sz)
        if r:
            raise zwoasi.zwo_errors[r]
        return self.im1.reshape(self.whbi[1::-1])

def start(url):
    try:
        cam = AbstractCameraZwoAsi()
    except ImportError:
        cam = AbstractZwoAsi()
    webcam = FancyWebcamServer(cam)
    time.sleep(1)
    webcam._start()
    server = socketrpc.SecureRPCServer(webcam, url=url)
    try:
        server.start()
    finally:
        webcam.stop()

def main():
    import argparse
    import os
    parser = argparse.ArgumentParser(
        description='Test the speed of the rpc system')
    parser.add_argument(
        '-d', '--daemon', action='store_true',
        help='Run in deamon mode')
    parser.add_argument(
        '-H', '--hostname', default='',
        help='Give hostname and port instead of url')
    parser.add_argument(
        '-p', '--port', default='',
        help='Give hostname and port instead of url')
    parser.add_argument(
        '--url', default='http://127.0.0.1:9983', 
        help='Url of the server')
    
    args = parser.parse_args()
    if args.hostname:
        url = f'http://{args.hostname}:{args.port}'
    else:
        url = args.url
    if args.daemon:
        rpc.daemonize(lambda: start(url), logfile=os.path.expanduser('~/logs/webcam_log'))
    else:
        start(url)
    
if __name__ == '__main__':
    main()
