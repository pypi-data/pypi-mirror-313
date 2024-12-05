from pipelet3 import socketrpc
from test_rpc_speed import SchedulerTest
from pipelet3.rpc import daemonize
import threading
import time
import logging


def test_authenticate(tmp_path):
    user_file = tmp_path / 'users.txt'
    socketrpc.add_user(user_file.as_posix(), 'toto', 'titi')

    # test the authentication algo
    a = socketrpc.Authentication(user_file)
    challenge = a.authentication_request('toto')
    response = socketrpc.compute_response(challenge, 'titi')
    assert a.login('toto', response)

    # Lanch the server
    server = socketrpc.SecureRPCServer(SchedulerTest(), url='http://localhost:8888', authentication=a)
    t = threading.Thread(target=server.start, daemon=True)
    t.start()
    time.sleep(0.5)
    client = socketrpc.SecureRPCClient(url='http://localhost:8888')

    # Test connexion without authentication
    assert hasattr(client, 'echo')
    assert not hasattr(client, 'status')
    assert client.echo('toto') == 'toto'

    # Test connexion with authentication
    client.login('toto', 'titi')
    assert hasattr(client, 'status')
    assert client.status() == 0

    # Test keyword arguments
    assert client.keyword(titi='titi', toto='toto') == 'toto titi'
    assert client.keyword(titi='tata') == 'toto tata'
    assert client.keyword('tata') == 'tata titi'
    
    # Test logout
    client.logout()
    assert not hasattr(client, 'status')

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
        '--url', default='http://127.0.0.1:8888', 
        help='Server url')
    
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # This will send logging output to stdout
        ]
    )

    user_file = './users.txt'
    socketrpc.add_user(user_file, 'toto', 'titi')
    a = socketrpc.Authentication(user_file)

    challenge = a.authentication_request('toto')
    response = socketrpc.compute_response(challenge, 'titi')
    print(a.login('toto', response))

    server = socketrpc.SecureRPCServer(SchedulerTest(), chunk_size=args.cs, header_size=args.hs, url=args.url, authentication=a, single_session=True)
    server.instance.set_server(server)
    t = threading.Thread(target=server.start, daemon=True)
    t.start()
    time.sleep(0.5)
    client = socketrpc.SecureRPCClient(chunk_size=args.cs, header_size=args.hs, url=args.url)
    print(hasattr(client, 'status'))
    client.login('toto', 'titi')
    client2 = socketrpc.SecureRPCClient(chunk_size=args.cs, header_size=args.hs, url=args.url)
