import matplotlib.pyplot as plt
import numpy as np
import os

import bokeh.io 
import bokeh.layouts 
import bokeh.plotting 
import bokeh.models
import bokeh.client 
import bokeh.palettes


import astropy.visualization
import astropy.units 
import astropy.time 
import astropy.coordinates 
import matplotlib.dates 
import datetime
import sys
import time

import L_visibility as L
import importlib

#- Date selection
golden = (1 + 5 ** 0.5) / 2

"""
To run
bokeh serve app_visibility.py --port 5008 --dev

"""


class ObsNight(object):
    def __init__(self,
                 date=None,
                 n_obs=100,
                 mag_max=14,
                 delta_t=14.,
                 airmass_cut=1.2
                 ):
        #- Data
        self.n_obs = n_obs
        self.mag_max = mag_max
        self.delta_t = delta_t
        self.airmass_cut = airmass_cut
        
        self.date = date

        self.night_renderer_now = None
        self.night_renderers = []
        self.calspec_renderers = {}
        self.solar_system_renderers = {}
        
        self.d_night = None
        self.d_calspec = None
        self.d_airmass = None
        self.visibility = None

        self.figure = None


    def create_night_data(self):#date, mag_max=14, delta_t=14., n_obs=800, airmass_cut=1.2):
        """
        Selects the night, calculates the airmass, and selects the stars that can be seen above the airmass cut
        """
        d_night = {} # Night information
        
        ##- Creates the visibility object for the current date and with a magnitude cut for the calspec data
        visibility = L.Visibility(self.date, mag_max=self.mag_max, delta_t=self.delta_t, n_obs=self.n_obs)

        ##- Time window, keeping only visible stars:
        d_night['sunrise'], d_night['rise_twilight_12'], d_night['rise_twilight_18'] = L.get_sunrise(visibility)
        d_night['sunset'], d_night['set_twilight_12'], d_night['set_twilight_18'] = L.get_sunset(visibility)
        d_night['midnight'] = visibility.midnight_ohp
        d_night['begin'] = (visibility.midnight_ohp - visibility.delta_t * astropy.units.hour).to_datetime()
        d_night['end'] = (visibility.midnight_ohp + visibility.delta_t * astropy.units.hour).to_datetime()

        i_night = visibility.observing_frame.obstime < d_night['sunrise']
        i_night &= visibility.observing_frame.obstime > d_night['sunset']

        # Solar System:
        d_solar_system = {}
        d_solar_system['Moon'] = {'time':visibility.delta_midnight.to_datetime(),
                                  'airmass': visibility.get_target(name='Moon')['altaz'].secz.value,
                                  'alt':visibility.get_target(name='Moon')['altaz'].alt.value,
                                  'az':visibility.get_target(name='Moon')['altaz'].az.value,
                                  'name':['Moon'] * visibility.n_obs,
                                  'color': ['grey'] * visibility.n_obs} 

        
        # select the stars:
        l_colors = bokeh.palettes.Category20[20]
        time = visibility.delta_midnight.to_datetime()
        
        d_airmass = {}
        d_calspec = {'name':[],
                     'magnitude':[],
                     'airmass':[],
                     'time':[],
                     'color':[],
                     'alt':[],
                     'az':[],
                     'simbad_name':[]}

        for i_calspec,nt in enumerate(visibility.nt_calspec):
            simbad_name = nt['SIMBAD_NAME']
            calspec_name = nt['CALSPEC_NAME']
            simbad_name = nt['SIMBAD_NAME']
            altaz = visibility.get_target(name=simbad_name)['altaz']
            airmass = altaz.secz.value #np.abs(altaz.secz.value)
            if not np.all(np.isfinite(airmass)):
                continue # drop cases with airmass as nan
            if np.any(airmass < self.airmass_cut):
                color = l_colors[i_calspec % 20]
                mag_V = nt['V']
            
                d_calspec['name'].append(calspec_name)
                d_calspec['simbad_name'].append(simbad_name)
                d_calspec['magnitude'].append(mag_V)
                d_calspec['color'].append(color)
                i_top = np.argmin(airmass[i_night])
                d_calspec['airmass'].append((airmass[i_night][i_top]))
                d_calspec['alt'].append(altaz.alt[i_night][i_top].value)
                d_calspec['az'].append(altaz.az[i_night][i_top].value)
                d_calspec['time'].append((time[i_night][i_top]).strftime("%Hh%M"))

                print('Calculating %s for date %s'%(calspec_name, time[i_night][i_top].strftime("%m/%d %Hh%M")))
                d_airmass[calspec_name] = {}
                i_ok = airmass > 0
                d_airmass[calspec_name]['airmass'] = airmass[i_ok]
                d_airmass[calspec_name]['alt'] = altaz.alt.value[i_ok]
                d_airmass[calspec_name]['az'] = altaz.az.value[i_ok]
                d_airmass[calspec_name]['time'] = time[i_ok]
                d_airmass[calspec_name]['name'] = [calspec_name] * len(airmass[i_ok]) 
                d_airmass[calspec_name]['color'] = [color] * len(airmass[i_ok])
                d_airmass[calspec_name]['magnitude'] = [mag_V] * len(airmass[i_ok])

        self.visibility = visibility
        self.d_night = d_night
        self.d_calspec = d_calspec
        self.d_airmass = d_airmass
        self.d_solar_system = d_solar_system
        self.calspec_selected = []
        
    def init_date_picker(self):
        ##-- Date picker:
        self.date_picker = bokeh.models.DatePicker(title='Select date', value=self.date)
        self.date_picker.on_change("value", self.date_picker_callback)
        self.prog_button = bokeh.models.Button(label='Dump program')
        self.prog_button.on_event('button_click', self.make_obsprog)

    def date_picker_callback(self, attr, old, new):    
        selected_date = self.date_picker.value
        print("Selected date:", selected_date)
        self.date = selected_date
        self.update_all()
        
                                   
    def init_figure(self,
                    width=900,
                    height=900,
                    y_range=[5,1]):#[2.5,1]):
        ##- Define the plot with a title that gives the current time
        figure = bokeh.plotting.figure(width=width,
                                       height=height,
                                       y_range=y_range,
                                       x_axis_type='datetime',
                                       toolbar_location=None,
                                       x_axis_label='time (UTC)',
                                       y_axis_label='Airmass')
        figure.xaxis.ticker.desired_num_ticks = 24
        from bokeh.models import DatetimeTickFormatter
        xformatter = DatetimeTickFormatter(hours='%Hh', days='%d/%m')
        figure.xaxis.formatter = xformatter 
        figure.title.text = "Date: " + self.date + "\n"
        figure.title.text += "Now: " + datetime.datetime.utcnow().strftime(format='%Y-%m-%d %Hh%M')

        self.figure = figure

        #-- Hovering tool
        hover_tooltips = [
            ('Name', '@name'),
            ('Airmass', '@airmass (@alt, @az)'),
            ('Time', '@time{%Hh%M}')
        ]
        hover = bokeh.models.HoverTool(tooltips=hover_tooltips, mode='mouse')
        hover.formatters = {'@time': 'datetime'}
        self.figure.add_tools(hover)

    def callback_utcnow(self):
        self.plot_now_renderer()
        self.figure.title.text = "Now: " + datetime.datetime.utcnow().strftime(format='%Y-%m-%d %Hh%M')

        

    def init_table(self):
        table_columns = [ bokeh.models.TableColumn(field='name', title='Name'),
                            bokeh.models.TableColumn(field='magnitude', title='mV', formatter=bokeh.models.NumberFormatter(format="0.00")),                                 
                            bokeh.models.TableColumn(field='airmass', title='Transit', formatter=bokeh.models.NumberFormatter(format="0.00")),
                            bokeh.models.TableColumn(field='time', title='t(transit)'),
                            bokeh.models.TableColumn(field='alt', title='alt(transit)', formatter=bokeh.models.NumberFormatter(format="0.00")),
                            bokeh.models.TableColumn(field='az', title='az(transit)', formatter=bokeh.models.NumberFormatter(format="0.00")),
                            bokeh.models.TableColumn(field='simbad_name', title='Nom SIMBAD'),
]

        table_source = bokeh.models.ColumnDataSource(self.d_calspec)
        self.calspec_table = bokeh.models.DataTable(source=table_source,
                                                    columns=table_columns,
                                                    editable=False,
                                                    height=900)


        self.calspec_table.source.selected.on_change('indices', self.calspec_selection_callback)

    def calspec_selection_callback(self, attr, old, new):
        self.calspec_selected =  self.calspec_table.source.selected.indices
        print(self.calspec_selected)
        self.plot_calspec_renderers()        

        
    def get_widget(self):
        self.create_night_data()
        
        self.init_figure()
        self.init_date_picker()
        self.init_table()
        layout = bokeh.layouts.column(bokeh.layouts.row(self.figure, self.calspec_table), bokeh.layouts.row(self.date_picker, self.prog_button))

        self.plot_figure()
        
        return layout
        

    def update_all(self):
        self.create_night_data()
        table_source = bokeh.models.ColumnDataSource(self.d_calspec)
        self.calspec_table.source = table_source
        self.calspec_table.source.selected.on_change('indices', self.calspec_selection_callback)
        self.calsepc_selected = []
        self.calspec_renderers = {}
        
        self.figure.renderers = []
        self.night_renderer_now = None
        self.night_renderers = []
        for key in self.solar_system_renderers:
                self.solar_system_renderers[key] = None
        
        self.plot_figure()

    
    def plot_figure(self):
        print(self.d_night['begin'])
#        self.figure.update(start = self.d_night['begin'].timestamp() * 1.e3, end = self.d_night['end'].timestamp() * 1.e3)
        
        self.plot_now_renderer()
        self.plot_night_renderers()
        self.plot_solar_system_renderers()
        self.plot_calspec_renderers()
        
    def plot_now_renderer(self):    
        if self.night_renderer_now is not None:
            self.figure.renderers.remove(self.night_renderer_now)
            self.night_renderer_now = None
            
        if self.date == datetime.datetime.now().strftime('%Y-%m-%d'):
            v_now = bokeh.models.Span(location=datetime.datetime.utcnow(),
                                      dimension='height',
                                      line_color='black',
                                      line_width=3)    
            self.night_renderer_now = v_now
            self.figure.renderers.extend([self.night_renderer_now])


               
    def plot_night_renderers(self):
        #- first clear the existing lines, if they exist        
        v_sunrise = bokeh.models.Span(location=self.d_night['sunrise'],
                                      dimension='height',
                                      line_color='red',
                                      line_width=3)
        
        v_rise_twilight_12 = bokeh.models.Span(location=self.d_night['rise_twilight_12'],
                                               dimension='height',
                                               line_color='red',
                                               line_width=1)
            
        v_rise_twilight_18 = bokeh.models.Span(location=self.d_night['rise_twilight_18'],
                                               dimension='height',
                                               line_color='red',
                                               line_width=1,
                                               line_dash='dotted')
    
        v_sunset = bokeh.models.Span(location=self.d_night['sunset'],
                                     dimension='height',
                                     line_color='red',
                                     line_width=3)    
        v_set_twilight_12 = bokeh.models.Span(location=self.d_night['set_twilight_12'],
                                              dimension='height',
                                              line_color='red',
                                              line_width=1)
        v_set_twilight_18 = bokeh.models.Span(location=self.d_night['set_twilight_18'],
                                              dimension='height',
                                              line_color='red',
                                              line_width=1,
                                              line_dash='dotted')
        self.night_renderers.extend([v_sunrise, v_rise_twilight_12, v_rise_twilight_18, v_sunset, v_set_twilight_12, v_set_twilight_18])
        self.figure.renderers.extend(self.night_renderers)

                               
    def plot_solar_system_renderers(self):
        l_name = list(self.d_solar_system.keys())
        for key in l_name:
            source = bokeh.models.ColumnDataSource(self.d_solar_system[key])
            renderer = self.figure.circle(x='time',
                                          y='airmass',
                                          source=source,
                                          legend_label=key,
                                          color='color')


                
            self.solar_system_renderers[key] = renderer
            self.figure.renderers.extend([renderer])



            
    def plot_calspec_renderers(self):
        #- removes the calspec rendered and not selected:
        l_keys = list(self.calspec_renderers.keys())
        for i_calspec in l_keys:
            if i_calspec not in self.calspec_selected:
                renderer = self.calspec_renderers.pop(i_calspec)
                self.figure.renderers.remove(renderer)
                
        #- Plots active calspecs
        for i_calspec in self.calspec_selected:
            if i_calspec not in self.calspec_renderers:
                calspec_name = self.d_calspec['name'][i_calspec]
                source = bokeh.models.ColumnDataSource(self.d_airmass[calspec_name])
                self.calspec_renderers[i_calspec] = self.figure.line(x='time',
                                                                     y='airmass',
                                                                     legend_label=calspec_name,
                                                                     color=self.d_airmass[calspec_name]['color'][0],
                                                                     source=source,
                                                                     line_width=3)

    def make_obsprog(self):
        names = [self.d_calspec['name'][i_calspec] for i_calspec in self.calspec_selected]
        airmasses = np.array([self.d_airmass[calspec_name]['airmass'] for calspec_name in names])

        targets = ['EVENING_FLAT']
        times = [self.d_night['set_twilight_12']]

        while times[-1] < self.d_night['rise_twilight_18']:
            times.append(times[-1] + datetime.timedelta(hours=1))
            targets.append(names[0])
            times.append(times[-1] + datetime.timedelta(minutes=30))
            targets.append('led_long')
        times.append(self.d_night['sunrise'])
        targets.append('MORNING_FLAT')
        with open('toto.pkl', "wb") as fid:
            import pickle
            pickle.dump(targets, fid)
            pickle.dump(times, fid)
        print('program saved in toto.pkl')
