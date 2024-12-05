from . import rpc, socketrpc
import threading
import time
import signal
import queue
import traceback

class Worker(object):
    def __init__(self, addr, env):
        self.env = env
        #self.server = rpc.ProxyWithCompletion(addr)
        self.server = socketrpc.SecureRPCClient(addr)
        self.wid = self.server.register()
        self.running = True
        self.comm_lock = threading.Lock()

    def handler(self, sig, frame):
        print("Signal caught, shutting down")
        self.running = False

    def poll(self):
        while self.running and threading.main_thread().is_alive():
            try:
                with self.comm_lock:
                    status = self.server.poll(self.wid)
                if status["status"] != "Registered":
                    print(f"Worker {self.wid} scheduled for shutdown")
                    self.running = False
            except Exception as e:
                print(
                    f"Communication problem, worker {self.wid} scheduled for shutdown: {type(e).__name__} - {e}"
                )
                self.running = False
            time.sleep(1)
        try:
            with self.comm_lock:
                self.server.disconnect(self.wid)
        except Exception as e:
            print(
                f"Unable to warn the scheduler for the deconnection of worker {self.wid} due to unexpected exception: {e}"
            )

    def process(self):
        with self.comm_lock:
            self.code = self.server.get_graph()
        #self.env = {}
        #for f in self.code:
        #    exec(self.code[f], self.env)
        while self.running and threading.main_thread().is_alive():
            with self.comm_lock:
                try:
                    task = self.server.get(self.wid)
                except Exception as e:
                    print(
                        f"Caught an unexpected exception: {type(e).__name__} - {e}, going down"
                    )
                    self.running = False
                    continue
            if task is None:
                time.sleep(1)
                continue
            try:
                name = task.process_name
                #result = eval(f'{name}({task["argument"]})', self.env)
                result = self.env[name](task.argument)
                with self.comm_lock:
                    self.server.task_done(self.wid, result)
            except Exception as e:
                with self.comm_lock:
                    self.server.task_failed(self.wid, traceback.format_exception(type(e), e, e.__traceback__))
        print(f"Worker {self.wid} complete.")

    def main(self, wait=True, local=False):
        """Run the worker loop

        Use the wait option for a worker running as an independant process.
        """
        if wait:
            # TODO Make sure that we are in the main thread else fail gracefully
            # Set up interrupt handling
            signal.signal(signal.SIGINT, self.handler)
        # Start the polling loop in a thread
        self.poll_thread = threading.Thread(target=self.poll)
        self.poll_thread.start()
        # And start the processing loop
        if local:
            self.process()
        else:
            self.process_thread = threading.Thread(target=self.process)
            self.process_thread.start()
            if wait:
                self.poll_thread.join()
                self.process_thread.join()
        print(f"Worker {self.wid} shutdown.")
