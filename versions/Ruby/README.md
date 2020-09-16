# MicroQiskit for Ruby

This version of MicroQiskit is compatible with the Ruby programming language.

### Installation

All you need to do is take the [MicroQiskit.rb](MicroQiskit.rb) file, and place somewhere that it can be found by Ruby when importing. The easiest option is simply to put it in the same folder as any scripts that will use it.

For example, one of your scripts might look like:

```
load 'MicroQiskit.rb'

psiMinus = QuantumCircuit.new(2, 2)
psiMinus.h(0)
psiMinus.x(1)
psiMinus.cx(0, 1)
psiMinus.z(1)
psiMinus.measure(0, 0)
psiMinus.measure(1, 1)
psiMinusStatevector = simulate(psiMinus, 0, 'statevector')
puts 'psiMinusStatevector: '
puts psiMinusStatevector
puts simulate(psiMinus, 5, 'counts')
```

### Documentation

* [Documentation for MicroQiskit](https://microqiskit.readthedocs.io/en/latest/micropython.html)
* [Documentation for Qiskit](https://qiskit.org/documentation/)
