extends Node

class_name QuantumSimulator

const r2 = 0.70710678118

func superpose(v1: Vector2, v2: Vector2) -> PoolVector2Array:
	var x := PoolVector2Array()
	x.append(Vector2(r2*(v1.x + v2.x), r2*(v1.y + v2.y)))
	x.append(Vector2(r2*(v1.x - v2.x), r2*(v1.y - v2.y)))
	return x;
func turn(v1: Vector2, v2: Vector2, theta: float) -> PoolVector2Array:
	theta = float(theta)
	var x := PoolVector2Array()
	x.append(Vector2(v1.x * cos(theta/2) + v2.y * sin(theta/2), v1.y * cos(theta/2) - v2.x * sin(theta/2)))
	x.append(Vector2(v2.x * cos(theta/2) + v1.y * sin(theta/2), v2.y * cos(theta/2) - v1.x * sin(theta/2)))
	return x
func phaseturn(v1: Vector2, v2: Vector2, theta: float) -> PoolVector2Array:
	theta = float(theta)
	var x := PoolVector2Array()
	x.append(Vector2(v1.x * cos(theta/2) - v1.y * sin(-theta/2), v1.y * cos(theta/2) + v1.x * sin(-theta/2)))
	x.append(Vector2(v2.x * cos(theta/2) - v2.y * sin(+theta/2), v2.y * cos(theta/2) + v2.x * sin(+theta/2)))
	return x

# Takes in a decimal value (int) and returns the binary value (int)
# & is bitwise AND, >> is bitwise shift
# binary e.g.: abc & 010 = 0b0, abc >> 2 = a
func dec2bin(decimal_value: int, max_bits: int) -> String:
	var binary_string := "" 
	var temp : int
	var count := max_bits - 1
	while(count >= 0):
			temp = decimal_value >> count 
			if(temp & 1):
					binary_string = binary_string + "1"
			else:
					binary_string = binary_string + "0"
			count -= 1
	return binary_string

func simulate(qc: QuantumCircuit, config={}):
	var shots : int = (1024 if not config.has('shots') else config['shots'])
	var get : String = ('counts' if not config.has('get') else config['get'])
	var noise_model : Array = ([] if not config.has('noise_model') else config['noise_model'])
	var k := PoolVector2Array()
	k.resize(int(pow(2, qc.num_qubits)));
	k[0] = Vector2(1.0, 0.0)

	var outputnum_clbitsap : Dictionary = {}
	for gate in qc.circuit_data:
		if gate[0]=='init': 
			if typeof(gate[1][0]) == TYPE_VECTOR2:
				k = PoolVector2Array()
				k.resize(gate[1].size())
				for i in range(gate[1].size()):
					k[i] = gate[1][i]
			else: 
				k = PoolVector2Array()
				k.resize(gate[1].size())
				for i in range(gate[1].size()):
					k[i] = Vector2(gate[1][i], 0)
		elif gate[0]=='m': 
			outputnum_clbitsap[gate[2]] = gate[1]
		elif ['x', 'h', 'rx', 'rz'].has(gate[0]): 
			var j : int = gate[-1] 
			for i0 in range(pow(2, j)):
				for i1 in range(pow(2, qc.num_qubits-j-1)):
					var b0 : int = i0 + int(pow(2, (j+1))) * i1 
					var b1 : int = b0 + int(pow(2, j))
					if gate[0] == 'x': 
						var temp := k[b0]
						k[b0] = k[b1]
						k[b1] = temp
					elif gate[0] == 'h': 
						var temp_arr := superpose(k[b0], k[b1])
						k[b0] = temp_arr[0]
						k[b1] = temp_arr[1]
					elif gate[0]=='rx': 
						var temp_arr := turn(k[b0], k[b1], float(gate[1]))
						k[b0] = temp_arr[0]
						k[b1] = temp_arr[1]
					elif gate[0]=='rz': 
						var temp_arr := phaseturn(k[b0], k[b1], float(gate[1])) 
						k[b0] = temp_arr[0]
						k[b1] = temp_arr[1]
		elif ['cx', 'crx'].has(gate[0]): 
			var s_gate_var : int
			var t_gate_var : int
			var theta : float
			if gate[0]=='cx': 
				s_gate_var = gate[1]
				t_gate_var = gate[2]
			else:
				theta = float(gate[1])
				s_gate_var = gate[2]
				t_gate_var = gate[3]
			var l_gate_var := int(min(s_gate_var, t_gate_var))
			var h_gate_var := int(max(s_gate_var, t_gate_var))
			for i0 in range(pow(2, l_gate_var)):
				for i1 in range(pow(2, (h_gate_var-l_gate_var-1))):
					for i2 in range(pow(2, (qc.num_qubits-h_gate_var-1))):
						var b0: int = i0 + int(pow(2, (l_gate_var+1))) * i1+ int(pow(2, (h_gate_var+1))) * i2 + int(pow(2, s_gate_var))
						var b1: int = b0 + int(pow(2, t_gate_var))
						if (gate[0] == 'cx') :
							var temp := k[b0] 
							k[b0] = k[b1] 
							k[b1] = temp
						else:
							var temp_arr := turn(k[b0], k[b1], theta) 
							k[b0] = temp_arr[0]
							k[b1] = temp_arr[1]
	if get=='statevector':
		return k
	else:
		var probs := [] # Array of floats
		probs.resize(k.size())
		for i in range(k.size()):
			probs[i] = pow(k[i].x, 2) + pow(k[i].y, 2)
		if noise_model.size() > 0:
			for j in range(qc.num_qubits):
				var p_meas : float = noise_model[j]
				for i0 in range(pow(2, j)):
					for i1 in range(pow(2, (qc.num_qubits-j-1))):
						var b0 : int = i0 + int(pow(2, (j+1))) * i1 
						var b1 : int = b0 + int(pow(2, j)) 
						var p0 : float = probs[b0]
						var p1 : float = probs[b1]
						probs[b0] = (1 - p_meas) * p0 + p_meas * p1
						probs[b1] = (1 - p_meas) * p1 + p_meas * p0
		if get=='probabilities_dict':
			var probs_dict : Dictionary = {};
			for i in range(probs.size()):
				probs_dict[dec2bin(i, qc.num_qubits)] = probs[i]
			return probs_dict
		elif ['counts', 'memory'].has(get):
			var m := []
			m.resize(qc.num_qubits)
			for i in range(qc.num_qubits):
				m[i] = false
			for gate in qc.circuit_data:
				for j in range(qc.num_qubits):
					assert(not(gate[-1] == j and m[j]), 'Incorrect or missing measure command.')
					m[j] = gate.size() >= 3 and gate[0]=='m' and gate[1] == j and gate[2] == j
			m = []
			for _i in range(shots):
				var cumu: float = 0
				var un : bool = true
				var rand_float := randf()
				for j in range(probs.size()):
					var p : float = probs[j]
					cumu += p
					var raw_out : String = ""
					var out_list : Array = [] # Array of strings
					out_list.resize(qc.num_clbits)
					if rand_float < cumu and un:
						raw_out = dec2bin(j, qc.num_qubits)
						out_list.resize(qc.num_clbits)
						for clbitPos in range(qc.num_clbits):
							out_list[clbitPos] = "0"
						for bit in outputnum_clbitsap:
							out_list[qc.num_clbits - 1 - int(bit)] = raw_out.substr(qc.num_qubits - 1 - outputnum_clbitsap[bit],1)
						var out : String = ''
						for val in out_list:
							out += str(val)
						m.append(out)
						un = false
			if get=='memory':
				return m
			else:
				var counts : Dictionary = {}
				for out in m:
					if counts.has(out):
						counts[out] += 1
					else:
						counts[out] = 1
				return counts
