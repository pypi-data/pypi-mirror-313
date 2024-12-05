
class FakeInstrumentServer():
    def __init__(self):
        self.components = None
    
    def set_state(self, state):
        if self.components is None:
            self.prepare()
        self.state.update(state)

    def get_state(self):
        if self.components is None:
            self.prepare()
        self.state.update(self.meteo.get_meteo())
        return self.state

    def get_image(self):
        import jax
        import jax.numpy as jnp
        import numpy as np
        if self.components is None:
            self.prepare()
        image_state = {'key': jax.random.PRNGKey(42)}
        for c in self.components:
            image_state.update(c.process_state(self.state))
        sources = {}
        for c in self.components:
            sources = c.process_sources(sources, image_state)
        image = jnp.zeros(self.static['shape'])
        for component in self.components:
            image = component.process_image(image, image_state, sources)
        return np.array(image)

    def choices(self):
        return ['start', 'stop']

    def __call__(self, name):
        import subprocess
        import os
        from pipelet3 import socketrpc, rpc
        from stardiceonline.tools.config import config
        import time
        if name.option == 'start':
            print('Starting FakeInstrumentServer')
            rpc.daemonize(self.start, logfile=os.path.expanduser('~/logs/fakeinstrument_log'))
            time.sleep(1.0)
            print('Starting scheduler fake systems drivers')
            result = subprocess.run(['./stardicectl', 'server_start', 'needed', '--dummy'], cwd=config['simu.stardicectl'], capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
            #print('Starting scheduler')
            #result = subprocess.run(['./stardicemain.py', '--fake'], cwd=config['simu.stardicectl'], capture_output=True, text=True)
            #print(result.stdout)
            #print(result.stderr)

        if name.option == 'stop':
            #result = subprocess.run(['killall', 'stardicemain.py'], capture_output=True, text=True)
            #print(result.stdout)
            #print(result.stderr)
            result = subprocess.run(['./stardicectl', 'server_kill', 'all'], cwd=config['simu.stardicectl'], capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
            connection = socketrpc.SecureRPCClient(config['simu.url'])
            connection.shutdown()
            
    def start(self):
        from stardiceonline.tools.config import config
        from pipelet3 import socketrpc
        server = socketrpc.SecureRPCServer(self, url=config['simu.url'], allow_remote_shutdown=True)
        server.start()

    def prepare(self):
        from stardiceonline.simulation.fakecomponents import FakeMeteo, FakeSky, FakeMount, FakeNewton, FakeCamera
        from stardiceonline.tools.datesandtimes import utctime
        self.state = {'band': 'u',
                      'time': utctime(),
                      'exptime': 1,
                      'sunalt': -15,
                      }
        self.static = {'shape': (1128, 1156),
                       'illuregion': ((0,1032), (1,1057))}
        
        self.meteo = FakeMeteo()
        self.components = [FakeSky(self.static), FakeMount(self.static), FakeNewton(self.static),  FakeCamera(self.static)]

if __name__ == '__main__':
     fi = FakeInstrumentServer()
     #fi.start()
