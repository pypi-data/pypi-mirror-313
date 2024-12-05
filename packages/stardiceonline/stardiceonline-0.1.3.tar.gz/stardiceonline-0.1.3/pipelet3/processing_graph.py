import inspect
import re


class Link(object):
    descr_re = re.compile("->(\[(?P<filter>\w+)\])?")

    def __init__(self, graph, descr):
        self.graph = graph
        self.child = None
        self.parent = None
        match = self.descr_re.match(descr)
        if match is None:
            raise ValueError(
                f'Unable to process this part of the pipeline string: {descr}. It is expected to match the format "{self.descr_re.pattern}"'
            )
        for s in self.descr_re.groupindex:
            if match[s]:
                try:
                    setattr(self, s, self.graph.namespace[match[s]])
                except KeyError:
                    raise ValueError(
                        f"Function {match[s]} is not available in the provided namespace"
                    )
            else:
                setattr(self, s, Truef)
        self.calculated = set()

    def __str__(self):
        return f'{self.parent.name} -> {self.child.name}'

    def __repr__(self):
        return str(self)
    
    def pass_through(self, task, scheduler):
        for result in task.result:
            if result in self.calculated:
                continue
            if self.filter(result):
                self.calculated.add(result)
                scheduler.push_task(self.child.name, result)
            
    def push_available(self, scheduler):
        pass


def Truef(task):
    return True


class GroupBy(Link):
    descr_re = re.compile("@>\((?P<classdef>\w+)\)(\[(?P<filter>\w+)\])?")

    def __init__(self, graph, descr):
        Link.__init__(self, graph, descr)
        self.calculated = {}
        self.available = set()

    def pass_through(self, task, scheduler):
        for result in task.result:
            if not self.filter(result):
                continue
            hash_class = self.classdef(result)
            if hash_class in self.calculated:
                calculated = self.calculated[hash_class]
                if result in calculated:
                    continue
                calculated.append(result)
            else:
                self.calculated[hash_class] = [result]
            self.available.add(hash_class)

    def push_available(self, scheduler):
        while len(self.available):
            hash_class = self.available.pop()
            scheduler.push_task(
                self.child.name, (hash_class, tuple(self.calculated[hash_class]))
            )


class Join(Link):
    def pass_through(self, task):
        pass


class Process(object):
    def __init__(self, graph, name):
        self.graph = graph
        self.name = name
        self.children = []
        self.parents = []
        try:
            self.func = self.graph.namespace[name]
        except KeyError:
            raise ValueError(
                f"Function {name} is not available in the provided namespace"
            )


link_types = {"-": Link, "=": Join, "@": GroupBy}


class Task(object):
    def __init__(self, process_name, argument):
        self.process_name = process_name
        self.argument = argument
        self.result = None

    def __str__(self):
        return f"{self.process_name}: {self.result}"


class Graph(object):
    def __init__(self, description, namespace, state_file="pipelet_state.pkl"):
        self.state_file = state_file
        self.namespace = namespace
        self.description_to_graph(description)
        self.store_source_code()
        
    def description_to_graph(self, description):
        self.processes = {}
        self.links = {}

        for descr in description.splitlines():
            chunks = descr.split()
            current_process = None
            previous_process = None
            current_link = None
            for _c, c in enumerate(chunks):
                if c[0] in ["-", "=", "@"]:
                    current_link = link_types[c[0]](self, c)
                else:
                    if c not in self.processes:
                        self.processes[c] = Process(self, c)
                    current_process = self.processes[c]
                    if current_link is not None:
                        l = self.links.setdefault(c, [])
                        l.append(current_link)
                        current_link.parent = previous_process
                        current_link.child = current_process
                        if previous_process is not None:
                            previous_process.children.append(current_link)
                        if current_process is not None:
                            current_process.parents.append(current_link)
                    previous_process = current_process

    def store_source_code(self):
        self.source_code = {}
        functions = (
            [process.func for p, process in self.processes.items()]
            + [link.filter for l, link in self.links.items() if hasattr(link, "filter")]
            + [
                link.classdef
                for l, link in self.links.items()
                if hasattr(link, "classdef")
            ]
        )
        for f in functions:
            self.source_code[f.__name__] = inspect.getsource(f)

    def __str__(self):
        return str(self.links)
