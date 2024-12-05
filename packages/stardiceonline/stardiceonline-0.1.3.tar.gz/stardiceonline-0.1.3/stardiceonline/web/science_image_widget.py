import bokeh.models
import bokeh.plotting
import bokeh.palettes
import numpy as np
import logging

from stardiceonline.tools import orgfiles
from stardiceonline.tools.metadatamanager import MetaDataManager

manager = MetaDataManager()

targets, _ = orgfiles.fromorg(manager.get_data('targets.org', 'http://supernovae.in2p3.fr/stardice/stardiceot1/targets.org'))

def zscale(data):
    samples = data[::10,::10].flatten()  
    return np.percentile(samples, [10, 90])

TOOLTIPS = [
    ("x", "$x"),
    ("y", "$y"),
    ("value", "@image")]
TOOLTIST = [
    ("ra", "@ra"),
    ("dec", "@dec"),
    ("fiso", "@fiso"),
    ("fluxmax", "@fluxmax"),
]

class ScienceImageWidget():
    def __init__(self):
        self.figure = bokeh.plotting.figure(width=800, height=800, tools='pan,wheel_zoom,reset,save', active_scroll='wheel_zoom')
        #self.mapper = bokeh.models.LinearColorMapper(palette=bokeh.palettes.Greys256, low=100, high=300)
        self.picture = self.figure.image(image=[], x=0, y=0, dw=[], dh=[])#, color_mapper=self.mapper)
        self.hover = bokeh.models.HoverTool(tooltips=TOOLTIPS,
                                            renderers=[self.picture])
        self.figure.add_tools(self.hover)
        self.source = self.picture.data_source
        self._state()
        self._catalogs()
        
    def _state(self):
        '''Set up checkbox button to change the display state
        '''
        self.display_state = {
            'Catalog': False,
            'Zscale': False,
            'Log': True,
            'IR': False}
        self.state_button_group = bokeh.models.CheckboxButtonGroup(
            labels=list(self.display_state.keys()),
            active=[i for i, s in enumerate(self.display_state) if self.display_state[s]])
        self.state_button_group.on_event('button_click', self.change_state)
                
    def _catalogs(self):
        '''Set up the display of detected objects as circles in the image'''
        self.catalog = bokeh.models.ColumnDataSource(
            data=dict(x=[], y=[], a=[], b=[], angle=[],
                      ra=[], dec=[], fiso=[], fluxmax=[]
            ))
        self.target_image_coord = bokeh.models.ColumnDataSource(
            data=dict(x=[], y=[], name=[]))
        self.catalog_plot = self.figure.ellipse(x="x", y="y", width='a', height='b', angle='angle', source=self.catalog, fill_alpha=0.1, color='green')
        self.target_plot = self.figure.circle(x="x", y="y", radius=5, source=self.target_image_coord, fill_alpha=0.1, color='red')
        hovers = bokeh.models.HoverTool(tooltips=TOOLTIST,
                                        renderers=[self.catalog_plot])
        self.figure.add_tools(hovers)
        self.cat = []

    ################
    # Event handlers
    ################
    def change_state(self, new):
        for i, k in enumerate(self.display_state.keys()):
            if i in new.model.active:
                self.display_state[k] = True
            else:
                self.display_state[k] = False
        self.set_color_scale()
        self.update_catalog()
        self.update_image()
        
    def set_color_scale(self):
        logging.debug(f'{self.picture.glyph.color_mapper}')
        if self.display_state['Log']:
            mapper = bokeh.models.LogColorMapper(palette=bokeh.palettes.Greys256, low=100, high=300)
            logging.debug('Visualizition switch to log scale')
        else:
            mapper = bokeh.models.LinearColorMapper(palette=bokeh.palettes.Greys256, low=100, high=300)
        try:
            data = self.source.data['image'][0]
            if self.display_state['Zscale']:
                dmin, dmax = zscale(data)
                logging.debug('Visualizition switch to zscale')
            else:
                logging.debug('Visualizition switch to full scale')
                dmin, dmax = data.min(), data.max()
            mapper.low = max(dmin, 1)
            mapper.high = dmax
        except IndexError:
            # No image available, we leave the scale as it is
            pass
        self.picture.glyph.color_mapper = mapper
        
    def load_image(self, directory, expnum):
        try:
            self.vis, self.cat, self.title, self.header, self.wcs, self.ir, self.ir_stream = directory[expnum]
            logging.debug(f'Loading image {self.title}')
        except ValueError:
            logging.debug(f'No image')
            self.vis, self.cat, self.title, self.header, self.wcs, self.ir, self.ir_stream = [], [], 'NO IMAGES', [], [], [], []
        self.update_image()

    def update_image(self):
        if self.display_state['IR']:
            data = self.ir
        else:
            data = self.vis
        if len(data) > 0:
            self.source.data = {'image':[data],
                                'dw': [data.shape[1]],
                                'dh': [data.shape[0]],
            }
        else:
            self.source.data = {'image': [],
                                'dw': [],
                                'dh': []}
        self.figure.title.text = self.title
        self.set_color_scale()
        self.update_catalog()
        
    def update_catalog(self):
        catalog_fields = ['x', 'y', 'a', 'b', 'angle', 'ra', 'dec', 'fiso', 'fluxmax']
        if (len(self.cat) > 0) and self.display_state['Catalog']:
            data = dict([(f, self.cat[f]) for f in catalog_fields])
            data['a'] = 3*data['a']
            data['b'] = 3*data['b']
            self.catalog.data = data

            tname = self.header['mountTARGET'].strip()
            if tname in targets['TARGET'] and self.wcs is not None:
                t = targets[targets['TARGET'] == tname][0]
                tx, ty = self.wcs.all_world2pix(np.array([[float(t['RA']), float(t['DEC'])]]), 0).T
                self.target_image_coord.data = {'x': list(tx),
                                                'y': list(ty),
                                                'name': [tname]}
            else:
                self.target_image_coord.data = {'x': [],
                                                'y': [],
                                                'name': []}
        else:
            self.catalog.data = dict([(f, []) for f in catalog_fields])
            self.target_image_coord.data = {'x': [],
                                            'y': [],
                                            'name': []}
        
    #######
    # Utils
    #######
    def get_widget(self):
        return bokeh.layouts.column(self.state_button_group,self.figure)
    
    
