import subprocess
import webbrowser
from stardiceonline.tools.config import config

import os

class ServerStart():
    def __init__(self):
        pass

    def __call__(self, args):
        return subprocess.check_call(['bokeh',
                                      'serve',
                                      '--port',
                                      config['webapp.port'],
                                      '--address', config['webapp.host'],
                                      os.path.join(__path__[0], 'online.py'),
                                      os.path.join(__path__[0], 'monitoring.py'),
                                      os.path.join(__path__[0], 'visibility.py'),
                                      #os.path.join(__path__[0], 'program_widget.py'),
                                      '--show'])

    def choices(self):
        return ['serve']


