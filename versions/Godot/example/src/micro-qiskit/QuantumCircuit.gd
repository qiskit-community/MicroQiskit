extends Node

class_name QuantumCircuit

var num_qubits: int = 0
var num_clbits: int = 0
var circuit_name: String
var circuit_data: Array


func _ready():
	self.num_qubits = 0
	self.num_clbits = 0
	self.circuit_name = ""
	self.circuit_data = []


func set_circuit(number_of_qubits: int, number_of_clbits: int):
	self.num_qubits = number_of_qubits
	self.num_clbits = number_of_clbits
	self.circuit_data = []


func name_circuit(new_name: String):
	self.circuit_name = new_name


func add(otherQuantumCircuit: QuantumCircuit) -> QuantumCircuit:
	var new_quantum_circuit: QuantumCircuit = get_script().new()
	var max_qubits = max(self.num_qubits, otherQuantumCircuit.num_qubits)
	var max_clbits = max(self.num_clbits, otherQuantumCircuit.num_clbits)
	new_quantum_circuit.set_circuit(max_qubits, max_clbits)
	new_quantum_circuit.circuit_data = self.circuit_data
	new_quantum_circuit.circuit_data.append_array(otherQuantumCircuit.circuit_data)
	new_quantum_circuit.circuit_name = self.circuit_name
	return new_quantum_circuit


# Not sure what this function is for
# same tbh, not in the test also leh...
func initialize(k: Array) -> QuantumCircuit:
	var arr: Array = []
	arr.resize(k.size())
	for i in range(k.size()):
		arr[i] = k[i + 1]
	arr.append(['init', arr])
	self.circuit_data = arr
	return self


func x(q: int) -> QuantumCircuit:
	var temp = ['x', q]
	self.circuit_data.append(temp)
	return self


func rx(theta: float, q: int) -> QuantumCircuit:
	var temp = ['rx', theta, q]
	self.circuit_data.append(temp)
	return self


func rz(theta: float, q: int) -> QuantumCircuit:
	var temp = ['rz', theta, q]
	self.circuit_data.append(temp)
	return self


func h(q: int) -> QuantumCircuit:
	var temp = ['h', q]
	self.circuit_data.append(temp)
	return self


func cx(s: int, t: int) -> QuantumCircuit:
	var temp = ['cx', s, t]
	self.circuit_data.append(temp)
	return self


func crx(theta: float, s: int, t: int) -> QuantumCircuit:
	var temp = ['cx', theta, s, t]
	self.circuit_data.append(temp)
	return self


func measure(q: int, b: int) -> QuantumCircuit:
	if b < self.num_clbits:
		print("Index for bits out of range")
	elif q < self.num_qubits:
		print("Index for qubit out of range.")
	var temp = ['m', q, b]
	self.circuit_data.append(temp)
	return self


func ry(theta, q) -> QuantumCircuit:
	return self.rx(PI / 2, q).rz(theta, q).rx(-PI / 2, q)


func print_data():
	print(self.circuit_data)


func z(q) -> QuantumCircuit:
	return self.rz(PI, q)


func y(q) -> QuantumCircuit:
	return self.rz(PI, q).x(q)
