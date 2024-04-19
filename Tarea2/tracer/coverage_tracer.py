import sys
import ast
import inspect
from types import *
import traceback
from stack_inspector import StackInspector

""" Clase para la Tarea 2. Para su uso, considere:
with CoverageTracer() as covTracer:
    function_to_be_traced()

covTracer.report_executed_lines()
"""

class CoverageTracer(StackInspector):

    def __init__(self):
        super().__init__(None, self.traceit)
        self.lines_executed = {}

    # Completa la funcion de rastreo
    def traceit(self, frame, event: str, arg):
        if event == 'line':
            filename = frame.f_globals.get('__file__', None)
            if filename:
                filename = filename.split('/')[-1]  # Obtener solo el nombre del archivo
            lineno = frame.f_lineno
            func_name = frame.f_code.co_name
            if func_name in ['<module>', '__exit__', '__enter__']:  # Filtrar funciones especiales
                return
            key = (filename, func_name, lineno)
            self.lines_executed[key] = self.lines_executed.get(key, 0) + 1  # Incrementar la frecuencia de la línea ejecutada
        return self.traceit  # Devolver la función de trazado para seguir trazando

    def print_lines_report(self):
        print("{:<30} {:<10} {:<10}".format('fun', 'line', 'freq'))
        for (filename, func_name, lineno), freq in sorted(self.lines_executed.items()):
            print("{:<30} {:<10} {:<10}".format(func_name, lineno, freq))

    def report_executed_lines(self):
        self.print_lines_report()
        # Completa el codigo necesario
