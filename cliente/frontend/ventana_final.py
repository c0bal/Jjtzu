import sys
from PyQt5 import uic
from utils import data_json
from os.path import join
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal


window_name, base_class = uic.loadUiType(join(*data_json("RUTA_VENTANA_FINAL")))

class VentanaFinal(window_name, base_class):
    senal_voler_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.volver_buton.clicked.connect(self.volver_inicio)
        self.init_gui()
    
    def init_gui(self):
        self.setWindowTitle("Ventana de Final")

    def volver_inicio(self):
        self.senal_voler_inicio.emit()

    def iniciar(self, dic):
        self.final_text.setText(dic["texto"])
        self.final_text.repaint()
        self.show()  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaFinal()
    sys.exit(app.exec_())