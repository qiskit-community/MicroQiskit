# MicroQiskit for Python

This version of MicroQiskit is compatible with MicroPython, CircuitPython and Python 2.

The [microqiskit.py](microqiskit.py) file found here is the same as that in the top-level folder, but with comments and blank lines removed. This is to reduce the file size, in order to better fit on a microcontroller.

The creation of this file is done automatically by running [initialize_microqiskit.py](initialize_microqiskit.py). This process also performs tests to ensure that MicroQiskit is working correctly.

### Installation

Dowloading a single file is all that is needed, so the word 'installation' is perhaps overkill. All you need to do is take the [microqiskit.py](microqiskit.py) file, and place somewhere that it can be found by Python when importing. The easiest option is simply to put it in the same folder as any Python scripts that will use it.

### Documentation

* [Documentation for MicroQiskit](https://microqiskit.readthedocs.io/en/latest/micropython.html)
* [Documentation for Qiskit](https://qiskit.org/documentation/)
