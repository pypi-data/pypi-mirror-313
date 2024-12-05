from stardiceonline.archive.archive import local_archive
from stardiceonline.tools.config import config
import ast

import os
class Process():
    def __call__(self, args):
        from stardiceonline.processing import pipeline
        import pipelet3
        from pipelet3.cli import Connection
        Ponline = pipelet3.Graph(
            '''
            list_directory -> new_image ->[isstar] photometry -> astrometry -> forced_photometry
            new_image ->[isled] led_photometry
            new_image ->[issphere] sphere_photometry
            ''',
            pipeline.__dict__,
            state_file=os.path.join(config['archive.local'], "pipelet_stardice.pkl")
        )
        connection = Connection(Ponline, url='http://localhost:7173')
        if args.option == 'status':
            connection.status({}, Ponline)
        elif args.option == 'stop':
            connection.stop({}, Ponline)
        elif args.option == 'live':
            connection.run({}, Ponline)
            connection.poll(Ponline, local_archive.sync)
            connection.poll(Ponline, local_archive.sync_meteo, interval=60)
            connection.watch(Ponline, [local_archive.current_directory()], 'new_image', '*.fits')
        elif args.option == 'inspect':
            connection.inspect(Ponline.namespace['match_expnum'], int(args.value))
        elif args.option == 'reset':
            print(connection.connection.reset(args.value, 'Done'))
        elif args.option == 'reset_failed':
            print(connection.connection.reset(ast.literal_eval(args.value), 'Failed'))
        else:
            connection.run({}, Ponline)
            connection.push(Ponline, 'list_directory', [args.option])
        
    def choices(self):
        try:
            choices = local_archive.ls_nights()
        except ValueError:
            choices = []
        except FileNotFoundError:
            choices = []
        return choices + ['live', 'status', 'inspect', 'stop', 'reset', 'reset_failed']
