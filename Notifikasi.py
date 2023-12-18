from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDateTimeEdit, QMessageBox, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from plyer import notification
from datetime import datetime

class NotifierApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Pengingat')
        self.setGeometry(100, 100, 400, 398)

        # Load Image
        img = QPixmap(r"D:\Kuliah Semester 3\Python\test\gambarnotif.png")
        img_label = QLabel()
        img_label.setPixmap(img)

        # Label - Title
        t_label = QLabel("judul pengingat", self)
        self.title = QLineEdit(self)

        # Label - Message
        m_label = QLabel("Pesan", self)
        self.msg = QLineEdit(self)

        # Label - DateTime
        dt_label = QLabel("Set tanggal dan waktu", self)
        self.datetime_edit = QDateTimeEdit(self)
        self.datetime_edit.setDateTime(datetime.now())

        # Button
        but = QPushButton("SET NOTIFIKASI", self)
        but.clicked.connect(self.schedule_notification)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(img_label)
        layout.addWidget(t_label)
        layout.addWidget(self.title)
        layout.addWidget(m_label)
        layout.addWidget(self.msg)
        layout.addWidget(dt_label)
        layout.addWidget(self.datetime_edit)
        layout.addWidget(but)

        # Timer for scheduling notifications
        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(self.show_notification)

    def schedule_notification(self):
        selected_datetime = self.datetime_edit.dateTime().toPyDateTime().replace(tzinfo=None)
        current_datetime = datetime.now()

        if selected_datetime <= current_datetime:
            QMessageBox.critical(self, "Alert", "Please select a future date and time!")
        else:
            time_difference = selected_datetime - current_datetime
            milliseconds_until_notification = int(time_difference.total_seconds() * 100)

            # Schedule the notification using a QTimer
            self.notification_timer.start(milliseconds_until_notification)

    def show_notification(self):
        self.notification_timer.stop()  # Stop the timer to avoid repeated notifications
        get_title = self.title.text()
        get_msg = self.msg.text()

        # Use plyer's notification with a longer timeout
        notification.notify(
            title=get_title,
            message=get_msg,
            app_name="Notifier",
            timeout=10  # Use a longer timeout, e.g., 10 seconds
        )