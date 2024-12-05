import os
import sys
import xmlrpc.server
import xmlrpc.client

def daemonize(target, logfile=None):
    ''' Logfile should be provided if the terminal is being closed after launching the daemon. Else the closure of stdout will cause issues.
    '''
    try:
        pid = os.fork()
        if pid > 0:
            # first parent return
            return
    except OSError as e:
        print("fork #1 failed: %d (%s)" % (e.errno, e.strerror), file=sys.stderr)
        sys.exit(1)
    os.setsid()
    if logfile is not None:
        log = open(logfile, 'a')
    else:
        log = None
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            print("starting daemon with PID %d" % pid)
            sys.exit(0)
    except OSError as e:
        print("fork #2 failed %d (%s)" % (e.errno, e.strerror), file=sys.stderr)
        sys.exit(1)
    if log is not None:
        redirect_stream(sys.stdin,  log)
        redirect_stream(sys.stdout, log)
        redirect_stream(sys.stderr, log)
    target()
    sys.exit(0)


def redirect_stream(system_stream, target_stream):
    if target_stream is None:
        target_fd = os.open(os.devnull, os.O_RDWR)
    else:
        target_fd = target_stream.fileno()
    os.dup2(target_fd, system_stream.fileno())


class Server(xmlrpc.server.SimpleXMLRPCServer):
    def __init__(self, instance, url):
        addr = (url.replace("http://", "").split(":")[0], int(url.split(":")[-1]))
        xmlrpc.server.SimpleXMLRPCServer.__init__(
            self, addr, allow_none=True, logRequests=False
        )
        self.instance = instance

    def _listMethods(self):
        methods = xmlrpc.server.list_public_methods(self.instance)
        return methods

    def _methodHelp(self, method):
        f = getattr(self.instance, method)
        return inspect.getdoc(f)

    # def _serve_forever(self):
    #    while not self.instance._status == "stop":
    #        self.handle_request()

    def main(self):
        # redirect_stream(sys.stdin, None)
        # redirect_stream(sys.stdout, None)
        # redirect_stream(sys.stderr, None)

        self.register_function(self._listMethods, "__dir__")
        self.register_function(self._listMethods, "system.listMethods")
        self.register_function(self._listMethods, "trait_names")
        self.register_function(self._listMethods, "_getAttributeNames")
        self.register_function(self._methodHelp, "system.methodHelp")
        # self.register_function(self.exit, "exit")

        # logging.info(str(self.instance))
        for method in self._listMethods():
            f = getattr(self.instance, method)
            # self.register_function(logged_call(f, self.lock), method)
            self.register_function(f, method)
            # logging.info('registering method '+method)

        # logging.info("server is up and listening at http://%s:%d." % self.socket.getsockname())
        print("server is up and listening at http://%s:%d." % self.socket.getsockname())
        self.instance.start_sweep_vehicle(self)
        self.serve_forever()
        self.server_close()
        print("Down")


class ProxyWithCompletion(xmlrpc.client.ServerProxy):
    def __dir__(self):
        return self.system.listMethods()
