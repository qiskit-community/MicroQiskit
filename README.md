# Aether - Quantum for Microcontrollers

Microcontrollers are a popular platform for hobbyist and educational programming. Quantum computation is an emerging technology that also promises to be great for these purposes. So let's combine them!

The best way to do quantum computing is with [Qiskit](https://github.com/qiskit/). This is an open-source Python framework with which quantum programs can be written, tested and run on [IBM's prototype quantum devices](https://www.research.ibm.com/ibm-q/). The many features of Qiskit, however, make it rather hard to fit quantumness on a microcontroller. 

There are many ways to try solving this problem. For example, if you can use the internet with your microcontroller, you could delegate all the tricky bits to the cloud.

Aether is an alternative option. It is the heart of Qiskit, reborn in less than 100 lines of code. With Aether, you can create and simulate simple quantum circuits to add a quantum flavour to your microcontroller project.

Aether is written to be as compatible with Qiskit as possible. Learning quantum programming with Aether is therefore a way to get started with Qiskit. And [getting to know Qiskit](https://github.com/Qiskit/qiskit-tutorials) is a great way to get started with Aether.

Even so, there are a few differences. These are detailed below.

### Setting up a quantum circuit

The quantum circuit is the basic element of quantum programming. In Qiskit, a simple way to define a circuit is

    qc = QuantumCircuit(n,m)           # Qiskit
    
This creates a circuit with `n` qubits, from which `m` bits of output will be extracted. In most cases, we simply choose `m` to be equal to `n`. For the sake of simplicity, this choice is hardwired in to Aether. So to set up a quantum circuit, simply use

    qc = QuantumCircuit(n)             # Aether

Another restriction for Aether is that only one and two qubit circuits can be run, so `n` must be 1 or 2.

### Extracting outputs

In quantum circuits, output bits can be extracted from qubits at any desired point. Multiple output bits can be extracted from each qubit, or none can.

The most common choice is to extract a single output bit from each qubit, and to do so only at the very end of the circuit. In Qiskit, this would be done using the following command at the end of the circuit.

    for j in range(n):
        qc.measure(n,n)               # Qiskit

This is the case that is hardwired into Aether. As such, so `measure` command is required.


### Running a circuit

In Qiskit, a circuit `qc` is run on a given backend by first creating a job object

    job = execute(qc,backend,shots)    # Qiskit
    
Once the job is finished, a results object can be extracted from this

    results = job.result()             # Qiskit
    
From the results object we can then extract the actual results. The most common way to do this is with a dictionary that lists how many of the `shots` samples went to each of the possible outputs. This is known as the 'counts' dictionary.

    counts = results.get_counts()     # Qiskit

This multi-stage process allows for the many possible ways of running circuits and extracting results in Qiskit. But in Aether, there is only one simulator and the counts are the only type of results you can get. So the process is reduced to a single step.

    counts = execute(qc,shots)        # Aether
    
### Additional features

The simulation in Aether is done on the fly by the quantum circuit object. This makes it possible to inspect the state so far at any time using the `expectations` attribute. This is a dictionary of all Pauli expectation values.
    
### Available gates

Quantum gates are added to circuits in Aether in the same way as in Qiskit. The main difference is that the set of available gates in Aether is limited to `x`, `z`, `cx`, `cz`, `rx`, `rz` and `h`. It is also not advisable to use `rx` and `rz` with a `theta` outside the range from -pi/2 to pi/2. Instead use these gates multiple times with angles inside this range, or combine with other gates.

## Aether in action!

* [simple test](simple_test.py) - A simple script using Aether to randomly generate a series of images for the [micro:bit](https://microbit.org/).

If you have projects that use Aether, add them to this list!
