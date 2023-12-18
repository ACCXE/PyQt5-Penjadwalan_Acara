from PyQt5.QtWidgets import QApplication, QMainWindow
from Jadwal import Ui_MainWindow

if __name__ == "__main__":
    app = QApplication([])
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()