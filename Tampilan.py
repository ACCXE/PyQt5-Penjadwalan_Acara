from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime, timedelta, date
from Detail_Acara import Ui_Detail_Acara
from Kontrol_Acara import Kontrol_Acara
from Filter import FilterApp
import mysql.connector

class Ui_Tampilan(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(481, 358)

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(50, 20, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(50, 80, 381, 251))
        self.listWidget.setObjectName("listWidget")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(340, 20, 91, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_filter_window)
        # Menghubungkan sinyal doubleClicked ke fungsi show_details
        self.listWidget.doubleClicked.connect(self.show_details)

        self.retranslateUi(Form)

        # Buat instance AcaraController dengan konfigurasi database yang sesuai
        self.acara_controller = Kontrol_Acara({
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'jadwal_acara',
        })

        # Buat instance FilterApp dengan kontrol_acara dan callback yang sesuai
        self.filter_app = FilterApp("Filter Acara", self.acara_controller, self.update_list_widget, self)
        self.filter_app.main_ui = self  # Atur atribut main_ui pada objek FilterApp

        

    def filter_acara(self):
        # Mendapatkan tipe filter dari ComboBox
        filter_type = self.comboBox.currentText()

        # Set filter type di objek FilterApp
        self.filter_app.filter_type = filter_type

        # Panggil metode apply_filter dari objek FilterApp
        self.filter_app.apply_filter()

    def update_list_widget(self, data):
        # Hapus semua item di listWidget sebelum memperbarui
        self.listWidget.clear()

        # Check if filter_type is set
        if hasattr(self.filter_app, 'filter_type') and self.filter_app.filter_type is not None:
            # Filter data based on filter type
            filtered_data = [item for item in data if item[1] == self.filter_app.filter_type]
            for item in filtered_data:
                self.listWidget.addItem(str(item[1]))
        else:
            # Display all data if no filter type is selected
            for item in data:
                self.listWidget.addItem(str(item[1]))

    def tampilkan_detail_acara(self, original_data):
        detail_acara_dialog = QtWidgets.QDialog()
        detail_acara_ui = Ui_Detail_Acara(self.acara_controller, original_data)
        detail_acara_ui.setupUi(detail_acara_dialog)
        result = detail_acara_dialog.exec_()

    def show_filter_window(self):
        # Panggil metode show_filter_window dari objek FilterApp
        self.filter_app.show()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Daftar Acara:"))
        self.pushButton.setText(_translate("Form", "Filter"))

    def show_details(self):
        # Mendapatkan item yang dipilih dari QListWidget
        selected_item = self.listWidget.currentItem()

        # Pernyataan print tambahan
        print("Nama Acara yang Dipilih:", selected_item.text())

        # Memastikan ada item yang dipilih sebelum melanjutkan
        if selected_item:
            # Menyimpan data awal sebelum diedit
            data_item = self.acara_controller.get_data_database(selected_item.text())

            # Pernyataan print tambahan
            print("Data Item dari Database:", data_item)

            # Memastikan data_item tidak None dan memiliki panjang yang cukup
            if data_item is not None and len(data_item) > 0:
                data_item = data_item[0]  # Ambil elemen pertama dari tuple

                self.original_data = {
                    "Nama Acara": data_item[1],
                    "Tanggal": QtCore.QDate.fromString(str(data_item[2]), "yyyy-MM-dd"),
                    "Waktu": QtCore.QTime.fromString(str(data_item[3]), "hh:mm:ss"),
                    "Deskripsi Acara": data_item[4],
                }

                # Membuat instance dari dialog Detail_Acara
                detail_acara_dialog = QtWidgets.QDialog()
                detail_acara_ui = Ui_Detail_Acara()

                # Creating an instance of Ui_Detail_Acara and initializing it
                detail_acara_ui.initialize(self.acara_controller, selected_item.text())

                # Setting up the UI for the detail view
                detail_acara_ui.setupUi(detail_acara_dialog)

                # Menampilkan data pada UI Detail_Acara
                detail_acara_ui.setLineEditValues(self.original_data)

                # Menampilkan dialog Detail_Acara
                if detail_acara_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    # Update QListWidget
                    self.update_list_widget(self.acara_controller.get_acara_by_filter_type(self.filter_app.filter_type))
            else:
                # Menampilkan pesan kesalahan jika data_item tidak lengkap atau tidak tersedia
                error_message = f"Data untuk item dengan nama acara '{selected_item.text()}' tidak tersedia atau tidak lengkap."
                QtWidgets.QMessageBox.critical(self.listWidget, "Error", error_message)
                print(error_message)  # Tambahkan ini untuk mencetak informasi tambahan ke terminal
        else:
            # Menampilkan pesan kesalahan jika tidak ada item yang dipilih
            QtWidgets.QMessageBox.critical(self.listWidget, "Error", "Tidak ada item yang dipilih.")

    def get_data_database(self, nama_acara):
        # Assuming 'acara_controller' is an instance of Kontrol_Acara
        return self.acara_controller.get_data_database(nama_acara)
    
    def tampilkan_detail_acara(self, original_data):
        detail_acara_dialog = QtWidgets.QDialog()
        detail_acara_ui = Ui_Detail_Acara()
        detail_acara_ui.initialize(self.acara_controller, original_data)
        detail_acara_ui.setupUi(detail_acara_dialog)
        result = detail_acara_dialog.exec_()
