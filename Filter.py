from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QFormLayout, QComboBox
from Kontrol_Acara import Kontrol_Acara
import mysql.connector

class FilterApp(QDialog):
    def __init__(self, title, kontrol_acara, update_list_widget_callback, main_ui):
        super().__init__()
        self.setWindowTitle(title)
        self.kontrol_acara = kontrol_acara
        self.update_list_widget_callback = update_list_widget_callback
        self.filter_type = None  # Add a new attribute for filter type
        self.main_ui = main_ui  # Set the main_ui attribute

        self.create_widgets()

    def create_widgets(self):
        layout = QFormLayout()

        # Combo Box for filter types
        self.filter_type_combo = QComboBox()
        self.filter_type_combo.addItems(["Harian", "Mingguan", "Bulanan"])
        layout.addRow(QLabel("Filter Type:"), self.filter_type_combo)

        # Filter Button
        filter_button = QPushButton("Filter")
        filter_button.clicked.connect(self.apply_filter)
        layout.addRow(filter_button)

        # Status Label
        self.status_label = QLabel()
        layout.addRow(self.status_label)

        self.setLayout(layout)

        # Dictionary to store filter values
        self.filters = {"Filter Type": None}

    def apply_filter(self):
        # Set filter values based on user input
        filter_type = self.filter_type_combo.currentText()
        self.filters["Filter Type"] = filter_type
        self.main_ui.filter_type = filter_type  # Set filter type in the main UI

        # Call the get_acara_by_filter_type function with the set filter
        result = self.kontrol_acara.get_acara_by_filter_type(filter_type)

        # Update the view if there are filter results
        if result is not None:
            self.update_list_widget_callback(result)

        self.status_label.setText(f"Filter Applied: {self.filters}")

    