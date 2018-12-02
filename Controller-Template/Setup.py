from distutils.core import setup
from Cython.Build import cythonize

files = [
    "Commands.py",
    "Context.py",
    "Controller.py"
    "Main.pyx",
    "Model.py",
    "{subsystem}Controller.py",
    "States.py",
    "Threads.py"
]

setup(name = "{subsystem}", ext_modules=cythonize(files))