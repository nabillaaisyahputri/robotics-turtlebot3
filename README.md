# Robotics TurtleBot3 - Dockerized ROS 2 Development Environment

Repositori ini berisi implementasi lingkungan pengembangan berbasis Docker untuk ROS 2 Humble Hawksbill pada Ubuntu 22.04 LTS (WSL2), ditujukan untuk praktikum robotika TurtleBot3.

---

## Struktur Repositori

```text
robotics-turtlebot3/
├── config/       # Berkas konfigurasi RViz dan simulasi
├── data/         # Dataset, log, dan artefak keluaran (rqt_graph.png)
├── docker/       # Dockerfile, compose.yaml, dan script entrypoint
├── docs/         # Laporan praktikum (modul01_report.md)
├── launch/       # Berkas ROS 2 launch
├── maps/         # Peta navigasi robot
├── src/          # Source code paket ROS 2 (my_first_robot_package)
└── tests/        # Skrip pengujian otomatis
---

## Petunjuk Penggunaan (Quickstart)

Ikuti langkah-langkah berikut untuk mereproduksi dan menjalankan sistem development:

### 1. Prasyarat Host
Pastikan Docker Engine, Docker Compose plugin, dan X-Server (WSLg atau VcXsrv) telah terpasang pada sistem host.

### 2. Konfigurasi Environment & Hak Akses GUI
Jalankan di terminal host sebelum mengaktifkan container:
```bash
# Izinkan akses tampilan GUI X11 ke container
xhost +local:docker

# Masuk ke direktori docker
cd docker

#Bangun image lokal dan jalankan kontainer di latar belakang
# Build image ROS 2 dev
docker compose build

# Jalankan service dev
docker compose up -d

#Eksekusi ROS2
# Masuk ke terminal container
docker compose exec dev bash

# Di dalam container: build paket
cd /ws
colcon build --symlink-install

# Source overlay workspace
source install/setup.bash

# Jalankan node uji coba
ros2 run my_first_robot_package hello_robot

# Mematikan Lingkungan
docker compose down
