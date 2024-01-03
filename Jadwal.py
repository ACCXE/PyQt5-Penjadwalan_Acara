from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDateTimeEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from plyer import notification
from datetime import datetime, timedelta
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox
from Tampilan import Ui_Tampilan
import calendar
import mysql.connector
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(754, 602)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 30, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(390, 30, 321, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 100, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 170, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(390, 100, 161, 41))
        self.dateEdit.setObjectName("dateEdit")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(390, 170, 161, 41))
        self.timeEdit.setObjectName("timeEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(140, 220, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(40, 310, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(390, 310, 321, 141))
        self.textEdit.setUndoRedoEnabled(True)
        self.textEdit.setObjectName("textEdit")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 240, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(390, 240, 81, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(500, 240, 81, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(170, 480, 151, 61))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(430, 480, 151, 61))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_4.clicked.connect(self.tambahAcara)
        self.pushButton_6.clicked.connect(self.tampilkan_acara)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 754, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.notification_timer = QTimer(self.centralwidget)
        self.notification_timer.timeout.connect(self.show_notification)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Penjadwalan Acara"))
        self.label.setText(_translate("MainWindow", "Nama Acara:"))
        self.label_2.setText(_translate("MainWindow", "Tanggal:"))
        self.label_3.setText(_translate("MainWindow", "Waktu:"))
        self.label_6.setText(_translate("MainWindow", "Deskripsi Acara:"))
        self.label_5.setText(_translate("MainWindow", "Pengingat:"))
        self.pushButton.setText(_translate("MainWindow", "Ya"))
        self.pushButton_2.setText(_translate("MainWindow", "Tidak"))
        self.pushButton_4.setText(_translate("MainWindow", "Tambah Acara"))
        self.pushButton_6.setText(_translate("MainWindow", "Tampilkan Acara"))

    def tambahAcara(self):
        # Ambil data dari UI
        event_name = self.lineEdit.text()
        event_date = self.dateEdit.date().toString("yyyy-MM-dd")
        event_time = self.timeEdit.time().toString("hh:mm:ss")
        event_description = self.textEdit.toPlainText()

        # Validasi data
        if not event_date or not event_time:
            QMessageBox.critical(self.centralwidget, "Error", "Tanggal dan Waktu harus diisi.")
            return

        try:
            # Konfigurasi koneksi ke database MySQL
            db_config = {
                'host': 'localhost',
                'user': 'root',
                'password': '',
                'database': 'jadwal_acara',
            }

            # Membuat koneksi
            connection = mysql.connector.connect(**db_config)

            # Membuat kursor
            cursor = connection.cursor()

            # Tentukan Filter Type berdasarkan tanggal acara
            filter_type = self.determine_filter_type(event_date)

            # Query untuk menyimpan data
            query = "INSERT INTO acara (Nama_Acara, Tanggal, Waktu, Deskripsi_Acara, Filter_Type) VALUES (%s, %s, %s, %s, %s)"
            values = (event_name, event_date, event_time, event_description, filter_type)

            # Eksekusi query
            cursor.execute(query, values)

            # Commit perubahan ke database
            connection.commit()

            # Menutup kursor dan koneksi
            cursor.close()
            connection.close()

            # Mengatur nilai default setelah acara ditambahkan
            self.lineEdit.clear()
            self.dateEdit.setDate(QtCore.QDate.currentDate())
            self.timeEdit.setTime(QtCore.QTime.currentTime())
            self.textEdit.clear()

            # Memberikan notifikasi bahwa acara berhasil ditambahkan
            QMessageBox.information(
                self.centralwidget, "Sukses", "Acara berhasil ditambahkan ke database.")
        except Exception as e:
            # Menampilkan pesan error jika terjadi masalah
            QMessageBox.critical(self.centralwidget, "Error", f"Terjadi kesalahan: {str(e)}")

    def determine_filter_type(self, event_date):
        # Tentukan Filter Type berdasarkan tanggal acara
        selected_date = datetime.strptime(event_date, "%Y-%m-%d").date()
        today = datetime.now().date()

        _, last_day_of_month = calendar.monthrange(today.year, today.month)
        _, last_day_of_selected_month = calendar.monthrange(selected_date.year, selected_date.month)

        end_of_week = today + timedelta(days=(calendar.SATURDAY - today.weekday()))
        end_of_month = datetime(today.year, today.month, last_day_of_month).date()

        if selected_date == today:
            return "Harian"
        elif today <= selected_date <= end_of_week:
            return "Mingguan"
        elif today <= selected_date <= end_of_month:
            return "Bulanan"
        else:
            return "Semua"
        
    def showNotificationFromNotifierApp(self):
        print("Entering showNotificationFromNotifierApp")

        # Extract relevant data from Ui_MainWindow
        event_name = self.lineEdit.text()
        event_date = self.dateEdit.date().toString("yyyy-MM-dd")
        event_time = self.timeEdit.time().toString("hh:mm:ss")
        event_description = self.textEdit.toPlainText()

        # Validasi: Pastikan pengingat dijadwalkan dengan acara
        if not (event_date and event_time):
            print("Pengingat dijadwalkan tanpa acara")
            self.notification_timer.start(0)  # Menjalankan timer tanpa waktu tunggu
            return

        # Validasi: Pastikan nama acara diisi
        if not event_name:
            print("Nama Acara harus diisi")
            QMessageBox.critical(self.centralwidget, "Error", "Nama Acara harus diisi.")
            return

        # Validasi: Jangan tampilkan notifikasi jika waktu yang dipilih sudah berlalu
        selected_datetime_str = f"{event_date} {event_time}"
        selected_datetime = datetime.strptime(selected_datetime_str, "%Y-%m-%d %H:%M:%S")
        current_datetime = datetime.now()

        if selected_datetime <= current_datetime:
            print("Waktu yang dipilih sudah berlalu")
            QMessageBox.critical(self.centralwidget, "Error", "Waktu yang dipilih sudah berlalu.")
            return

        # Validasi: Pastikan deskripsi acara diisi
        if not event_description:
            print("Deskripsi Acara harus diisi")
            QMessageBox.critical(self.centralwidget, "Error", "Deskripsi Acara harus diisi.")
            return

        # Calculate time difference in seconds
        time_difference = (selected_datetime - current_datetime).total_seconds()

        # Schedule the notification using a QTimer
        self.notification_timer.start(int(time_difference * 1000))

        print("Notification scheduled")

    def show_notification(self):
        # Stop the timer to avoid repeated notifications
        self.notification_timer.stop()

        # Extract relevant data from Ui_MainWindow
        event_name = self.lineEdit.text()
        event_description = self.textEdit.toPlainText()

        # Set data for notification
        get_title = event_name
        get_msg = event_description

        # Use plyer's notification with a longer timeout
        try:
            notification.notify(
                title=get_title,
                message=get_msg,
                app_name="Notifier",
                timeout=20
            )
            print("Notification shown")
        except Exception as e:
            print(f"Error showing notification: {e}")

    def tampilkan_acara(self):
        # Membuat instance dari QWidget untuk menampilkan antarmuka pengguna
        self.form_widget = QtWidgets.QWidget()

        # Membuat instance dari Ui_Form dan menampilkan form
        ui_form = Ui_Tampilan()
        ui_form.setupUi(self.form_widget)

        # Menyimpan rujukan ke Ui_Form
        self.form_ui = ui_form

        # Mengambil data dari database
        try:
            # Konfigurasi koneksi ke database MySQL
            db_config = {
                'host': 'localhost',
                'user': 'root',
                'password': '',
                'database': 'jadwal_acara',
            }

            # Membuat koneksi
            connection = mysql.connector.connect(**db_config)

            # Membuat kursor
            cursor = connection.cursor()

            # Query untuk mengambil semua data acara
            query = "SELECT Nama_Acara FROM acara"
            cursor.execute(query)

            # Mendapatkan semua data
            all_events = cursor.fetchall()

            # Menutup kursor dan koneksi
            cursor.close()
            connection.close()

            # Menampilkan nama acara pada QListWidget
            for event in all_events:
                ui_form.listWidget.addItem(event[0])

            # Tampilkan form
            self.form_widget.show()
        except Exception as e:
            # Menampilkan pesan error jika terjadi masalah
            QMessageBox.critical(self.centralwidget, "Error",f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    app = QApplication([])
    MainWindow = QMainWindow()
    ui_main = Ui_MainWindow()
    ui_main.setupUi(MainWindow)

    # Hanya membuat koneksi di __main__
    ui_main.pushButton.clicked.connect(ui_main.showNotificationFromNotifierApp)
    ui_main.pushButton_6.clicked.connect(ui_main.tampilkan_acara)

    MainWindow.show()
    sys.exit(app.exec())
