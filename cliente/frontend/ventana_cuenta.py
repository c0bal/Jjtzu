import sys
from PyQt5 import uic
from utils import data_json
from os.path import join
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, Qt, QTimer


window_name, base_class = uic.loadUiType(join(*data_json("RUTA_VENTANA_CUENTA")))

class VentanaCuenta(window_name, base_class):
    senal_enviar_login = pyqtSignal(dict)
    senla_enviar_volver = pyqtSignal(dict)
    senal_preparar_juego = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.contador = data_json("CUENTA_REGRESIVA_INICIO")
        self.boton_volver.clicked.connect(self.volver)
        self.init_gui()
    
    def init_gui(self):
        self.setWindowTitle("Ventana de Cuenta")
        self.cuenta.setText(str(self.contador))

    def volver(self):
        diccionario = {
            "comando": "volver_inicio"}
        self.senla_enviar_volver.emit(diccionario)

    def progreso(self):
        self.cuenta.setText(str(self.contador))
        self.cuenta.repaint()

        if self.contador == 0:
            self.senal_preparar_juego.emit({"comando": "pedir_mazo"}) 
        self.contador -= 1

    def iniciar(self, dic):
        self.show()
        self.j1.setText(dic["p1"])
        self.j1.repaint()
        self.j2.setText(dic["p2"])
        self.j2.repaint() 
        self.cuenta.show() 
        self.timer = QTimer()
        self.timer.timeout.connect(self.progreso)
        self.timer.start(1000)

    def esperando(self, nombre):
        self.j1.setText(nombre)
        self.j2.setText("Esperando Rival")
        self.show()
        self.cuenta.hide()

    def detener(self):
        self.contador = data_json("CUENTA_REGRESIVA_INICIO")
        self.cuenta.setText(str(self.contador))
        self.cuenta.repaint()        
        self.timer.stop()
        self.cuenta.hide()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaCuenta()
    sys.exit(app.exec_())