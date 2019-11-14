# MicroQiskit for Python

This version of MicroQiskit is compatible with MicroPython, CircuitPython and Python 2.

The [microqiskit.py](microqiskit.py) file found here is the same as that in the top-level folder, but with comments and blank lines removed. This is to reduce the file size, in order to better fit on a microcontroller.

The creation of this file is done automatically by running [initialize_microqiskit.py](initialize_microqiskit.py). This process also performs tests to ensure that MicroQiskit is working correctly.

## Installing MicroQiskit

Dowloading a single file is all that is needed, so the word 'installation' is perhaps overkill. All you need to do is take the [microqiskit.py](microqiskit.py) file, and place somewhere that it can be found by Python when importing. The easiest option is simply to put it in the same folder as any Python scripts that will use it.

## Learn more

* The main differences between Qiskit and MicroQiskit are detailed below.
* Check out [the docs](https://microqiskit.readthedocs.io/en/latest/#).


## Differences with Qiskit

### Running a circuit

When running a quantum program in Qiskit, you start with a `QuantumCircuit` object that you want to run. Let's call it `qc`. The execute function is then used to create a `Job` object.

    job = execute(qc,backend,shots)    # Qiskit
    
Once the job is finished, a `Results` object can be extracted from this

    results = job.result()             # Qiskit
    
Then we can extract the actual results. The most common way to do this is with a dictionary that lists how many of the `shots` samples went to each of the possible outputs. This is known as the 'counts' dictionary.

    counts = results.get_counts()     # Qiskit

This multi-stage process allows for the many possible ways of running circuits and extracting results in Qiskit. But in MicroQiskit, there is only one way to run the circuit: using MicroQiskit's built in simulator. This allows for a simpler syntax.

    counts = simulate(qc,shots,get='counts')        # MicroQiskit
    
It is also possible to extract the memory and statevector with `get='memory'` and `get='statevector'`, respectively.

See [the docs](https://microqiskit.readthedocs.io/en/latest/#) for more details.