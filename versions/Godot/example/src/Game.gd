extends Node2D

class_name Game

onready var drop_timer : Timer = $DropTimer
onready var q : QuantumNode = $QuantumNode

var b : Ball
var probs := 0.0

const commands = {
  0: 'x',
  1: 'h',
  2: 'z',
  3: 'y',
  4: 'rx',
  5: 'ry',
  6: 'rz',
  7: 'reset'
}

func _ready() -> void:
	q.qc.set_circuit(1,1)
	drop_timer.connect("timeout", self, "drop_ball")
	_update_ui()
	pass


func drop_ball()-> void:
	b = load("res://src/Ball.tscn").instance()
	b.set_state(randf() >= probs)
	add_child(b)
	pass


func _on_PopupMenu_index_pressed(index: int) -> void:
	var command = commands[index]
	if command == "reset":
		get_tree().change_scene(get_tree().current_scene.filename)
	elif 'r' in command:
		q.qc.call(command, PI/4, 0)
	else:
		q.qc.call(command, 0)
	probs = q.simulate_and_get_probabilities_dict()["1"]
	_update_ui()


func _update_ui():
	var data = q.qc.circuit_data
	var output = ""
	for arr in data:
		output += str(arr[0])
		if arr.size() == 3:
			var angle : float = round(arr[1] * 100 / PI) / 100.0
			output += " (" + str(angle) + " pi)"
		output += '\n'
	var prob_text = 'Probability of passing through: ' + str(probs) + '\n---'  
	$QuantumDisplay/Probability.text = prob_text
	$QuantumDisplay/Gates.text = output


func _on_AddGatesBtn_pressed() -> void:
	$PopupMenu.popup()
