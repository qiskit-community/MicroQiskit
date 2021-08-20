extends KinematicBody2D

class_name Ball

var speed = Vector2(10, 0)
const GRAVITY = Vector2(0.0, 9.8)
const SPEED_SCALE = 20

func _ready() -> void:
	self.position = Vector2(60, 100) # location of generator
	
func set_state(will_collide: bool):
	self.set_collision_layer_bit(0, will_collide)
	self.set_collision_mask_bit(0, will_collide)

func _process(delta: float) -> void:
	speed += GRAVITY * delta
	var collision := move_and_collide(speed * delta * SPEED_SCALE, false)
	if (collision):
		speed += Vector2(0, -20)
