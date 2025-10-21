import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream

from menu_ui import Ui_MainWindow  # Asegúrate de que este archivo exista

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()  # Ocultar el widget inicialmente
        self.ui.stackedWidget.setCurrentIndex(0)  # Mostrar la página de inicio
        self.ui.indexbtn2.setChecked(True) 
        
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
            + self.ui.full_menu_widget.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [5, 6]:  # Índices de las páginas de inicio y configuración
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    def on_indexbtn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_indexbtn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_becerrosbtn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_becerrosbtn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_animalesbtn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_animalesbtn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_corralesbtn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_corralesbtn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_propietariosbtn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_propietariosbtn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_bitacorabtn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def on_bitacorabtn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def on_reportesbtn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    def on_reportesbtn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    def on_seguridadbtn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(7)

    def on_seguridadbtn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(7)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("style.qss", "r") as style_file:
        style_str = style_file.read()
    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())