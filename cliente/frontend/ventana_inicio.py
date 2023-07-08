import sys
from PyQt5 import uic
from utils import data_json
from os.path import join
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, Qt


window_name, base_class = uic.loadUiType(join(*data_json("RUTA_VENTANA_INICIO")))

class VentanaInicio(window_name, base_class):
    senal_enviar_login = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.encima_puerta = False
        self.no_bloqueo = True
        self.init_gui()
    
    def init_gui(self):
        self.setWindowTitle("Ventana de Inicio")
        self.puerta_abierta.hide()
        self.esperando.hide()
        self.errores.hide()
       
        self.iniciar()

    def mouseMoveEvent(self, e):
        if self.no_bloqueo:
            x = e.x()
            y = e.y()
            if (455 >= x >= 364) and (366 >= y >= 265):
                self.puerta_abierta.show()
                self.encima_puerta = True
            else:
                self.puerta_abierta.hide()
                self.encima_puerta = False

    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton and self.encima_puerta and self.no_bloqueo:
            self.errores.setText("")
            self.enviar_login()
            
    def enviar_login(self):
        """cuando se apreta la puerta"""
        nombre_usuario = self.usuario_text.text()
        diccionario = {
            "comando": "validar_login",
            "nombre usuario": nombre_usuario}
        self.senal_enviar_login.emit(diccionario)

    def iniciar(self):
        self.show()

    def mostrar_error(self, errores):
        mensaje = "-".join(errores)
        self.errores.setText(mensaje)
        self.errores.show()

    def reset(self):
        self.usuario_text.show()
        self.puerta_abierta.hide()
        self.esperando.hide()
        self.errores.hide()
        self.encima_puerta = False
        self.no_bloqueo = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaInicio()
    sys.exit(app.exec_())