extends Node

class_name QuantumNode

onready var qc: QuantumCircuit = $QuantumCircuit
onready var sim: QuantumSimulator = $Simulator


# returns array of strings 
func simulate_and_get_memory(config = {}) -> Array:
	config['get'] = 'memory'
	return sim.simulate(qc, config)


# returns dictionary: binary_repr: string => : int
func simulate_and_get_counts(config = {}) -> Dictionary:
	config['get'] = 'counts'
	return sim.simulate(qc, config)


# returns dictionary: binary_repr: string => : float
func simulate_and_get_probabilities_dict(config = {}) -> Dictionary:
	config['get'] = 'probabilities_dict'
	return sim.simulate(qc, config)


func simulate_and_get_statevector(config = {}) -> PoolVector2Array:
	config['get'] = 'statevector'
	return sim.simulate(qc, config)
