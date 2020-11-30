load 'MicroQiskit.rb'

ghz = QuantumCircuit.new(3, 3)
ghz.h(0)
ghz.cx(0, 1)
ghz.cx(0, 2)
ghz.measure(0, 0)
ghz.measure(1, 1)
ghz.measure(2, 2)
ghzStatevector = simulate(ghz, 0, 'statevector')
puts 'ghzStatevector: '
puts ghzStatevector
puts simulate(ghz, 5, 'counts')
