import sys
from PyQt5 import uic
from utils import data_json
from os.path import join
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel

window_name, base_class = uic.loadUiType(join(*data_json("RUTA_VENTANA_CHAT")))

class VentanaChat(window_name, base_class):
    senal_enviar_chat = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.chat_labels = []
        self.init_gui()
    
    def init_gui(self):
        self.enviar_buton.clicked.connect(self.mandar_mensaje)

    def mandar_mensaje(self):
        m = self.chat.text()
        mensaje = self.nombre + ": " + m
        self.senal_enviar_chat.emit({"comando": "chat",
                                    "mensaje": mensaje})
        self.colocar_mensaje(mensaje)
    
    def colocar_mensaje(self, m):
        label = QLabel()
        label.setText(m)
        self.vertical.insertWidget(-1, label)
        if len(self.vertical) >= 20:
            self.vertical.removeWidget(self.chat_labels[0])
            self.chat_labels.pop(0)
        label.show()
        self.chat_labels.append(label)
        self.chat.setText("")

    def recibir_mensaje(self, m):
        label = QLabel()
        label.setText(m)
        self.vertical.insertWidget(-1, label)
        if len(self.vertical) >= 27:
            self.vertical.removeWidget(self.chat_labels[0])
            self.chat_labels.pop(0)
        label.show()
        self.chat_labels.append(label)   
        self.chat.setText("")     

    def iniciar(self, nombre):
        self.nombre = nombre
        self.setWindowTitle(f"Ventana de Chat {self.nombre}")
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaChat()
    sys.exit(app.exec_())