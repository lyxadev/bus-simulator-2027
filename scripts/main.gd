extends Node2D

# Rute sederhana: nama halte dan menit dari titik awal.
const STOPS := [
	{"name": "Terminal", "minutes": 0},
	{"name": "Pasar", "minutes": 10},
	{"name": "Kampus", "minutes": 25},
]

var elapsed_minutes := 0.0
var label: Label


func _ready() -> void:
	label = Label.new()
	label.position = Vector2(24, 24)
	label.add_theme_font_size_override("font_size", 24)
	add_child(label)
	_update_label()


func _process(delta: float) -> void:
	elapsed_minutes += delta
	_update_label()


func next_stop_name(minutes: float) -> String:
	for stop in STOPS:
		if stop["minutes"] >= minutes:
			return stop["name"]
	return "-"


func _update_label() -> void:
	label.text = "Halte berikutnya: %s\nWaktu: %.1f menit" % [next_stop_name(elapsed_minutes), elapsed_minutes]
