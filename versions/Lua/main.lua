-- This code is part of Qiskit.
--
-- Copyright IBM 2020

print("\n===================================================================================")
print("This is MicroQiskitLua: an extremely minimal version of Qiskit, implemented in Lua.")
print("\nFor the standard version of Qiskit, see qiskit.org. To run your quantum programs\non real quantum hardware, see quantum-computing.ibm.com.")
print("===================================================================================\n")

dofile("MicroQiskit.lua")

print("\nWe start with a Bell pair: the standard 'Hello World' of quantum computing.\nSee the source code for the circuit.")


--initialize a circuit with two qubits
local qc = QuantumCircuit()
qc.set_registers(2)

--add the gates to create a Bell pair
qc.h(0)
qc.cx(0,1)

--initialize another circuit with two qubits and two output bits
local meas = QuantumCircuit()
meas.set_registers(2,2)
--add the measurements
meas.measure(0,0)
meas.measure(1,1)

--add the measurement circuit to the end of the original circuit
qc.add_circuit(meas)

--simulate the circuit and get a counts result
result = simulate(qc,"counts")

--print this to screen
print("\nThe counts are\n")
for string, counts in pairs(result) do
  print("Counts for",string,"=",counts)
end

--and again, but with less shots
result = simulate(qc,"counts",10)
print("\nHere's the same, but with 10 shots\n")
for string, counts in pairs(result) do
  print("Counts for",string,"=",counts)
end

print("\nNow let's try single qubit rotations and a statevector output.\nSee the source code for the circuit.")

--initialize a circuit with two qubits
local qc2 = QuantumCircuit()
qc2.set_registers(2)
--add some single qubit gates
local pi = 3.14159
qc2.rx(pi/4,0)
qc2.ry(pi/2,1)
qc2.rz(pi/8,0)

--no measurements needed for a statevector output

--simulate the circuit and get a result
print("\nThe statevector is\n")
result2 = simulate(qc2,"statevector")
for index, amp in pairs(result2) do
  print("(",amp[1],")+i(",amp[2],")")
end

print("\nNext, a single qubit, biased towards 0")

local qc3 = QuantumCircuit()
qc3.set_registers(1,1)
qc3.rx(pi/4,0)
qc3.measure(0,0)

print("\nThe counts are\n")
result3 = simulate(qc3,"counts")
for string, counts in pairs(result3) do
  print("Counts for",string,"=",counts)
end

print("\nWe can also get the expectation value of the counts\n")
result3b = simulate(qc3,"expected_counts")
for string, counts in pairs(result3b) do
  print("Counts for",string,"=",counts)
end

print("\nFinally, we'll look at how to only measure a subset of the qubits, and measure them in a different order.\n")

-- 5 qubits and 4 bits of output
-- we put 1s on qubits 1, 3 and 4
local qc4 = QuantumCircuit()
qc4.set_registers(5,4)
qc4.x(1)
qc4.x(3)
qc4.x(4)

-- qubits 1, 3 and 4 (the 1s) are read out to bits 0, 1 and 2
-- qubit 0 is read out to bit 3
qc4.measure(1,0)
qc4.measure(3,1)
qc4.measure(4,2)
qc4.measure(0,3)

print("Here's the bit string that comes out.\n")

result4 = simulate(qc4,"counts",1)
for string, counts in pairs(result4) do
  print(string)
end