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
        self.method_ocurrencies = {}
        
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
                # print('stack tuple', stack_tuple)
                self.trace_tuples.append(stack_tuple)

                # get all method in the stack tuple
                for method in stack_tuple:
                    if method in self.method_ocurrencies:
                        self.method_ocurrencies[method] += 1
                    else:
                        self.method_ocurrencies[method] = 1

    def sample(self):
        while self.active:
            self.checkTrace()
            sleep(1)
            self.sample_count += 1


    def print_report(self):
        # Este metodo debe imprimir el reporte del call context tree

        # Imprimir el tiempo total de ejecución
        print('total ({} seconds)'.format(self.sample_count))

        print('Call context tree:')
        print(self.trace_tuples)
        print()
        print(self.method_ocurrencies)





