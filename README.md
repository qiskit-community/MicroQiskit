# MicroQiskit

[Qiskit](https://qiskit.org) is the well-developed and most feature-rich framework for quantum computing. It allows quantum programs to be created, and then run on either advanced simulator or [real prototype quantum devices](https://quantum-computing.ibm.com). Though its obviously a good thing to have many features and support many use-cases, it can sometimes be too much of a good thing!

For this reason we have created MicroQiskit: the smallest and most feature-poor framework for quantum computing. It has all the basic features and only the basic features. Making it much easier to learn, and much easier to get running.

MicroQiskit was initially conceived as a version of Qiskit that could run on microcontroller devices. The strict need for simplicity and a lack of complex dependencies was the main design constraint.

We are now in the process of porting MicroQiskit to other languages. In this regard it serves as a trial version of Qiskit, allowing new users to try it out before they buy into the Python ecosystem. It is not recommended for long-term use, since there is so much that can only be done using the standard version. For this reason, the ports will all allow you to export your quantum jobs in Python-compatible code.

MicroQiskit is written to be as compatible with Qiskit as possible. Learning quantum programming with MicroQiskit is therefore a way to get started with Qiskit. And [getting to know Qiskit](https://community.qiskit.org/textbook) is a great way to get started with MicroQiskit.

### Documentation

* [Documentation for MicroQiskit](https://microqiskit.readthedocs.io/en/latest/#)
* [Documentation for Qiskit](https://qiskit.org/documentation/)

### Installation

Installation guides for the various versions of MicroQiskit can be found in the corresponding README files.

* [MicroPython/Python 2](versions/MicroPython/README.md)
* [Lua](versions/Lua/LUA.md)
* [C++](versions/C++/README.md)


### Template Version

The [microqiskit.py](microqiskit.py) file found in this folder is intended as a template version. It contains comments to explain how each part of MicroQiskit works, both to aid understanding and to help in the writing of ports. The MicroPython version is directly constructed from this template.

## Differences with Qiskit

### Available gates

Quantum gates are added to circuits in MicroQiskit in the same way as in Qiskit. The main difference is that only the gates `x`, `y`, `z`, `h`, `cx`, `rx`, `ry` and `rz` can be added to a circuit in MicroQiskit. All others can be created if and when required from this basic set.

During simulation, or when exporting the circuit in a Python-compatible form, it is compiled into the set consisting only of `x`, `h`, `cx` and `rx`.

### Running Circuits

In Qiskit, the way circuits are run must account for the many different possible backends, including various simulators as well as prototype quantum devices. In MicroQiskit, there is only one simulator. As such, the process is reduced to either a single `simulate` function or a single `Simulator` class, depending on language. These functions and classes are not present in Qiskit.
