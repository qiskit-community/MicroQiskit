MicroQiskit Library Reference
*****************************

A version of `Qiskit <https://qiskit.org`_ made for microcontrollers and for educational purposes.

.. module:: microqiskit


.. function:: simulate(level)

    Set the brightness of the display, from 0 (minimum) to 15 (maximum). On
    devices that don't support varying the brightness this does nothing.
    
    This is the MicroQiskit equivalent of the ``execute`` function in Qiskit.

.. class:: QuantumCircuit(num_qubits, num_bits=0)

    Contains a quantum circuit, which is essentially a list of quantum gates
    that are applied to a register of qubits. At the end, a binary output is
    recorded on a register of bits.
    
    This is the MicroQiskit version of the identically named class in Qiskit.

    .. classmethod:: initialize(ket)
    
        Initializes a circuit with the state described by the statevector ``ket``.
    
    .. classmethod:: x(qubit)
    
        Adds an ``x`` gate to the circuit on the given qubit.
    
    .. classmethod:: rx(theta,qubit)
    
        Adds rotation around the x axis to the circuit on the given qubit. The
        angle is given by ``theta``.
    
    .. classmethod:: ry(theta,qubit)
    
        Adds rotation around the y axis to the circuit on the given qubit. The
        angle is given by ``theta``.
    
    .. classmethod:: rz(theta,qubit)
    
        Adds rotation around the z axis to the circuit on the given qubit. The
        angle is given by ``theta``.
    
    .. classmethod:: h(qubit)
    
        Adds an ``h`` gate to the circuit on the given qubit.
    
    .. classmethod:: cx(control,target)
    
        Adds a ``cx`` gate to the circuit for the given control and target qubits.
    
    .. classmethod:: measure(qubit,bit)
    
        Adds a measure gate, which extracts a bit of output from the given qubit.
        The ability to independently set ``qubit`` and ``bit`` is to maintain
        consistency with Qiskit. However, an exception will arise if ``qubit!=bit``.
        Exceptions will also arise if any gates are performed on a qubit after it
        has been measured.
