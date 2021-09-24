## Versi Python: 3.9 64-bit
## Hanya bekerja di Windows 10 64-bit

## A. Menjalankan File EXE
# 1. Persiapan:
> 1. Download aplikasi [di sini](https://drive.google.com/drive/u/4/folders/1rQz-WZunWNFY_f1EGSVhmoOSrNfdKkUm)
> 2. Extract `Aplikasi.zip`
> 3. Download video rekaman Zoom [di sini](https://drive.google.com/drive/u/4/folders/1cWqTxx0ZdY6TY4ON6KdkWnAkyZRXmuEn) (bisa salah satu)
> 4. Download media player classic [di sini](https://files3.codecguide.com/K-Lite_Codec_Pack_1646_Basic.exe), lalu install

# 2. Cara run:
> 1. Folder `1. Encode Face` untuk melakukan training dan folder `2. Recognize Face` untuk melakukan presensi
> 2. Masuk pada folder `1. Encode Face`, lalu jalankan `encode_faces.exe` tunggu sampai selesai
> 3. File `encode_faces.exe` akan menghasilkan file `encodings_file.pickle`. Copy file `encodings_file.pickle` kedalam folder `2. Recognize Face`
> 4. Putar video yang sudah didownload, menggunakan media player classic, bisa seek videonya sampai beberapa mahasiswa oncam
> 5. Jalankan file `recognize_faces_image.exe` Kemudian masukan kelas dan mata kuliah
> 6. Proses presensi dimulai

## B. Menjalankan melalui interpreter

# 1. Persiapan:
> 1. Install dlib terlebih dahulu. [Windows](https://learnopencv.com/install-dlib-on-windows/) | [MacOS](https://learnopencv.com/install-dlib-on-macos/) | `Disarankan menggunakan CUDA untuk penggunga nVidia GeForce`
> 2. Download code ini [di sini](https://codeload.github.com/alanrizky/tugasakhir/zip/refs/heads/main)
> 3. Download dataset [di sini](https://drive.google.com/drive/folders/1PaeCwKMrkeeK7ot8z1Lmcw8PzZ73Flws)
> 4. Extract ```tugasakhir-main.zip```
> 5. Extract ```dataset.rar``` di dalam folder ```tugasakhir-main.zip```

# 2. Cara run:
> 1. Jalankan ```encode_faces.py``` kemudian tunggu proses training
> 2. Buka video yang sudah di download [di sini](https://drive.google.com/drive/u/4/folders/1cWqTxx0ZdY6TY4ON6KdkWnAkyZRXmuEn) (bisa salah satu)
> 3. Jalankan ```recognize_faces_image.py``` kemudian isikan kelas dan mata kuliah
> 4. Melakukan proses presensi

## Catatan:
Ketika file `recognize_faces_image.exe` dijalankan akan menghasilkan folder/file:
1. `[Kelas]\_[Mata Kuliah]\_[Tanggal-Bulan-Tahun].csv` sebagai wajah yang berhasil dikenali. Contoh [di sini](https://i.ibb.co/42rYS5z/Capture.jpg)
2. Folder `hasil` dengan isi folder `[Kelas]\_[Mata Kuliah]\_[Tanggal-Bulan-Tahun]` dengan isi file screenshot `[angka].jpg` (angka adalah presensi ke). Contoh [di sini](https://i.ibb.co/ZxVn9k1/Capture.jpg)
3. File `test.db` yang berisi kumpulan wajah yang berhasil dikenali
Berikut adalah contoh salah satu data yang terdapat pada file `test.db` 

| no  | nim_mahasiswa | nama_mahasiswa | waktu_hadir | tanggal         | kelas |
|-----|---------------|----------------|-------------|-----------------|-------|
| 300 | 2041720161    | hilda          | 09:35:42    | 26/Agustus/2021 | TI1I  |


