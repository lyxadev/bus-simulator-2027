# Bus Simulator 2027

Bus Simulator 2027 adalah game simulator mengemudi bus kota, dibuat dengan Godot 4.7.2 (GDScript).

## Cara menjalankan

1. Install Godot 4.7.2.
2. Buka Godot, pilih Import, lalu pilih file `project.godot` di folder ini.
3. Tekan F5 untuk menjalankan.

Kontrol: W/S gas dan rem, A/D belok.

## Model bus

Model dibuat oleh Blender lewat `tools/make_bus.py` dan disimpan sebagai `assets/models/bus.glb`. Jalankan manual dengan:

```
blender -b --factory-startup --python tools/make_bus.py
```

## Build

Workflow GitHub Actions di `.github/workflows/build.yml` memasang Blender, membuat model bus, mengekspor versi web Godot, dan menyimpannya sebagai artifact. Workflow ini jalan otomatis setiap ada commit ke `main`.

## Fitur rencana

- Rute bus kota dengan halte dan jadwal
- Sistem penumpang dan pendapatan
- Kontrol kemudi, gas, rem, dan pintu bus
- Mode karier dengan tingkat kesulitan bertahap

## Lisensi

Belum ditentukan.
