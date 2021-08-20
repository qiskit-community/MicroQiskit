# Developer Guide

This README is not intended to explain the Godot game engine or the GDScript, please refer to Godot resources, they have an excellent community and documentation to get you started.
Instead, this set of Godot scenes and scripts can be used by any beginner in Godot to add quantum computation to their game.
To this, end we have 

## Sample Project

There is also a sample godot project in the [example folder](https://github.com/quantum-defence/MicroQiskit#./example).
Try it out [here](https://bhcs.itch.io/sample-quantum-godot-game) on your browser. 

:warning: the overhead of running godot game engine (not the lightweight microqiskit code), will result in significant loading time on the webpage as opposed to exporting it as a native app or running it in your Godot engine.

This sample project aims to only show a very simple use of MicroQiskit​ ported to Godot. 
It is a minimal quantum simulator that sets up a circuit of 1 qubit with gates according to your specification, and visually shows the result of measuring the output qubit (ball bouncing off the barrier).

For example, if you add an RY gate (at an angle of PI/4), this would be equivalent to adding RX at PI/2, RZ at PI/4, RX at -PI/2.
This simplified gate set is displayed and the quantum circuit output is measured.
As displayed, the output is a qubit that has a ~15% chance of resolving to 1 on measurement.
Accodingly, the ball now goes through the barrier ~15% of the time.


## Getting Started

There are three scenes to this codebase, _*QuantumNode*_ _*QuantumCircuit*_  and _*Simulator*_ which loosely the structure of the MicroQiskit python library.
In addition to this there is a _*QiskitTester*_ scene that serves as an automatic test script to validate the _*Simulator*_ and _*QuantumCircuit*_ code.

To begin, take the [microqiskit.zip](./microqiskit.zip), unzip it and place it in the root of your Godot game project. Click on each script and scene from inside Godot editor to ensure your `project.godot` has been updated. For more detailed information, refer [here](./dev-guide.md).
(You may move it subsequently using Godot's built in move method from the file explorer in the editor to avoid dependency errors.)
Use the _*QuantumNode*_ in your intended scene, and interact it with it programmatically using your scene. For example:

```python
var onready q: QuantumNode = $QuantumNode

func _ready() -> void:
	q.qc.set_circuit(1, 1) # Initialises with an empty circuit with 1 qubit and 1 classical bit
```

Subsequently, you can call functions on `q.qc` to add gates. The usage is very similar to the python code:

```
q.qc.h(0) # add a Hadamard gate to the 0 index qubit
q.qc.x(0) # add a not gate to the 0 index qubit
q.qc.cx(1, 0) # add a CX gate to the 1 index qubit using 0 qubit
q.qc.rx(PI/4, 0) # add an RX gate with PI/4 as the angle to the 0 index qubit
```

This sets up a sequence of gates in the order called.
After this, running any of the `simulate_and_get_...` functions will serve you the required computation for use in your other logic.
This is a complete scene, and using all signals, connect and other functionality are entirely possible and up to the developer's imagination.

### _*QuantumNode*_ 

This is the main node that surfaces the results of quantum computation to users.
It has two members (`qc:` _`QuantumCircuit`_ and `sim:` _`Simulator`_) that are explained further down.

Most importantly, it has the following functions that would be the most useful for a developer:

```python
simulate_and_get_memory(config = {}) -> Array
simulate_and_get_counts(config = {}) -> Dictionary
simulate_and_get_probabilities_dict(config = {}) -> Dictionary
simulate_and_get_statevector(config = {}) -> PoolVector2Array
```

A developer with more specific requirements would be advised to extend the _*QuantumNode*_ or create a new similar scene that holds the number of _*QuantumCircuit*_ and _*Simulator*_ you wish and surfaces the appropriate methods.
One example used in the [Quantum Defence game](https://github.com/quantum-defence/quantum-defence/)(note: under development) is a subclass of _*QuantumNode*_ that initialises a circuit of 1 qubit on creation and surfaces more appropriate methods for use.

### _*QuantumCircuit*_ 

This class serves to contain the data of the quantum circuit as well as the methods to set and use it (including the code to add gates or quantum circuits to an existing circuit).

Calling the instance with a gate name (`.h`, `.x`, `.cx`, etc) will add the gate to the object. All gates require at least one variable (the index of the qubit the gate is used on), but specific gates that require angle or an additional qubit will need those arguments as well.

### _*Simulator*_ 

This script is MicroQiskit's Python `simulate()` function remade in GDScript, and takes in a _*QuantumCircuit*_ and a config, returning simulated values;
Note that there have been many changes made for GDScripts different requirements.
This is kept seperate from _*QuantumCircuit*_ to have this rather heavy bit of code handled separately from the encapsulation of circuit data.
In this manner future optimisation relating to game performance could potentially be easier done, and the simulator nodes could be made to run multi-threaded processes while the _*QuantumCircuit*_ instances only serve as a store of gates and their parameters.

### _*QiskitTester*_ 

This script is MicroQiskit's Python `initialize_microqiskit.py` file remade in GDScript, and tests the _*QuantumCircuit*_ and _*QuantumSimulator*_ to the same battery of tests.
Note that there have been many changes made for GDScripts different requirements.
If you wish to contribute, please make sure _*QiskitTester*_ continues to pass, with additional tests if necessary.