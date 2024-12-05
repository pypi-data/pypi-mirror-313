import argparse
import difflib
import time

# import socket

# socket.setdefaulttimeout(10)

from . import scheduler, rpc, worker, socketrpc, external_events


class Connection():
    def __init__(self, graph, url='http://localhost:7173'):
        self.url = url
        try:
            self.connection = socketrpc.SecureRPCClient(url)
        except ConnectionRefusedError:
            print("No server available, launching one")
            sched = scheduler.Scheduler(graph)
            server = socketrpc.SecureRPCServer(sched, url, allow_remote_shutdown=True)
            rpc.daemonize(server.start)
            time.sleep(0.5)
            self.connection = socketrpc.SecureRPCClient(url)
            self.connection.start_sweep_vehicle()
        except Exception as e:
            print(f"Internal error, stopping: {e}")
            self.connection.stop()

    
    def stop(self, args, graph):
        self.connection.shutdown()
        for i in range(10):
            try:
                self.connection.status()
            except Exception as e:
                break
            time.sleep(1)
        else:
            import psutil
            print("Server is slow to terminate, probably due to uncatch exception locking the scheduler. Killing explicitly, state may not be saved.")
            process = psutil.Process(self.connection.get_pid())
            process.terminate()

    def diff(self, args, graph):
        running_code = self.connection.get_graph()
        for func_name in graph.source_code:
            if func_name not in running_code:
                print(
                    "Current code contains method {func_name} not present in the running graph:"
                )
                print(graph.source_code[func_name])
                continue
            diff = "".join(
                [
                    l
                    for l in difflib.context_diff(
                        running_code[func_name].splitlines(keepends=True),
                        graph.source_code[func_name].splitlines(keepends=True),
                        fromfile="Running code",
                        tofile="Current code state",
                    )
                    if l
                ]
            )
            if diff:
                print(f"Method {func_name} in current code differs from the running graph:")
                print(diff)

    def run(self, args, graph, n_workers=1, debug=False):
        if debug:
            wid = worker.Worker(self.url)
            wid.main(local=True)
        for i in range(n_workers):
            wid = worker.Worker(self.url, graph.namespace)
            print(f"Lanching worker {wid.wid}")
            rpc.daemonize(wid.main)
    
    def watch(self, graph, directories, process, pattern='*'):
        wid = external_events.NewFileWatcher(self.url, graph.namespace, directories, process, pattern)
        print(f"Watching for new files in directories {directories} to be fed to '{process}'")
        rpc.daemonize(wid.main)

    def poll(self, graph, process, interval=2):
        wid = external_events.PollingWorker(self.url, graph.namespace, process, interval=interval)
        print(f"Start polling be fed to '{process}'")
        rpc.daemonize(wid.main)

    
    def push(self, graph, process, tasks):
        if process in graph.processes:
            for t in tasks:
                self.connection.push_task(process, t)
        else:
            print(f"{process} is not a processing step: {list(graph.processes.keys())}")
    
    
    def status(self, args, graph):
        status = self.connection.status()
        print("Scheduling status:")
        print("------------------")
        for k in status:
            print(f"{k}: {status[k]}")
    
    
    def inspect(self, task_filter, value):
        print(self.connection.inspect(task_filter, value))

    def reset(self, args, graph):
        print(self.connection.reset(args.process, args.status))

def main(graph):
    global connection
    parser = argparse.ArgumentParser(description="Launch or manage a pipelet instance.")
    parser.add_argument("--url", default="http://localhost:7173", help="Server url")
    subparsers = parser.add_subparsers(help="Let us see")
    parser_diff = subparsers.add_parser(
        "diff", help="Display differences between computed and current code"
    )
    parser_diff.set_defaults(func=diff)

    parser_stop = subparsers.add_parser("stop", help="Shutdown the computation")
    parser_stop.set_defaults(func=stop)

    parser_run = subparsers.add_parser("run", help="Add workers to the working pool")
    parser_run.add_argument(
        "-n", "--n-workers", type=int, default=1, help="Number of workers to start"
    )
    parser_run.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Start a normal process instead of a daemon and prevent catching of processing exceptions to ease debugging",
    )
    parser_run.set_defaults(func=run)

    parser_watch = subparsers.add_parser("watch", help="Look for new file appearing in directories to add to the task list")
    parser_watch.add_argument(
        "-d", "--directories", type=str, nargs='+', help="Directories to be watched for"
    )
    parser_watch.add_argument(
        "-p",
        "--process",
        type=str,
        nargs=1,
        help="Target process for the watch list",
    )
    parser_watch.set_defaults(func=watch)

    parser_push = subparsers.add_parser("push", help="Add a task to the task queue")
    parser_push.add_argument(
        "task", nargs="+", help="Name of the processing step and metadata of the task"
    )
    parser_push.set_defaults(func=push)

    parser_status = subparsers.add_parser(
        "status", help="Print the scheduler status report"
    )
    parser_status.set_defaults(func=status)

    parser_reset = subparsers.add_parser(
        "reset", help="Reque failed tasks"
    )
    parser_reset.set_defaults(func=reset)
    parser_reset.add_argument(
        "--status",
        choices=['Failed', 'Done'],
        default='Failed',
        help="Requeue all Failed tasks (default) or all completed tasks. In general requeing completed makes little sense, but can be useful in the development phase when task completes but do not return the proper results",
    )
    parser_reset.add_argument(
        "--process",
        default='all',
        help="Requeue only tasks associated to the specified processing stage. If not specify all tasks will be requeued."
    )

    parser_inspect = subparsers.add_parser("inspect", help="inspect various products")
    parser_inspect.add_argument(
        "--failed",
        type=int,
        default=-1,
        help="Display the task ids of failed task, or print the task corresponding to a given task id",
    )
    parser_inspect.set_defaults(func=inspect)

    args = parser.parse_args()

    #connection = rpc.ProxyWithCompletion(args.url)
    if hasattr(args, "func"):
        args.func(args, graph)
    return connection
