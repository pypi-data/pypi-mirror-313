import bokeh.models
import bokeh.plotting
import bokeh.layouts
import numpy as np

from stardiceonline.tools import orgfiles
from stardiceonline.tools.metadatamanager import MetaDataManager
from stardiceonline.tools.config import config
from stardiceonline.pointing_model import pointing_model
import pipelet3.socketrpc
import logging
from stardiceonline.archive import ssh

manager = MetaDataManager()

targets, _ = orgfiles.fromorg(manager.get_data('targets.org', 'http://supernovae.in2p3.fr/stardice/stardiceot1/targets.org'))
pointing_model_params = manager.get_data('pointing_model_last.npy', 'http://supernovae.in2p3.fr/stardice/stardiceot1/pointing_model_parameters_2023_01_18.npy')

def polar_coordinate_to_xy(alt, az):
    return (90-alt) * np.cos(np.radians(az)), (90-alt) * np.sin(-np.radians(az))

callback = bokeh.models.CustomJS(args=dict(), code="""
    function showLoginDialog() {
        const login = prompt("Please enter your login:", "");
        if (login !== null) {
            const password = prompt("Please enter your password:", "");
            if (password !== null) {
                const event = new CustomEvent('login-attempt', { detail: { login, password } });
                document.dispatchEvent(event);
            }
        }
    }
    showLoginDialog();
""")    

def format_status(status):
    if status['observation_status'] == 'OBSERVING':
        return f"Telescope status: {status['observation_status']} ({status['sequence']})"
    else:
        return f"Telescope status: {status['observation_status']}"
    
class TelescopeWidget():
    def __init__(self, program_widget):
        self.program_widget = program_widget
        button_width=150
        self.stardice = None
        self.figure = bokeh.plotting.figure(
            width=500, height=500,
            title="Telescope Altitude and Azimuth",
            x_axis_type=None, y_axis_type=None,
            tools="pan, wheel_zoom, reset")
        logging.debug(f'{self.figure.title.text_color},{self.figure.title.text_font_size}')
        self.figure.x_range = bokeh.models.Range1d(-105, 105)
        self.figure.y_range = bokeh.models.Range1d(-105, 105)

        self.connect_button = bokeh.models.Toggle(label='Connected', width=button_width)
        self.connect_button.on_event('button_click', self.connect_stardice)
        self.authenticate_button = bokeh.models.Toggle(label="Request control", disabled=True, width=button_width)
        self.control_buttons = {'slit_button': bokeh.models.Toggle(label='Open slit', width=button_width),
                                'program_button': bokeh.models.Button(label='Upload program', width=button_width),
                                'obs_button': bokeh.models.Toggle(label='Observation Active', width=button_width),
                                'focus_increase_button': bokeh.models.Button(label='Increase Focus offset', width=button_width),
                                'focus_decrease_button': bokeh.models.Button(label='Decrease Focus offset', width=button_width),
                                'park_button': bokeh.models.Toggle(label='Park', width=button_width),}
        self.control_on(False)
        self.control_buttons['program_button'].on_event('button_click', self.upload_program)
        self.control_buttons['slit_button'].on_event('button_click', self.open_slit)
        self.control_buttons['obs_button'].on_event('button_click', self.observation_loop)
        self.control_buttons['park_button'].on_event('button_click', self.park)
        self.control_buttons['focus_increase_button'].on_event('button_click', self.focus_increase)
        self.control_buttons['focus_decrease_button'].on_event('button_click', self.focus_decrease)
        # JavaScript callback to capture login and password
        login_input = bokeh.models.TextInput(visible=False)
        password_input = bokeh.models.TextInput(visible=False)
        input_ready = bokeh.models.Toggle(visible=False)
        callback = bokeh.models.CustomJS(args=dict(authenticate_button=self.authenticate_button, login_input=login_input, password_input=password_input, input_ready=input_ready), code="""
        if (authenticate_button.active){
        const login = prompt("Please enter your login:", "");
        if (login !== null) {
            const password = prompt("Please enter your password:", "");
            if (password !== null) {
                login_input.value = login;
                password_input.value = password;
                input_ready.active = true;
            }
        }}
    """)
        def process_login(attr, old, new):
            if new == True:
                input_ready.active = False
                result = self.handle_login_event(
                    login_input.value, password_input.value)
        
        def logout(active):
            if not active:
                if hasattr(self.stardice, 'logout'):
                    self.stardice.logout()
                self.control_on(False)

        self.authenticate_button.js_on_click(callback)
        self.authenticate_button.on_click(logout)
        input_ready.on_change('active', process_login)

        self.data = bokeh.models.ColumnDataSource(data=dict(
            name=[], alt=[], az=[], airmass=[],
            ra=[], dec=[], x=[], y=[]))
        self.telescope_data = bokeh.models.ColumnDataSource(data=self.process_telescope_status())

        self.sources = self.figure.scatter(x='x', y='y',  source=self.data)
        self.telinfo = self.figure.scatter(x='telx', y='tely',  source=self.telescope_data, color='red', size=10)
    
        self.pointing_model = pointing_model.PointingModel_Extended(pointing_model_params)

        self.hovertool = bokeh.models.HoverTool(tooltips=[
            ("name", "@name"),
            ("alt", "@alt"),
            ("az", "@az"),
            ], mode='mouse', renderers=[self.sources])
        self.hovertel = bokeh.models.HoverTool(tooltips=[
            ("ha", "@telha"),
            ("ra", "@telra"),
            ("dec", "@teldec"),
            ("alt", "@telalt"),
            ("az", "@telaz"),
            ("dome", "@domeaz"),
            ("band", "@band"),
            ("focus", "@focus"),
            ("camtemp", "@camtemp"),
            ("volet", "@volet"),
            ], mode='mouse', renderers=[self.telinfo])
        self.figure.add_tools(self.hovertool, self.hovertel)

        self.figure.add_layout(
            bokeh.models.Arrow(line_width=5,
                               x_start="domex", y_start="domey", x_end="domexend", y_end="domeyend",
                               source=self.telescope_data))
        self.figure.title.text = 'Telescope status: Disconnected'
        self.stardice = None
        self._draw_axis()

    def upload_program(self, active):
        program = dict(self.program_widget.source.data)
        logging.info(self.stardice.set_observation_program(program['targets'], program['times']))

    def open_slit(self, new):
        if new.model.active:
            logging.info(self.stardice.open_slit())
        else:
            logging.info(self.stardice.stop_slit_opening())

    def park(self, new):
        status = self.stardice.status()
        if new.model.active:
            if status['observation_status'] in ['PARKING', 'PARK']:
                logging.debug('Telescope already parking or parked')
            else:
                logging.info(self.stardice.park())
        else:
            pass

    def observation_loop(self, new):
        if new.model.active:
            logging.info(self.stardice.start_observations())
            self.observing(True)
        else:
            logging.info(self.stardice.stop_observations())
            self.observing(False)
            
    def observing(self, value=True):
        for button in ['park_button', 'program_button', 'slit_button']:
            self.control_buttons[button].disabled = value

    
    def connect_stardice(self, new):
        if new.model.active:
            try:
                ssh.ssh_tunnel(config['webapp.serverport'], '127.0.0.1') # webcam
                self.stardice = pipelet3.socketrpc.SecureRPCClient(f'http://127.0.0.1:{config["webapp.serverport"]}')
                self.authenticate_button.disabled = False
                self.program_widget.set_table(*self.stardice.get_observation_program())
                self.program_widget.set_target_list(self.stardice.get_available_targets())
            except Exception as e:
                logging.error(e)
        else:
            self.authenticate_button.active = False
            self.authenticate_button.disabled = True
            if self.stardice is not None:
                self.stardice.close()
            self.stardice = None

    def control_on(self, value=True):
        for button in self.control_buttons.values():
            button.disabled = not value
        self.authenticate_button.active = value
        if value:
            self.authenticate_button.label = 'Resign control'
        else:
            self.authenticate_button.label = 'Request control'
            
    def handle_login_event(self, login, password):
        logging.debug(f'Authentication request {login}')
        result = self.stardice.login(login, password)
        logging.debug(f'Received {result}')
        if result is True:
            logging.info(f'{login} is authenticated as observer for this session')
            self.control_on()
        elif result is False:
            logging.info('Authentication failed')
            self.control_on(False)
        else:
            logging.info(result)
            self.control_on(False)

    def focus_increase(self):
        logging.info(self.stardice.adjust_focus(0.1))

    def focus_decrease(self):
        logging.info(self.stardice.adjust_focus(-0.1))
        
    def _draw_axis(self, alt_interval=10, az_interval=45):
        ''' Draw the polar axis grid
        '''
        self.figure.annular_wedge(x=0, y=0, inner_radius=0, outer_radius=90, start_angle=0, end_angle=2*np.pi, color="black", alpha=0.1)
        for i in range(10, 91, alt_interval):
            self.figure.annular_wedge(x=0, y=0, inner_radius=i, outer_radius=i, start_angle=0, end_angle=2*np.pi, color="black", alpha=0.1, syncable=False)
    
        # Add an angular axis
        for angle in np.arange(0, 360, az_interval):
            angle = np.radians(angle)
            self.figure.ray(x=0, y=0, length=90, angle=-angle, angle_units="rad", line_color="black", line_alpha=0.3)
            self.figure.text(x=95*np.cos(angle), y=95*-np.sin(angle), text=[f"{int(angle*180/np.pi)}°"], text_align="center", text_baseline="middle")

    def get_widget(self):
        return bokeh.layouts.row(self.figure, bokeh.layouts.column(self.connect_button, self.authenticate_button, *[button for button in self.control_buttons.values()]))

    def update_objects(self):
        #self._draw_axis()
        #logging.info(f'figure size: {self.figure.height}, {self.figure.width}')
        alt, az = np.array([self.get_target_altaz(entry['HA'], entry['RA'], entry['DEC']) for entry in targets]).T
        goods = alt>0
        alt = alt[goods]
        az = az[goods]
        x, y = polar_coordinate_to_xy(alt, az)
        self.data.data=dict(name=targets['TARGET'][goods], alt=alt, az=az, x=x, y=y)
        self.telescope_data.data = self.process_telescope_status()
        return self.data.data

    
    def get_target_altaz(self, ha, ra, dec):
        if ha == 'IDLE':
            ra_app, dec_app = self.pointing_model.radec_J2000_to_radec_apparent(float(ra), float(dec))
            ha_app, hdec_app = self.pointing_model.radec_to_hadec(ra_app, dec_app, mjd=None)
        else:
            ha_app, hdec_app = float(ha), float(dec)
        alt, az = self.pointing_model.hadec_to_altaz(ha_app, hdec_app)
        return alt, az

    def process_telescope_status(self):
        if self.stardice is not None:
            try:
                status = self.stardice.status()
            except Exception as e:
                logging.error(f'{e}')
                self.figure.title.text = 'Telescope status: Connection error'
                #self.connect_button.active=[False]
                #self.stardice = None
                #self.figure.title.text = "Telescope Altitude and Azimuth: Disconnected"
                #return
            ha, dec = self.pointing_model(status['mount']['delta'], status['mount']['tau'])
            ha, dec = pointing_model.no_side(ha, dec)
            alt, az = self.pointing_model.hadec_to_altaz(ha, dec)
            ra, _ = self.pointing_model.hadec_to_radec(ha, dec)
            x, y = polar_coordinate_to_xy(alt, az)
            domex, domey = polar_coordinate_to_xy(0, status['dome']['azimuth'])
            domexend, domeyend = polar_coordinate_to_xy(-5, status['dome']['azimuth'])
            self.figure.title.text = format_status(status)
            if (status['observation_status'] in ['PARKING', 'PARKED']) and not self.control_buttons['park_button'].active:
                self.control_buttons['park_button'].active = True
            elif (status['observation_status'] not in ['PARKING', 'PARKED']) and self.control_buttons['park_button'].active:
                self.control_buttons['park_button'].active = False
            if (status['observation_status'] != 'OPENING') and self.control_buttons['slit_button'].active:
                self.control_buttons['slit_button'].active = False
            return dict(
                telha=[ha],
                telra=[ra],
                teldec=[dec],
                teldelta=[status['mount']['delta']],
                teltau=[status['mount']['tau']],
                telalt=[alt],
                telaz=[az],
                telx=[x],
                tely=[y],
                domeaz=[status['dome']['azimuth']],
                domex=[domex],
                domey=[domey],
                domexend=[domexend],
                domeyend=[domeyend],
                band=[status['filterwheel']['band']],
                focus=[status['focuser']['position']],
                camtemp=[status['camera']['temperature']],
                volet=[status['ps']['volet']],
            )
        else:
            self.figure.title.text = 'Telescope status: Disconnected'
            return dict(
                telha=[np.nan],
                telra=[np.nan],
                teldec=[np.nan],
                teldelta=[np.nan],
                teltau=[np.nan],
                telalt=[np.nan],
                telaz=[np.nan],
                telx=[np.nan],
                tely=[np.nan],
                domeaz=[np.nan],
                domex=[np.nan],
                domey=[np.nan],
                domexend=[np.nan],
                domeyend=[np.nan],
                band=[np.nan],
                focus=[np.nan],
                camtemp=[np.nan],
                volet=[''],
            )            
if __name__ == '__main__':
    tw = TelescopeWidget()
