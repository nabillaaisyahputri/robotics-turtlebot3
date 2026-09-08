# Laporan Praktikum Modul 1: Dockerized ROS 2 Development Environment

* **Repositori GitHub:** https://github.com/nabillaaisyahputri/robotics-turtlebot3
* **Sistem Operasi Host:** Ubuntu 22.04 LTS (WSL2)
* **Distribusi ROS:** ROS 2 Humble Hawksbill

---

## 1. Pengambilan Data dan Metrik Lingkungan Pengembangan

### Tabel 1.1 Metrik Lingkungan Pengembangan
| No | Parameter | Satuan | Hasil |
|---|---|---|---|
| 1 | Waktu docker pull image dasar | s | 9.013 |
| 2 | Waktu build image pertama (tanpa cache) | s | 740.65 |
| 3 | Waktu build image kedua (dengan cache) | s | 3.305 |
| 4 | Ukuran image `robotics-lab:dev` | MB / GB | 1.89 GB |
| 5 | Waktu startup container (`docker compose up`) | s | 2.10 |
| 6 | Waktu `colcon build` pertama | s | 1.848 |
| 7 | Jumlah package terbangun | buah | 1 |
| 8 | Commit hash | — | 0725557 |

### Tabel 1.2 Perbandingan Bind Mount vs Named Volume
| Aspek | Bind mount (`../src:/ws/src`) | Named volume (`ws_install`) |
|---|---|---|
| Terlihat di host | Ya | Tidak |
| Bertahan setelah `docker compose down` | Ya | Ya |
| Cocok untuk kode sumber | Ya | Tidak |
| Cocok untuk artefak build | Tidak | Ya |

---

## 2. Analisis dan Pembahasan

1. **Layer Caching dan Urutan Instruksi Dockerfile:**
   Build pertama memakan waktu 740.65 s karena Docker harus mengunduh dan mengompilasi dependensi sistem melalui APT. Pada build kedua, layer caching digunakan kembali sehingga proses selesai dalam hitungan detik, terpangkas drastis menjadi 3.31s. Instruksi `COPY` diletakkan setelah instalasi dependensi agar perubahan kode harian tidak memicu instalasi ulang paket dependensi yang memakan waktu.
2. **Trade-off Image ros-base vs ros-desktop:**
   Image dasar `ros:humble-ros-base-jammy` menghasilkan footprint image akhir sebesar 1.89 GB. Ukuran ini jauh lebih ringkas dibanding image `ros-desktop` penuh yang dapat melebihi 4 GB, dengan dependensi GUI tetap terpenuhi lewat instalasi selektif di Dockerfile.
3. **Konfigurasi `network_mode: host` dan `ipc: host`:**
   Memungkinkan DDS (Data Distribution Service) dan shared memory transport berkomunikasi langsung dengan stack ROS 2 tanpa latensi port mapping atau isolasi bridge container.
4. **Perilaku Artefak Build:**
   Jika dijalankan `docker compose down -v`, named volume `ws_build` dan `ws_install` akan dihapus permanen, mengharuskan kompilasi ulang saat container diaktifkan kembali.

---

## 3. Log Troubleshooting

| Problem | Symptom | Root Cause | Solution | Verification |
|---|---|---|---|---|
| Eksekusi Shell Script | `exec /entrypoint.sh: exec format error` | File script `entrypoint.sh` menggunakan format line-ending Windows (CRLF). | Mengonversi ke format LF Linux murni dan rebuild layer image. | Container menyala dan berstatus `Up` saat `docker compose ps`. |
| Izin Akses Direktori Build | `PermissionError: [Errno 13] Permission denied: 'build/.built_by'` | Named volume `ws_build` dibuat oleh root, sedangkan container berjalan sebagai user `dev`. | Mengubah kepemilikan direktori kerja menggunakan `chown -R dev:dev /ws`. | Perintah `colcon build --symlink-install` berhasil tanpa error (`Summary: 1 package finished [1.61s]`). |
|Konteks Build Docker (Build Context Path)| ERROR [4/6] COPY entrypoint.sh /entrypoint.sh dan failed to compute cache key: ... "/entrypoint.sh": not found | Path sumber entrypoint.sh tidak ditemukan oleh Docker daemon karena build context pada compose.yaml mengarah ke direktori root repositori, bukan subdirektori docker/. | Mengubah instruksi salin berkas pada Dockerfile menjadi COPY docker/entrypoint.sh /entrypoint.sh.| Perintah docker compose build berhasil mengeksekusi step [4/6] tanpa error not found.
