from stardiceonline.tools.config import config
from stardiceonline.tools.datesandtimes import night_name

import os


def red(s):
    ''' Return a string colored in red'''
    return f'\033[91m{s}\x1b[0m'
    
def green(s):
    ''' Return a string colored in green'''
    return f'\033[92m{s}\x1b[0m'

def blue(s):
    return f'\033[94m{s}\x1b[0m'


class SSHArchive():
    def __init__(self, directory=config['archive.ssh']):
        self.directory = directory

    def ls_nights(self):
        from stardiceonline.archive import ssh
        return [d.decode() for d in ssh.ssh_command(['ls', self.directory]).split()]

class LocalArchive():
    ''' Manage the local image database'''
    special = ['meteo', 'gaia']
    def __init__(self, directory=config['archive.local']):
        self.directory = directory

    def ls_nights(self):
        if not self.directory:
            raise ValueError('Local archive not configured. Use "stardiceonline config archive.local [directory]" to set up')
        return [d for d in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, d)) and d not in self.special]

    def choices(self):
        return ['list', 'retrieve', 'sync', 'sync_meteo']

    def list(self, value):
        distant = SSHArchive().ls_nights()
        local = self.ls_nights()
        all = set(distant)
        all.update(local)
        all = list(all)
        all.sort()
        return ' '.join([blue(d) if d not in local else green(d) for d in all])

    def retrieve(self, value):
        from stardiceonline.archive import ssh
        return ssh.rsync(os.path.join(config['archive.ssh'], value), self.directory)

    def current_directory(self):
        return os.path.join(self.directory, night_name())
    
    def sync(self, value=None):
        from stardiceonline.archive import ssh
        # The early creation of the directory avoid failures of other
        # processes if the rsync fails or is too slow
        path = os.path.join(self.directory, night_name())
        if not os.path.exists(path):
            os.makedirs(path)
        return ssh.rsync(os.path.join(config['archive.ssh'], night_name()), self.directory)

    def sync_meteo(self, value=None):
        from stardiceonline.archive import ssh
        return ssh.rsync('~/meteo', self.directory)

    def last_meteo_files(self):
        import glob
        flist = glob.glob(os.path.join(self.directory, 'meteo', '*.csv'))
        flist.sort()
        return flist
    #os.path.join(self.directory, 'meteo', f'meteo_{datetime.now().strftime("%Y-%m-%d")}.csv')
    
    
    def __call__(self, args):
        if args.option in self.choices():
            return getattr(self, args.option)(args.value)
        
local_archive = LocalArchive()
