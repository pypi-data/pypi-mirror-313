from platformdirs import user_config_dir
import os
import configparser

appname = "stardiceonline"
appauthor = "stardice"

class Config():
    '''Handle generic configuration of stardiceonline
    '''
    def __init__(self):
        self._filename = os.path.join(user_config_dir(appname), 'stardiceonline.ini')
        self._backup_filename = self._filename.replace('.ini', '.sav')
        self.config = configparser.ConfigParser()
        if os.path.exists(self._filename):
            self.config.read(self._filename)
        else:
            self._default_config()
            self._save()

    def _default_config(self):
        self.config['archive'] = {'local': os.path.expanduser('~/ohp_archive'),
                                  'ssh': '/data/stardiceot1',
                                  'mirror':'http://supernovae.in2p3.fr/stardice/stardiceot1/'}
        self.config['ssh'] = {'proxy': 'cca.in2p3.fr',
                              'proxyuser': 'betoule',
                              'user': 'dice',
                              'host': '193.50.62.37',
                              'telhost':'192.168.200.178',
                              }
        self.config['webapp'] = {'host': 'localhost',
                                 'port': '5006',
                                 'serverport': '5000',
                                 'webcamport': '9983',
                                 }
        self.config['simu'] = {'meteolog': '',
                               'url': '',
                               'stardicectl': os.path.expanduser('~/soft/stardice/instruments/stardice_ot1/observations'),
                               }

    def _save(self, backup=False):
        if not os.path.exists(user_config_dir(appname)):
            os.makedirs(user_config_dir(appname))
        if backup:
            fname = self._backup_filename
        else:
            fname = self._filename
        with open(fname, 'w') as configfile:
            self.config.write(configfile)

    def _restore(self):
        if os.path.exists(self._backup_filename):
            self.config.read(self._backup_filename)
            self._save()
            print('Configuration file restored to saved state')
        else:
            print('No saved configuration available')
        
    def choices(self):
        choices = [f'{section}.{key}' for section in self.config for key in self.config[section]] + ['show', 'reset', 'simulation_mode', 'real_mode']
        return choices

    def __getitem__(self, name):
        section, key = name.split('.')
        return self.config[section][key]
    
    def __call__(self, args):
        name = args.option
        if name not in self.choices():
            raise ValueError('Unsupported configuration parameter {name}. Available options {self.choices()}')
        if name == 'show':
            return '\n'.join([f'{section}.{key}: {self.config[section][key]}' for section in self.config for key in self.config[section]])
        if name == 'reset':
            self._default_config()
            self._save()
            return 'Default settings restored'
        if name == 'simulation_mode':
            if self['simu.meteolog']:
                return f'Already in simulation mode'
            else:
                self._save(backup=True)
                new_archive = self.config['archive']['local'] + '_simu'
                if not os.path.exists(new_archive):
                    os.makedirs(new_archive)
                if not os.path.exists(os.path.join(new_archive, 'gaia')):
                    os.symlink(os.path.join(self.config["archive"]["local"], 'gaia'), os.path.join(new_archive, 'gaia'))
                self.config['simu'].update({'meteolog': os.path.join(self.config['archive']['local'], 'meteo'),
                                            'url': 'http://127.0.0.1:9999'})
                self.config['archive']['local'] = new_archive
                self.config['ssh'] = {'proxy': '',
                                      'proxyuser': '',
                                      'user': os.getlogin(),
                                      'host': 'localhost',
                                      'telhost':'localhost',
                                      }
                self._save()
                return f'Switched to simulation mode with working directory {self.config["archive"]["local"]}'
        if name == 'real_mode':
            if not self['simu.meteolog']:
                return f'Already in real mode'
            else:
                self._restore()
                return f'Back to real mode'
        section, key = name.split('.')
        if args.value is not None:    
            self.config[section][key] = args.value
            self._save()
        else:
            return self.config[section][key]
        
config = Config()
