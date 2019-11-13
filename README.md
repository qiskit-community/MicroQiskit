# MicroQiskit - Quantum for Microcontrollers

Microcontrollers are a popular platform for hobbyist and educational programming. Quantum computation is an emerging technology that also promises to be great for these purposes. So let's combine them!

The best way to do quantum computing is with [Qiskit](https://github.com/qiskit/). This is an open-source Python framework with which quantum programs can be written, tested and run on [IBM's prototype quantum devices](https://www.research.ibm.com/ibm-q/). The many features of Qiskit, however, make it rather hard to fit quantumness on a microcontroller. 

There are many ways to try solving this problem. For example, if you can use the internet with your microcontroller, you could delegate all the tricky bits to the cloud.

In this repository, there is an alternative option: MicroQiskit. This is the heart of Qiskit, reborn in around 100 lines of code. With MicroQiskit, you can create and simulate simple quantum circuits to add a quantum flavour to your microcontroller project.

MicroQiskit is written to be as compatible with Qiskit as possible. Learning quantum programming with MicroQiskit is therefore a way to get started with Qiskit. And [getting to know Qiskit](https://community.qiskit.org/textbook) is a great way to get started with MicroQiskit.

## Installing MicroQiskit

Dowloading a single file is all that is needed, so the word 'installation' is perhaps overkill. All you need to do is take the [microqiskit.py](other_versions/microqiskit.py) file, and place somewhere that it can be found by Python when importing. The easiest option is simply to put it in the same folder as any Python scripts that will use it.


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
    
### Available gates

Quantum gates are added to circuits in MicroQiskit in the same way as in Qiskit. The main difference is that the set of available gates in MicroQiskit is limited to `x`, `y`, `z`, `h`, `cx`, `rx`, `ry` and `rz`. All others can be created if and when required from this basic set.
