from __future__ import print_function
import threading
from time import sleep
import time
import traceback
from sys import _current_frames


class Sampler:
    def __init__(self, tid) -> None:
        self.tid = tid
        self.t = threading.Thread(target=self.sample, args=())
        self.active = True
        self.trace_tuples = []
        self.sample_count = 0
        self.method_details = []
        self.current_methods = {}
        
    def start(self):
        self.active = True
        self.t.start()

    def stop(self):
        self.active = False
        self.t.join()
        
    def checkTrace(self):
        for thread_id, frames in _current_frames().items():
            if thread_id == self.tid:
                frames = traceback.walk_stack(frames)
                stack = []
                for frame, _ in frames: 
                    code = frame.f_code.co_name
                    stack.append(code)
                stack.reverse()
                # print(stack)  # Esta linea imprime el stack despues de invertirlo la pueden comentar o descomentar si quieren
                stack_tuple = tuple(stack)
                self.trace_tuples.append(stack_tuple)

    def sample(self):
        while self.active:
            self.checkTrace()
            sleep(1)
            self.sample_count += 1


    def print_report(self):
        print('total ({} seconds)'.format(self.sample_count))

        # Usamos lista con diccionaros para almacenar distintas instancias de un mismo método
        method_instances = {}

        previous_trace = []
        method_order = {}  # Para rastrear el orden de aparición por primera vez
        order_counter = 0

        for trace in self.trace_tuples:

            # Manejar las instancias de los métodos
            for depth, method in enumerate(trace, 1):
                if method not in method_instances:
                    method_instances[method] = []
                
                # Checkear si el método continua o está empezando una nueva instancia
                if not method_instances[method] or method not in previous_trace:
                    # Nueva instancia del método
                    if method not in method_order:
                        method_order[method] = order_counter
                        order_counter += 1
                    method_instances[method].append({'count': 1, 'depth': depth})
                else:
                    # Continua la última instancia del método
                    last_instance = method_instances[method][-1]
                    last_instance['count'] += 1
                    last_instance['depth'] = min(last_instance['depth'], depth)
            previous_trace = trace

        # Creamos lista para guardar todos los detalles del método, incluyendo profundidad y conteo
        methods_to_print = []
        for method, instances in method_instances.items():
            for instance in instances:
                methods_to_print.append((instance['depth'], method, instance['count'], method_order[method]))

        # Ordenamos primero por profundidad y luego por orden de aparición
        methods_to_print.sort(key=lambda x: (x[0], x[3]))

        # Imprimimos los métodos con sus detalles
        for depth, method, count, _ in methods_to_print:
            indent = '  ' * (depth)
            print(f'{indent}{method} ({count} seconds)')









