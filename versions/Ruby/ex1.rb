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
