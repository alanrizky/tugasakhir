import csv
import locale
import os
import pickle
import re
import sqlite3
import sys
import time
import timeit
from datetime import datetime
from pathlib import Path
from sqlite3 import Error

import cv2
import face_recognition
import pyautogui
import pygetwindow as gw
import pywinauto
from pywinauto.keyboard import send_keys

locale.setlocale(locale.LC_ALL, "id_ID")


def input_kelas(prompt, on_validationerror):
    nama_kelas = input(prompt)
    while not re.match("^(MI|TI)[1-4][A-I]$", nama_kelas, re.I):
        print(on_validationerror + "\nContoh Format kelas: TI4C")
        nama_kelas = input(prompt)
    return nama_kelas


nama_kelas = input_kelas("Masukkan kelas: ", "Format kelas salah!")

matkul = input("Nama mata kuliah: ")
while matkul == "":
    print("Nama mata kuliah tidak boleh kosong!")
    matkul = input("Nama mata kuliah: ")


def focus_to_window(window_title=None):
    window = gw.getWindowsWithTitle(window_title)[0]
    if not window.isActive:
        pywinauto.application.Application(backend='uia').connect(handle=window._hWnd).top_window().set_focus()


def maximize_window(window_title=None):
    window = gw.getWindowsWithTitle(window_title)[0]
    if not window.isMaximized:
        window.maximize()


img_num = 1
data = pickle.loads(open("encodings_file.pickle", "rb").read())

while True:
    sleep = 60  # absen selama 1 menit

    # Memastikan aplikasi zoom terlihat di tampilan monitor (tidak minimize/aktif)

    try:
        focus_to_window("DATASET+DATA UJI.mp4")  # line code untuk media player classic
        maximize_window("DATASET+DATA UJI.mp4")  # ganti ke "Zoom Meeting" untuk aplikasi Zoom
    except:
        print("Tidak ada zoom yang berjalan")
        exit()

    time.sleep(1)


    def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        return cv2.resize(image, dim, interpolation=inter)


    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot\\screenshot.jpg")

    send_keys("%{TAB}")

    now = datetime.now()
    waktu = now.strftime('%H:%M:%S')
    tanggal = now.strftime('%d/%B/%Y')


    def buat_koneksi(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn


    def buat_tabel(conn, table_query):
        try:
            c = conn.cursor()
            c.execute(table_query)
        except Error as e:
            print(e)


    def presensi_mahasiswa(conn, data_insert):
        sql = """ INSERT INTO presensi(nim_mahasiswa, nama_mahasiswa, waktu_hadir, tanggal, kelas) 
                  VALUES(?,?,?,?,?)"""
        cur = conn.cursor()
        cur.execute(sql, data_insert)
        conn.commit()

        return cur.lastrowid


    database = r"test.db"

    create_table_query = """ CREATE TABLE IF NOT EXISTS presensi (
                             no integer PRIMARY KEY,
                             nim_mahasiswa varchar(50) NOT NULL,
                             nama_mahasiswa varchar(50) NOT NULL,
                             waktu_hadir datetime NOT NULL,
                             tanggal datetime NOT NULL,
                             kelas varchar(4) NOT NULL
                             ); """

    connection = buat_koneksi(database)
    if connection is not None:
        buat_tabel(connection, create_table_query)

    image = cv2.imread("screenshot/screenshot.jpg")
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    start_time = timeit.default_timer()
    print("\n[INFO] melakukan presensi...")
    boxes = face_recognition.face_locations(rgb, model="cnn")
    encodings = face_recognition.face_encodings(rgb, boxes, num_jitters=50, model="large")
    names = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.4)
        name = "Unknown"
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
        print(name)
        names.append(name)

    filt = re.compile("(?!Unknown).*")
    un_list = list(filter(filt.match, names))
    print("\nJumlah berhasil dikenali: " + str(len(un_list)))

    print("Jumlah berhasil dideteksi: " + str(len(names)))

    if any("Unknown" in s for s in names):
        print("Jumlah gagal dikenali: " + str(names.count("Unknown")))

    for ((top, right, bottom, left), name) in zip(boxes, names):
        if name == "Unknown":
            split_string = name.split(' ', 1)
            substring = split_string[0]
            cv2.rectangle(image, (left + 10, top + 10), (right + 10, bottom + 10), (0, 0, 255), 2)
            y = top - 7 if top - 7 > 7 else top + 7
            cv2.putText(image, substring, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 255), 2)
        else:
            split_string = name.split(' ', 1)
            substring = split_string[0]
            cv2.rectangle(image, (left + 10, top + 10), (right + 10, bottom + 10), (0, 255, 0), 2)
            y = top - 7 if top - 7 > 7 else top + 7
            cv2.putText(image, substring, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 0), 2)

        with connection:
            if name != "Unknown":
                try:
                    insert_presensi_mahasiswa = (
                        name.split(' ', 1)[1],
                        name.split(' ', 1)[0],
                        waktu,
                        tanggal,
                        nama_kelas.upper())
                    presensi_mahasiswa(connection, insert_presensi_mahasiswa)
                except:
                    insert_presensi_mahasiswa = (
                        "-",
                        name.split(' ', 1)[0],
                        waktu,
                        tanggal,
                        nama_kelas.upper())
                    presensi_mahasiswa(connection, insert_presensi_mahasiswa)
    cursors = connection.cursor()
    cursors.execute("select * from presensi where waktu_hadir='{}'".format(waktu))
    filename = nama_kelas.upper() + "_" + matkul.upper() + "_" + now.strftime('%d-%m-%Y') + ".csv"
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline='') as f:
        headers = [i[0] for i in cursors.description]
        write = csv.writer(f)
        writer1 = csv.DictWriter(f, headers)
        if not file_exists:
            writer1.writeheader()
        write.writerows(cursors)

    resize = ResizeWithAspectRatio(image, width=1920)

    Path("hasil/{}".format(filename.split(".csv")[0])).mkdir(parents=True, exist_ok=True)
    print("\n[INFO] menyimpan hasil di " + str(os.path.join("hasil/{}/".format(filename.split(".csv")[0]),
                                                            "{}.jpg".format(str(img_num))), ))
    cv2.imwrite(
        os.path.join("hasil/{}/".format(filename.split(".csv")[0]),
                     "{}.jpg".format(str(img_num))),
        resize)
    print("\nHasil ke-{} berhasil disimpan".format(str(img_num)))

    elapsed = timeit.default_timer() - start_time
    print("Presensi ke-{}".format(img_num) + " membutuhkan " + f"{elapsed:.3f}" + " detik\n")

    img_num += 1
    for i in range(sleep):
        time.sleep(1)
        print_out = f"\rPresensi berikutnya dalam %d" % int(sleep - 1) + " detik lagi"
        print(print_out, end='')
        sleep -= 1
        sys.stdout.flush()
    print("\n")
