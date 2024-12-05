import bokeh.models
import bokeh.plotting
import summary_plots
import astropy.time
import bokeh.transform
import logging
import datetime
from stardiceonline.archive.archive import local_archive
import time

band_color_map = {
    'u': 'violet',
    'g': 'green',
    'r': 'pink',
    'i': 'red',
    'z': 'magenta',
    'y': 'orange',
    'GRISM': 'black'}

bands = ['u', 'g', 'r', 'i', 'z', 'y', 'GRISM']

def sanitize_name(name):
    return name.replace(' ', '_').replace('[', '').replace(']', '').replace('#','').replace('/', 'per')

tooltips_image_summary = [("mjd", "@mjd{5.4f}"), ("seeing", "@seeing"), ("band", "@band"), ("expnum", '@expnum')]

class NightPlotWidget(object):
    ''' Base class for plots sharing the same Nightly data'''
    def __init__(self, summary_data, width=800, height=300, x='time', y='seeing', label=None, tooltips=tooltips_image_summary):
        self.summary_data = summary_data
        if label is None:
            label=y
        self.figure = bokeh.plotting.figure(width=width, height=height, tools='pan,box_zoom,reset,save,tap', x_axis_type='datetime', y_axis_label=label)
        self.tooltips = tooltips
        self.plot = self.figure.scatter(x=x, y=y, size=7, legend_group='band', color=bokeh.transform.factor_cmap('band', 'Category10_7', bands), fill_alpha=0.5, source=summary_data)
        self.figure.legend.location = "top_left"
        self.figure.legend.title = "Filter"
        self.figure.legend.click_policy="hide"
        self.hovertool = bokeh.models.HoverTool(tooltips=self.tooltips, mode='mouse')
        self.figure.add_tools(self.hovertool)

class NightPlotWidgets():
    def __init__(self, axes=[], labels=[], heights=[], selection_callback=[]):
        self.summary_data = bokeh.models.ColumnDataSource(data=dict(mjd=[], seeing=[], color=[], band=[], expnum=[], time=[], temperature=[], humidity=[], skylev=[]))
        self.plots = [NightPlotWidget(self.summary_data, height=h, y=a, label=l, tooltips=tooltips_image_summary)
                      for a, l, h in zip(axes, labels, heights)]
        self.selection_callback = selection_callback
        self.summary_data.selected.on_change('indices', self.select_one)
            
    def select_one(self, attr, prev, new):
        logging.info(f'Select image')
        selected = self.summary_data.selected.indices
        if len(selected) > 0:
            sel = int(self.summary_data.data['expnum'][selected[0]])
            logging.info(f'Select image {sel}')
            for c in self.selection_callback:
                c(sel)
                
    def update_summary(self, directory):
        logging.info(f'Looking for images in directory {directory}')
        summary = summary_plots.SummaryPlots(directory.directory)
        nt = summary.get_summary()
        if len(nt) > 0:
            times = [astropy.time.Time(e['MOUNTMJD'], format='mjd').datetime for e in nt]
            summary_fields = ['MOUNTMJD', 'filterwheelfilter', 'EXPNUM', 'seeing', 'raritanhumidity', 'raritantemperature', 'skylev']
            display_fields = ['mjd', 'band', 'expnum', 'seeing', 'humidity', 'temperature', 'skylev']
            self.summary_data.data=dict([('time', times)] +[(f1, nt[f2]) for f1, f2 in zip(display_fields, summary_fields)])

    def get_widget(self):
        return bokeh.layouts.column(*[p.figure for p in self.plots])

tooltips_meteo_summary = [("date", "@date"), ("T [°C]", '@Air_temperature_C'), ("pressure [hPa]", '@Air_pressure_hPa'), ("wind [m/s]", "@Wind_speed_average_mpers")]
class MeteoPlotWidget(object):
    ''' Base class for plots sharing the same Nightly data'''
    def __init__(self, summary_data, width=800, height=300, x='time', y='Air_temperature_C', label=None, tooltips=tooltips_meteo_summary):
        self.summary_data = summary_data
        if label is None:
            label=y
        self.figure = bokeh.plotting.figure(width=width, height=height, tools='pan,box_zoom,reset,save,tap', x_axis_type='datetime', y_axis_label=label)
        self.tooltips = tooltips
        self.plot = self.figure.line(x=x, y=y, alpha=0.5, source=summary_data)
        self.figure.legend.location = "top_left"
        self.figure.legend.title = "Filter"
        self.figure.legend.click_policy="hide"
        self.hovertool = bokeh.models.HoverTool(tooltips=self.tooltips, mode='vline')
        self.figure.add_tools(self.hovertool)
        
class MeteoPlotWidgets():
    fields = ['#date', 'Wind direction minimum [deg]', 'Wind direction average [deg]', 'Wind direction maximum [deg]', 'Wind speed minimum [m/s]', 'Wind speed average [m/s]', 'Wind speed maximum [m/s]', 'Air temperature [C]', 'Relative humidity [%]', 'Air pressure [hPa]', 'Rain accumulation [mm]', 'Rain duration [s]', 'Rain intensity [mm/h]', 'Hail accumulation [hits/cm2]', 'Hail duration [s]', 'Hail intensity [hits/cm2/h]', 'Heating temperature [C]', 'Heating voltage [V]', 'Supply voltage [V]', 'Reference voltage [V]']
    def __init__(self, axes=[], labels=[], heights=[], selection_callback=[]):
        self.summary_data = bokeh.models.ColumnDataSource(data=dict([(sanitize_name(field), []) for field in ['time'] + self.fields]))
        self.plots = [MeteoPlotWidget(self.summary_data, height=h, y=a, label=l, tooltips=tooltips_meteo_summary)
                      for a, l, h in zip(axes, labels, heights)]
        self.plots[0].figure.title='Meteo'

    def update_meteo(self, filename=None):
        import pandas as pd
        if filename is not None:
            logging.info(f'Looking for meteo data in file {filename}')
            nt = pd.read_csv(filename)
        else:
            flist = local_archive.last_meteo_files()
            if len(flist) > 2:
                nt = pd.concat([pd.read_csv(flist[-2]), pd.read_csv(flist[-1])])
                # Keeping only the last 24hours
                nt = nt[(time.time() - nt['timestamp']) < (24*3600)]
            elif len(flist) == 1:
                nt = pd.read_csv(flist[-1])
                # Keeping only the last 24hours
                nt = nt[(time.time() - nt['timestamp']) < (24*3600)]
            else:
                nt = []

        if len(nt) > 0:
            times = [datetime.datetime.fromtimestamp(e) for e in nt['timestamp']]
            self.summary_data.data=dict([('time', times)] + [(sanitize_name(field), nt[field]) for field in self.fields])
            
    def get_widget(self):
        return bokeh.layouts.column(*[p.figure for p in self.plots])
    
