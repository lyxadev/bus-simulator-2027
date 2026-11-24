extends CharacterBody3D

const MAX_SPEED := 20.0
const ACCELERATION := 8.0
const BRAKE_FORCE := 14.0
const STEER_SPEED := 1.5

var speed := 0.0

func _physics_process(delta: float) -> void:
	var throttle := Input.get_axis("brake", "accelerate")
	speed = clamp(speed + throttle * ACCELERATION * delta, -MAX_SPEED * 0.3, MAX_SPEED)
	if throttle == 0.0:
		speed = move_toward(speed, 0.0, 3.0 * delta)
	var steer := Input.get_axis("steer_left", "steer_right")
	rotate_y(-steer * STEER_SPEED * delta * clamp(speed / MAX_SPEED, 0.0, 1.0))
	velocity = -transform.basis.z * speed
	move_and_slide()
