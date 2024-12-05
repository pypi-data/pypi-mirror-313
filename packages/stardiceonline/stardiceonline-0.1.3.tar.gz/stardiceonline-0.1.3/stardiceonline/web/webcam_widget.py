import bokeh.plotting
import bokeh.models
import bokeh.palettes
import numpy as np
import logging
from pipelet3 import socketrpc
from fancywebcam_server import uncompress
from stardiceonline.archive import ssh
from stardiceonline.tools.config import config

class Webcam(object):
    def __init__(self, title='Telescope webcam', width=650):
        self.figure = bokeh.plotting.figure(width=width, height=300, tools='pan,wheel_zoom,reset,save', active_scroll='wheel_zoom')
        self.mapper = bokeh.models.LinearColorMapper(palette=bokeh.palettes.Greys256, low=0, high=65000)
        self.plot = self.figure.image(image=[], x=0, y=0, dw=[], dh=[], color_mapper=self.mapper)
        self.source = self.plot.data_source
        self.oldtimestamp = ''
        self.title = title
        self.figure.title = self.title
        self._connect()
        self.compressed = True
        
    def _connect(self):
        url = f'http://127.0.0.1:{config["webapp.webcamport"]}'
        try:
            ssh.ssh_tunnel(config['webapp.webcamport'], config['ssh.telhost']) # webcam
            self.cam = socketrpc.SecureRPCClient(url=url)
        except Exception as e:
            logging.error(f'Failed connection to the webcam server {url}: {e}')
            self.cam = None
            
    def update_webcam(self):
        if self.cam is None:
            return
        logging.debug('Poll webcam')
        try:
            last = self.cam.get_last(self.oldtimestamp, self.compressed)
        except Exception as e:
            logging.warning(f'Failed to retrieve the webcam image: {e}')
            last = {'timestamp': 'LOST'}
        if last:
            if last['timestamp'] != 'LOST':
                if self.compressed:
                    last = uncompress(last)
                logging.debug('Webcam update')
                self.figure.title.text = f"{self.title}:{last['timestamp']}({last['exptime']:.3f}s)"

                #logging.debug(f'image scale: [{np.nanmin(last)}, {np.nanmax(last)}]')
                if self.compressed:
                    self.mapper.low, self.mapper.high = 0, 255
                else:
                    self.mapper.low, self.mapper.high = np.percentile(last['image'][::4,::4].ravel(), [5, 95])
                #self.mapper.high = np.max(last[::4, ::4])
                self.source.data = {'image':[last['image']],
                                    'dw': [last['image'].shape[1]],
                                    'dh': [last['image'].shape[0]]
                                    }
            else:
                self.source.data = {'image': [],
                                    'dw': [],
                                    'dh': [],}
