load 'MicroQiskit.rb'

qc = QuantumCircuit.new(3, 3)
qc.x(0)
qc.rx(Math::PI, 1)
qc.x(1)
qc.h(2)
qc.cx(0, 1)
qc.z(1)
qc.rz(Math::PI / 2, 1)
qc.ry(Math::PI / 4, 1)
qc.measure(0, 0)
qc.measure(1, 1)
qc.measure(2, 2)
puts qc.data
puts simulate(qc, 5, "counts")
