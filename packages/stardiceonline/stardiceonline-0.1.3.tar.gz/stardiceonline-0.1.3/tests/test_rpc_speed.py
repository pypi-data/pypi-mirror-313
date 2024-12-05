from pipelet3 import socketrpc
from pipelet3.rpc import daemonize
import time
import sys
import numpy as np
import logging

class SchedulerTest:
    def __init__(self):
        self.i = 0

    def set_server(self, rpcserver):
        ''' Needed to shutdown
        '''
        self.rpcserver = rpcserver
        
    @socketrpc.make_public
    def echo(self, string):
        return string

    def disconnect(self):
        self.i -= 1
        if self.i == 0:
            self.rpcserver.shutdown()

    def keyword(self, toto='toto', titi='titi'):
        return f'{toto} {titi}'
    
    def register(self):
        self.i += 1

    def status(self):
        return self.i

    def image(self):
        ''' Speed test on big file
        '''
        return np.zeros((1024,1024))

def tic(func, n=1000):
    def f(*args):
        tic = time.time()
        for i in range(n):
            func(*args)
        elapsed = time.time()-tic
        print(f'{elapsed/n*1e6:.2f}μs, {n/elapsed:.1f} request per sec')
        return elapsed / n
    return f

def launch_server():
    server = socketrpc.SecureRPCServer(SchedulerTest(), chunk_size=args.cs, header_size=args.hs, url=args.url)
    server.instance.set_server(server)
    server.start()

def test_client():
    client = socketrpc.SecureRPCClient(chunk_size=args.cs, header_size=args.hs, url=args.url)
    client.register()
    tic(client.echo)('toto')
    image = client.image()
    perreq = tic(client.image)()
    print(f'{image.nbytes / perreq/(2**20):.2f} MB/s')        
    client.disconnect()    
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Test the speed of the rpc system')
    parser.add_argument(
        '-n', '--n-client', default=1, type=int,
        help='Number of parallel clients')
    parser.add_argument(
        '--cs', default=4096, type=int,
        help='Chunk size in bytes')
    parser.add_argument(
        '--hs', default=1024, type=int,
        help='Header size in bytes')
    parser.add_argument(
        '--url', default='http://127.0.0.1:5000', 
        help='Server url')
    
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # This will send logging output to stdout
        ]
    )

    
    daemonize(launch_server, logfile='./speedtest')
    time.sleep(0.5)
    for n in range(args.n_client):
        daemonize(test_client, logfile='./speedtest')
    
