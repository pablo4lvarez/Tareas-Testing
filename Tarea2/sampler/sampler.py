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

                # Actualizar el contador de llamadas en el diccionario usando la tupla de la pila como clave
                stack_tuple = tuple(stack)
                self.trace_tuples.append(stack_tuple)

                # # get all method in the stack tuple
                # for method in stack_tuple:
                #     if method in self.method_ocurrencies:
                #         self.method_ocurrencies[method] += 1
                #     else:
                #         self.method_ocurrencies[method] = 1

    def sample(self):
        while self.active:
            self.checkTrace()
            sleep(1)
            self.sample_count += 1









    def print_report(self):
        print('total ({} seconds)'.format(self.sample_count))

        # Use a list of dictionaries to handle multiple instances of the same method
        method_instances = {}

        # Traverse through each stack trace and calculate method occurrences
        previous_trace = []
        for trace in self.trace_tuples:
            current_methods = set(trace)  # Methods in the current trace for easy lookup

            # Handle method instances
            for depth, method in enumerate(trace, 1):
                if method not in method_instances:
                    method_instances[method] = []
                
                # Check if method is continuing or starting anew
                if method not in previous_trace:
                    # New instance of the method
                    method_instances[method].append({'count': 1, 'depth': depth})
                else:
                    # Continue the last instance
                    last_instance = method_instances[method][-1]
                    last_instance['count'] += 1
                    last_instance['depth'] = min(last_instance['depth'], depth)
            
            # Mark end of current methods which did not appear in this trace
            for method in method_instances:
                if method not in current_methods and method_instances[method]:
                    # If the method is active, and did not appear in the current trace
                    last_instance = method_instances[method][-1]
                    if 'end' not in last_instance:
                        last_instance['end'] = True  # Mark the last instance as ended

            # Prepare for the next iteration
            previous_trace = trace

        # Print each method with all its instances
        for method, instances in method_instances.items():
            for instance in instances:
                indent = '  ' * (instance['depth'] - 1)
                duration = instance['count']
                print(f'{indent}{method} ({duration} seconds)')

        # Create a list to store all method details including their calculated depths and counts
        # methods_to_print = []
        # for method, instances in method_instances.items():
        #     for instance in instances:
        #         methods_to_print.append((instance['depth'], method, instance['count']))

        # # Sort by depth first, then by order of appearance
        # methods_to_print.sort(key=lambda x: (x[0], self.trace_tuples.index(tuple([x[1]] if x[1] in trace else trace for trace in self.trace_tuples if x[1] in trace)[0])))

        # # Print each method with all its instances
        # for depth, method, count in methods_to_print:
        #     indent = '  ' * (depth - 1)
        #     print(f'{indent}{method} ({count} seconds)')










