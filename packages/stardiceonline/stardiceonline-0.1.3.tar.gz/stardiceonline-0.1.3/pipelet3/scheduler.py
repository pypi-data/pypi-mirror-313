import queue
import time
import numpy as np
import threading
from . import processing_graph
import pickle
import os

class Scheduler:
    def __init__(self, graph, root_directory="./"):
        self.state_file = graph.state_file
        self.graph = graph
        self.root_directory = root_directory
        self._status = "up"
        self.queue = queue.Queue()
        self.completed_tasks = queue.Queue()
        self.done = {}
        self.failed_tasks = {}
        self.workers = {}
        self.disconnected_workers = {}
        self._worker_id = 0
        self.running_tasks = {}
        self.wid_lock = threading.Lock()
        self._task_id = 0
        if os.path.exists(self.state_file):
            self.load_state()

    def load_state(self):
        with open(self.state_file, "rb") as fid:
            self.done = pickle.load(fid)
            self.failed_tasks = pickle.load(fid)
        for (process_name, argument), result in self.done.items():
            children = self.graph.processes[process_name].children
            for child in children:
                task = processing_graph.Task(process_name, argument)
                task.result = result
                try:
                    child.pass_through(task, self)
                except Exception as e:
                    print(f'An exception was catched when processing the result of task {(task.process_name, task.argument)}')
                    print('The function should have return a list of hashable items')
                    print(e)
                
        print("Saved state loaded")

    def save_state(self):
        with open(self.state_file, "wb") as fid:
            pickle.dump(self.done, fid)
            pickle.dump(self.failed_tasks, fid)
        print("State saved")

    def handle_completed_tasks(self):
        while self.completed_tasks.qsize():
            task = self.completed_tasks.get()
            children = self.graph.processes[task.process_name].children
            for child in children:
                try:                
                    child.pass_through(task, self)
                except Exception as e:
                    print(f'An exception was catched when processing the result of task {(task.process_name, task.argument)}')
                    print('The function should have return a list of hashable items')
            self.done[(task.process_name, task.argument)] = task.result
            self.completed_tasks.task_done()

    def start_sweep_vehicle(self):
        self.sweep_thread = threading.Thread(target=self.sweep_vehicle)
        self.sweep_thread.start()

    def sweep_vehicle(self):
        while self._status == "up":
            t = time.time()
            sweep = []
            for wid in self.workers:
                worker = self.workers[wid]
                if worker["status"] != "Down":
                    if t - worker["lastseen"] > 10:
                        print(
                            f"Worker {wid} has not been seen for a while. Assumed to be dead"
                        )
                        sweep.append(wid)
                self.handle_completed_tasks()
            for wid in sweep:
                self.disconnect(wid)
            if not self.queue.qsize():
                for l in self.graph.links:
                    for c in self.graph.links[l]:
                        c.push_available(self)
            time.sleep(0.2)
        # Stopping the server
        # wait for the effective deconnection of all clients
        while np.any(
            [status["status"] != "Down" for wid, status in self.workers.items()]
        ):
            time.sleep(0.1)
        print("Stop servicing")
        self._status = "stop"
        self.save_state()
        self.server.running = False
        
    def register(self):
        with self.wid_lock:
            wid = self._worker_id
            self._worker_id = self._worker_id + 1
        self.workers[wid] = {
            "status": "Registered",
            "task": None,
            "lastseen": time.time(),
        }
        return wid

    def shut_worker_down(self, wid):
        self.workers[wid]["status"] = "Shutdown"

    def disconnect(self, wid):
        try:
            worker = self.workers.pop(wid)
            worker["status"] = "Down"
            self.disconnected_workers[wid] = worker
        except KeyError:
            pass

    def poll(self, wid):
        try:
            worker_status = self.workers[wid]
            worker_status["lastseen"] = time.time()
            return worker_status
        except KeyError:
            return {"status": "Down", "task": None, "lastseen": 0}

    def get_graph(self):
        return self.graph.source_code

    def status(self):
        status_report = {
            "status": self._status,
            "Registered": len(self.workers),
            "Down": len(self.disconnected_workers),
            "Queued": self.queue.qsize(),
            "Done": len(self.done),
            "Running": len(self.running_tasks),
            "Failed": len(self.failed_tasks),
        }
        return status_report

    def get(self, wid):
        status = self.poll(wid)
        if status["status"] == "Registered":
            try:
                task = self.queue.get(timeout=0.2)
            except queue.Empty:
                return None
            status["task"] = task.tid
            self.running_tasks[task.tid] = task
        else:
            task = None
        return task

    def inspect(self, task_filter, value):
        results = []
        #queue = self.failed_tasks
        queue = self.done
        for status, queue in [('Success', self.done), ('Failed', self.failed_tasks)]:
            for t in queue:
                try:
                    if task_filter(t, t[1], value):
                        results.append((t, status, queue[t]))
                except Exception as e:
                    print(t)
                    print(queue[t])
                    print(e)
        return results
        #d = {"Failed": self.failed_tasks}
        #if tid == -1:
        #    return str(d[status])
        #else:
        #    print(d[status][tid])
        #    return d[status][tid]

    def task_done(self, wid, result):
        status = self.poll(wid)
        tid = status["task"]
        task = self.running_tasks.pop(tid)
        if result is None:
            result = []
        task.result = result
        #print(task.result)
        self.completed_tasks.put(task)
        self.queue.task_done()

    def task_failed(self, wid, exception):
        print(f'task failed {exception}')
        status = self.poll(wid)
        tid = status["task"]
        task = self.running_tasks.pop(tid)
        task.result = exception
        self.failed_tasks[(task.process_name, task.argument)] = task.result
        self.queue.task_done()

    def reset(self, task='all', status='Failed'):
        #if process_name == 'all':
        process_name = set(self.graph.processes.keys())
        #    print(process_name)
        if status == 'Failed':
            queue = self.failed_tasks
        elif status == 'Done':
            queue = self.done
        requeue = []
        if task in process_name:
            for p, a in queue:
                if p == task:
                    requeue.append((p, a))
            print('requeing all task from process {task}')
        elif task not in queue:
            return f'{task} not in {status} queue'
        else:
            requeue = [task]
        #for p, a in queue:
        #    if p in process_name:
        #        print(f'requeing (p, a)')
        #        requeue.append((p, a))
        for p, a in requeue:
            queue.pop((p,a))
            self.push_task(p, a)
        return f"{len(requeue)} tasks back in queue"
         
    def push_task(self, process_name, argument):
        if (process_name, argument) in self.done or (
            process_name,
            argument,
        ) in self.failed_tasks:
            return
        task = processing_graph.Task(process_name, argument)
        with self.wid_lock:
            task.tid = self._task_id
            self._task_id += 1
        self.queue.put(task)

    def shutdown(self, server):
        self.server = server
        self._status = "stopping"
        print("Server shutting down")
        # Program all workers to shutdown
        for wid in self.workers:
            self.shut_worker_down(wid)

    def get_pid(self):
        import psutil
        return psutil.Process().pid

