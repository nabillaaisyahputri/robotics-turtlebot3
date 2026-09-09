# Modul 2: ROS 2 Nodes, Topics, Services, Actions, Parameters, and QoS

Repositori ini berisi implementasi praktikum **Modul 2 Praktikum Robotika**, yang berfokus pada eksplorasi mekanisme komunikasi tingkat lanjut di dalam kerangka kerja **ROS 2 Humble Hawksbill**, pembuatan *custom package*, pengelolaan parameter secara dinamis, serta analisis kebijakan *Quality of Service (QoS)*.

---

## 👨‍💻 Identitas Praktikan
* **Nama:** Nabilla Aisyah Putri
* **NIM:** 25/555621/PA/23295
* **Kelas:** ELA
* **Program Studi:** Elektronika dan Instrumentasi (Elins), Universitas Gadjah Mada

---

## 📂 Struktur Direktori Package (`lab_comm`)
Struktur berkas kode sumber di dalam *workspace* ROS 2 (`/ws/src/lab_comm`):
```text
lab_comm/
├── CMakeLists.txt
├── package.xml
├── lab_comm/
│   ├── __init__.py
│   ├── sensor_publisher.py
│   ├── processing_node.py
│   ├── reset_service.py
│   └── motion_action_server.py
├── launch/
│   └── lab_comm.launch.py
└── README.md

# =====================================================================
# PRASYARAT & LINGKUNGAN SISTEM
# =====================================================================
# Sistem Operasi Host: Ubuntu 22.04 LTS (via WSL2 / Native)
# Container Environment: Docker Engine (ros:humble-ros-base-jammy)
# Framework: ROS 2 Humble Hawksbill


# =====================================================================
# PANDUAN INSTALASI DAN BUILD WORKSPACE
# =====================================================================

# 1. Masuk ke direktori workspace di dalam container
cd /ws

# 2. Build workspace (pastikan package lab_comm sudah ada di dalam src/)
colcon build --symlink-install

# 3. Sourcing environment
source install/setup.bash


# =====================================================================
# CARA MENJALANKAN SISTEM (EXECUTION GUIDE)
# =====================================================================

# 1. Menjalankan Node secara Terintegrasi via Launch File
ros2 launch lab_comm lab_comm.launch.py

# 2. Pengujian Topik dan Analisis QoS
ros2 topic list
ros2 topic info /sensor_data --verbose

# 3. Pengujian Service
ros2 service call /reset_service std_srvs/srv/Trigger

# 4. Pengujian Action (Contoh: Fibonacci order 5)
ros2 action send_goal /compute_sequence example_interfaces/action/Fibonacci "{order: 5}" --feedback

# 5. Pengubahan Parameter secara Dinamis (Runtime)
ros2 param list
ros2 param set /processing_node threshold 0.7


# =====================================================================
# RINGKASAN HASIL EKSPERIMEN SINGKAT
# =====================================================================
# - Kompatibilitas QoS: Komunikasi gagal total (Loss 100%) apabila publisher 
#   menggunakan BEST_EFFORT sementara subscriber menuntut jaminan RELIABLE.
# - Action vs Service: Action lebih unggul untuk proses komputasi panjang 
#   karena mendukung feedback progresif dan pembatalan (cancellation), 
#   berbeda dengan service yang bersifat blocking instan.
