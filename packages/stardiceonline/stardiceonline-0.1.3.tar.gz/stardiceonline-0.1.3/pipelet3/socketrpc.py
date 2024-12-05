import socket
import ssl
import pickle
import select
import threading
import signal
import struct
import errno
import time
import traceback
import logging
import os
import bcrypt
import hmac
import hashlib

def url_to_host(url):
    hostname, port = (url.replace("http://", "").split(":")[0], int(url.split(":")[-1]))
    return hostname, port


def list_methods(cls):
    # Get all attributes of the class
    all_attributes = dir(cls)
    
    # Filter out special Python methods, private methods, and non-callable attributes
    public_methods = [
        attr for attr in all_attributes 
        if callable(getattr(cls, attr)) 
        and not attr.startswith('__') 
        and not attr.startswith('_')
    ]    
    return public_methods


def load_users(user_file):
    with open(user_file, 'r') as file:
        return {line.split(':')[0]: line.split(':')[1].strip() for line in file}

def set_file_permissions(filepath):
    import stat
    """Set permissions of the file to 600 (read and write for owner only)"""
    try:
        os.chmod(filepath, stat.S_IRUSR | stat.S_IWUSR)
        logging.info(f"File permissions set to 600 for {filepath}")
    except PermissionError:
        logging.error("Could not change file permissions, permission denied.")
    except Exception as e:
        logging.error(f"An error occurred while setting file permissions: {e}")

def compute_response(challenge, password):
    key, salt = challenge
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hmac.new(password_hash, key, hashlib.sha256).digest()

def add_user(user_file, username, password):
    import stat
    # Hash the password with bcrypt
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    # Ensure file exists with correct permissions
    if not os.path.exists(user_file):
        with open(user_file, 'w') as file:
            pass  # Create an empty file
        set_file_permissions(user_file)
    else:
        # Check and correct permissions if necessary
        current_permissions = stat.S_IMODE(os.stat(user_file).st_mode)
        if current_permissions != (stat.S_IRUSR | stat.S_IWUSR):
            logging.warning('Adjusting permission of the authentication file')
            set_file_permissions(user_file)

    # Check if the user already exists
    if os.path.exists(user_file):
        with open(user_file, 'r') as file:
            for line in file:
                if line.split(':')[0] == username:
                    logging.info(f"User {username} already exists.")
                    return False

    # Add the new user to the file
    with open(user_file, 'a') as file:
        file.write(f"{username}:{hashed_password}\n")
        logging.info(f"User {username} added successfully.")
        return True

def make_public(func):
    func._exposed = True
    return func
    
class Authentication():
    def __init__(self, user_file):
        #self.secret_key = secret_key
        self.user_file = user_file
        self.reload()
        self.sessions = {}
        self.challenge = {}

    def reload(self):
        self.users = load_users(self.user_file)

    def authentication_request(self, username):
        if username in self.users:
            logging.info(f'Received an authentication request for user {username}')
            self.challenge[username] = (os.urandom(32), (self.users[username][:29]).encode('utf-8'))
            return self.challenge[username]
        else:
            logging.warning(f'Received an authentication request for unknown user {username}')
            return (os.urandom(32), bcrypt.gensalt())
        
    def login(self, username, response):
        if username in self.challenge:
            expected_response = self.compute_expected_response(username)
            if hmac.compare_digest(response, expected_response):
                self.sessions[username] = True
                logging.info(f'Succesful login of user {username}')
                return True
            else:
                logging.warning(f'Failed login attempt from user {username}')
                return False
        else:
            logging.warning(f'Failed login attempt from user {username}')
            return False
        
    def compute_expected_response(self, username):
        password_hash = self.users[username]
        key, salt = self.challenge[username]
        expected_response = hmac.new(password_hash.encode('utf-8'), key, hashlib.sha256).digest()
        return expected_response
    
    
class SecureRPCServer():
    def __init__(self, instance, url='127.0.0.1:5000', certfile=None, keyfile=None,
                 chunk_size=4096, header_size=1024, allow_remote_shutdown=False,
                 authentication=None, single_session=False):
        host, port = url_to_host(url)
        self.instance = instance
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile        
        self.threads = []
        self.chunk_size = chunk_size
        self.header_size = header_size
        self.authentication = authentication
        self.allow_remote_shutdown = allow_remote_shutdown
        self.session_ids = {}
        self.rpc_methods = {}
        self.single_session = single_session
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def _register_methods(self, session_id):
        def _listMethods():
            return list(self.rpc_methods[session_id].keys())
        rpc_methods = {'_listMethods': _listMethods}
        rpc_methods.update(self._public_methods())

        if self.authentication is None:
            rpc_methods.update(self._private_methods())
        else:
            if self.session_ids[session_id]: # authenticated
                def logout():
                    username = self.session_ids[session_id]
                    logging.info(f'Session {session_id} is no longer authenticated as {username}')
                    self.session_ids[session_id] = ''
                    self._register_methods(session_id)
                rpc_methods.update(self._private_methods())
                rpc_methods['logout'] = logout
            else: # not authenticated
                def login(username, response):
                    if self.authentication.login(username, response):
                        authenticated = [username for username in self.session_ids.values() if username]
                        if self.single_session and (len(authenticated) > 0):
                            return f'The session token is already taken by user {authenticated}'
                        else:
                            self.session_ids[session_id] = username
                            self._register_methods(session_id)
                            return True
                    else:
                        return False
                rpc_methods['authentication_request'] = self.authentication.authentication_request
                rpc_methods['login'] = login
        self.rpc_methods[session_id] = rpc_methods
        

    def _public_methods(self):
        rpc_methods = dict([(method, getattr(self.instance, method)) for method in list_methods(self.instance) if hasattr(getattr(self.instance, method), '_exposed')])
        return rpc_methods
    
    def _private_methods(self):
        rpc_methods = dict([(method, getattr(self.instance, method)) for method in list_methods(self.instance) if not hasattr(getattr(self.instance, method), '_exposed')])
        if self.allow_remote_shutdown:
            rpc_methods['shutdown'] = self.shutdown
        return rpc_methods
    
    def start(self):
        self.running = True
        #if not self.allow_remote_shutdown:
        if self.certfile is not None:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
            self.sock.setblocking(False)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows restarting the server immediately
            self.sock.bind((self.host, self.port))
            self.sock.listen()
            logging.info(f"Server is listening on {self.host}:{self.port}")
            
            while self.running:
                try:
                    conn, addr = self.sock.accept()
                    logging.info(f"Connected by {addr}")
                    if self.certfile is not None:
                        scon = context.wrap_socket(conn, server_side=True)
                    else:
                        scon = conn
                    client_thread = threading.Thread(target=self.handle_client, args=(scon, addr))
                    client_thread.start()
                    self.threads.append((client_thread, scon))
                    #self.handle_client(scon, addr)
                except BlockingIOError as e:
                    time.sleep(1)
                    continue
                except OSError as e:
                    logging.info('Stop listening for new connections...')
                    raise
                #break
                except socket.error as e:
                    # This will catch any socket errors, but we're particularly interested in stopping the loop on shutdown
                    if e.errno != errno.EINTR:
                        raise  # Re-raise if it's not an interrupt error
                    else:
                        logging.info("Server shutting down due to interrupt...")
                        break
            for _t, (t, conn) in enumerate(self.threads, 1):
                logging.info(f'Waiting for connection {_t}/{len(self.threads)}')
                t.join()

    def shutdown(self):
        if hasattr(self.instance, 'shutdown'):
            try:
                self.instance.shutdown(self)
            except Exception as e:
                logging.error(e)
                self.running = False
        else:
            logging.info('\nServer is shutting down...')
            self.running = False

            
    def signal_handler(self, sig, frame):
        logging.info('\nYou pressed Ctrl+C!')
        self.shutdown()
        #sys.exit(0)

    def request_session_id(self):
        session_id = os.urandom(32)
        self.session_ids[session_id] = ''
        return session_id
            
    def handle_client(self, conn, addr):
        conn.setblocking(True)
        with conn:
            logging.info(f"Connected by {addr}")
            session_id = self.request_session_id()
            self._register_methods(session_id)
            while self.running:
                # Read the message length (assuming it's sent as a 4-byte integer)
                try:
                    header = conn.recv(self.header_size)
                except Exception as e:
                    logging.info(f'Server: retrying')
                    time.sleep(0.1)
                    continue
                if not header:
                    logging.info(f"Disconnected by {addr}")
                    break  # Connection closed by client
                
                # Unpack the header to get the length of the message
                message_length = struct.unpack('>I', header[:4])[0]

                # Now receive the actual message
                data = bytearray(header[4:])
                while len(data) < message_length:
                    # Determine how much more we need to read
                    to_read = message_length - len(data)
                    # Read up to the remaining length or the buffer size, whichever is smaller
                    chunk = conn.recv(self.chunk_size if to_read > self.chunk_size else to_read)
                    if not chunk:
                        raise RuntimeError("socket connection broken")
                    data.extend(chunk)
                
                # Now data contains the full message
                request = pickle.loads(data)
                method = request['method']
                params = request['params']
                keys = request.get('keys', {})
            
                # Process the request
                if method in self.rpc_methods[session_id]:
                    try:
                        result = self.rpc_methods[session_id][method](*params, **keys)
                        response = {'result': result, 'error': None}
                    except Exception as e:
                        exception_info = traceback.format_exc()
                        response = {'result': exception_info, 'error': str(e)}
                else:
                    response = {'result': None, 'error': 'Method not found'}
            
                # Serialize the response
                response_data = pickle.dumps(response)
                # Send the length of the response and the response itself
                conn.sendall(struct.pack('>I', len(response_data))+response_data)
        if 'logout' in self.rpc_methods[session_id]:
            self.rpc_methods[session_id]['logout']()
            logging.info(f"Logout from session {session_id}")                
        logging.info(f"Connection to {addr} closed")       


class SecureRPCClient:
    def __init__(self, url='http://127.0.0.1:5000', ssl=False, chunk_size=4096, header_size=1024):
        host, port = url_to_host(url)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self._socket.setblocking(True)
        self._chunk_size = chunk_size
        self._header_size = header_size
        self._created_methods = []
        self._register()
        
    def _register(self):
        for m in self._created_methods:
            delattr(self, m)
        self._created_methods = []
        method_list = self._call('_listMethods')
        if 'login' in method_list:
            def authenticate(username, password):
                challenge = self._call('authentication_request', username)
                response = compute_response(challenge, password)
                whatnot = self._call('login', username, response)
                if whatnot:
                    self._register()
                return whatnot
            
            setattr(self, 'login', authenticate)
            self._created_methods.append('login')
            method_list.remove('login')
            method_list.remove('authentication_request')
        if 'logout' in method_list:
            def logout():
                result = self._call('logout')
                self._register()
                return result
            setattr(self, 'logout', logout)
            self._created_methods.append('logout')
            method_list.remove('logout')
            
        for m in method_list:
            setattr(self, m, self._register_method(m))
      
    def _register_method(self, m):
        self._created_methods.append(m)
        def f(*args, **keys):
            return self._call(m, *args, **keys)
        return f

    def _call(self, method, *params, **kwargs):
        request = {
            'method': method,
            'params': list(params),
            'keys': kwargs,
        }
        data = pickle.dumps(request)
        
        # Send the message prefixed by its length
        self._socket.sendall(struct.pack('>I', len(data))+data)

        # Receive response
        for retry in range(10):
            try:
                header = self._socket.recv(self._header_size)
                break
            except Exception as e:
                logging.info(f'Client: retry')
                
        if not header:
            raise RuntimeError("socket connection broken")
        response_length = struct.unpack('>I', header[:4])[0]
        
        response_data = bytearray(header[4:])
        while len(response_data) < response_length:
            to_read = response_length - len(response_data)
            chunk = self._socket.recv(self._chunk_size if to_read > self._chunk_size else to_read)
            if not chunk:
                raise RuntimeError("socket connection broken")
            response_data.extend(chunk)

        response = pickle.loads(response_data)
        if response['error']:
            raise ValueError(f'Distant exec raised the following error: {response["error"]}\n with the following trace: {response["result"]}')
        return response['result']

    def close(self):
        self._socket.close()
