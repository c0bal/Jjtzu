import sys
from PyQt5 import uic
from utils import data_json
from os.path import join
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtTest import QTest
from random import choice


window_name, base_class = uic.loadUiType(join(*data_json("RUTA_VENTANA_JUEGO")))

class Carta(QLabel):
    def __init__(self, parent):
        super(Carta, self).__init__(parent)
        self.setMaximumSize(80, 100)
        self.parent = parent 
        self.elemento = None
        self.color = None
        self.puntos = None
        self.ruta = None
        self.id = None
        self.permitido_seleccionar = False

    def mousePressEvent(self, evento):
        if evento.buttons() == Qt.LeftButton and self.permitido_seleccionar:
            for c in self.parent.cartas_en_juego:
                c.setStyleSheet("")
            self.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.parent.por_concretar = self.id

class VentanaJuego(window_name, base_class):
    senal_enviar_login = pyqtSignal(dict)
    senal_abrir_juego = pyqtSignal()
    senal_ronda_terminada = pyqtSignal(dict)
    senal_seleccionar_carta = pyqtSignal(dict)
    senal_tiempo_agotado = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cartas_a_mostrar = data_json("BARAJA_PANTALLA")
        self.a_mostrar = 0
        self.cartas_en_juego = []
        self.cartas_mazo_jugador = []
        self.cartas_rival_en_juego = []
        self.cartas_mazo_rival = []
        self.contador = data_json("CUENTA_REGRESIVA_RONDA")
        self.seleccionada = ""
        self.por_concretar = ""
        self.fichas_usuario = []
        self.fichas_rival = []
        self.permitido = False
        self.init_gui()
    
    def init_gui(self):
        self.setWindowTitle("Ventana de Juego")
        self.seleccionar_buton.clicked.connect(self.seleccionar)

    def seleccionar(self):
        if self.permitido:
            if self.por_concretar != "":
                self.seleccionada = self.por_concretar
                for c in self.cartas_en_juego:
                    if c.id == self.seleccionada:
                        pixels = QPixmap(join("frontend", "sprites", "cartas", c.ruta + ".png"))
                        self.jugador_carta.setPixmap(pixels)
                        c.setStyleSheet("")
                self.senal_seleccionar_carta.emit({"comando": "seleccionar_carta",
                                                "id": self.seleccionada})

    def reset(self):
        self.cartas_a_mostrar = data_json("BARAJA_PANTALLA")
        self.a_mostrar = 0
        self.cartas_en_juego = []
        self.cartas_mazo_jugador = []
        self.cartas_rival_en_juego = []
        self.cartas_mazo_rival = []
        self.contador = data_json("CUENTA_REGRESIVA_RONDA")
        self.seleccionada = ""
        self.por_concretar = ""
        self.fichas_usuario = []
        self.fichas_rival = []
        self.timer.stop()

    def crear_carta(self, card):
        carta = Carta(self)
        carta.id = self.a_mostrar
        carta.elemento = card["elemento"]
        carta.color = card["color"]
        carta.puntos = card["puntos"]
        carta.ruta = str(carta.color + "_" + carta.elemento + "_" + str(carta.puntos))
        pixels = QPixmap(join("frontend", "sprites", "cartas", carta.ruta + ".png"))
        carta.setPixmap(pixels)
        carta.setScaledContents(True) 
        return carta

    def cartas_rival(self, card):
        carta = Carta(self)
        carta.id = self.a_mostrar
        carta.elemento = card["elemento"]
        carta.color = card["color"]
        carta.puntos = card["puntos"]
        carta.ruta = str(carta.color + "_" + carta.elemento + "_" + str(carta.puntos))
        pixels = QPixmap(join("frontend", "sprites", "cartas", "back.png"))
        carta.setPixmap(pixels)
        carta.setScaledContents(True)
        carta.setMaximumSize(40, 50)
        return carta

    def mostrar_ronda(self):
        for c in self.cartas_en_juego:
            c.show()
        for c in self.cartas_rival_en_juego:
            c.show()

    def cargar_datos(self, dic):
        
        nombre = dic["nombre"]
        rival = dic["rival"]
        mazo_usuario = dic["mazo_1"]
        mazo_rival = dic["mazo_2"]
        
        self.jugador_text.setText(nombre)
        self.jugador_text.repaint()
        self.rival_text.setText(rival)
        self.rival_text.repaint()

        while self.a_mostrar < self.cartas_a_mostrar:
            card = mazo_usuario[str(self.a_mostrar)]
            carta = self.crear_carta(card)
            card2 = mazo_rival[str(self.a_mostrar)]
            carta2 = self.cartas_rival(card2)
            self.a_mostrar += 1
            self.cartas_en_juego.append(carta)
            self.cartas_rival_en_juego.append(carta2)
            carta.hide()
            carta2.hide()
        
        while self.a_mostrar < 15:
            card = mazo_usuario[str(self.a_mostrar)]
            carta = self.crear_carta(card)
            card2 = mazo_rival[str(self.a_mostrar)]
            carta2 = self.cartas_rival(card2)
            self.a_mostrar += 1
            self.cartas_mazo_jugador.append(carta)
            self.cartas_mazo_rival.append(carta2)    
            carta.hide()   
            carta2.hide()     

        for carta in self.cartas_en_juego:
            self.jugador_layout.addWidget(carta)

        for carta in self.cartas_rival_en_juego:
            self.vertical1.addWidget(carta)

        self.iniciar()

    def iniciar(self):
        self.contador = data_json("CUENTA_REGRESIVA_RONDA")
        self.seleccionada = ""
        self.por_concretar = ""
        self.show()
        self.cuenta.setText("SET")
        self.cuenta.repaint()
        QTest.qWait(300)
        self.cuenta.setText("GO")
        self.cuenta.repaint()
        QTest.qWait(100)
        self.permitido = True
        self.mostrar_ronda()
        for c in self.cartas_en_juego:
            c.permitido_seleccionar = True
        self.timer = QTimer()
        self.timer.timeout.connect(self.progreso)
        self.timer.start(1000)        

    def progreso(self):
        self.cuenta.setText(str(self.contador))
        self.cuenta.repaint()

        if self.contador == 0:
            if self.seleccionada == "":
                self.seleccionada = choice(self.cartas_en_juego).id
                for c in self.cartas_en_juego:
                    if c.id == self.seleccionada:
                        pixels = QPixmap(join("frontend", "sprites", "cartas", c.ruta + ".png"))
                        self.jugador_carta.setPixmap(pixels)
                self.senal_tiempo_agotado.emit({"comando": "no_time"})
                self.senal_seleccionar_carta.emit({"comando": "seleccionar_carta",
                                                "id": self.seleccionada})
        if self.contador != 0:
            self.contador -= 1

    def mostrar_resultados(self, mensaje):
        for c in self.cartas_en_juego:
            c.permitido_seleccionar = False

        print(mensaje)

        id_carta_usuario = mensaje["usuario"]
        id_carta_rival = mensaje["rival"]
        carta_usuario = ""
        carta_rival = ""
        
        # Muestro carta Rival y resultado
        for c in self.cartas_rival_en_juego:
            if int(c.id) == int(id_carta_rival):
                pixels = QPixmap(join("frontend", "sprites", "cartas", c.ruta + ".png"))
                self.rival_carta.setPixmap(pixels)
                carta_rival = c
        for c in self.cartas_en_juego:
            if int(c.id) == int(id_carta_usuario):
                carta_usuario = c
                       
        self.vertical1.removeWidget(carta_rival)

        comando = mensaje["comando"]
        if comando == "empate":
            self.result_text.setStyleSheet("background-color: rgb(85, 85, 127);")
            self.result_text.setText("EMPATE")
            self.result_text.repaint()
        
        elif comando == "gano":
            ficha = QLabel()
            ficha.setMaximumSize(30, 30)
            ruta_ficha = carta_usuario.elemento + "_" + carta_usuario.color + ".png"
            pixels = QPixmap(join("frontend", "sprites", "elementos", "fichas", ruta_ficha))
            ficha.setPixmap(pixels)
            ficha.setScaledContents(True)
            self.fichas_usuario.append(ficha)
            self.triunfo_usuario.addWidget(ficha)

            self.result_text.setStyleSheet("background-color: rgb(59, 222, 0);")
            self.result_text.setText("GANASTE LA RONDA")
            self.result_text.repaint()
        
        elif comando == "pierdo":
            ficha = QLabel()
            ficha.setMaximumSize(30, 30)
            ruta_ficha = carta_rival.elemento + "_" + carta_rival.color + ".png"
            pixels = QPixmap(join("frontend", "sprites", "elementos", "fichas", ruta_ficha))
            ficha.setPixmap(pixels)
            ficha.setScaledContents(True)
            self.fichas_rival.append(ficha)
            self.triunfo_rival.addWidget(ficha)

            self.result_text.setStyleSheet("background-color: rgb(217, 0, 0);")
            self.result_text.setText("PERDISTE LA RONDA")
            self.result_text.repaint()
        QTest.qWait(5000)

        #Reseteo Ronda:-----------------------------------------------------------
        self.result_text.setStyleSheet("transparent;")
        self.result_text.setText("")
        self.result_text.repaint() 
        
        #Ocultar Cartas
        pixels = QPixmap(join("frontend", "sprites", "cartas", "back.png"))
        self.rival_carta.setPixmap(pixels)

        pixels = QPixmap("")
        self.jugador_carta.setPixmap(pixels)  

        # Elimino la en pantalla y meto en el mazo
        self.cartas_en_juego.remove(carta_usuario)
        self.cartas_rival_en_juego.remove(carta_rival)
        self.cartas_mazo_jugador.append(carta_usuario)
        self.cartas_mazo_rival.append(carta_rival)

        # Meto una en la pantalla y la elimino del mazo
        self.cartas_en_juego.append(self.cartas_mazo_jugador[0])
        self.cartas_mazo_jugador.pop(0)
        self.cartas_rival_en_juego.append(self.cartas_mazo_rival[0])
        self.cartas_mazo_rival.pop(0)

        self.actualizar_layout(carta_usuario, carta_rival)
        self.iniciar()

    def actualizar_layout(self, carta_usuario, carta_rival):
        '''
        Remuevo las cartas entregadas y inserto la -1 del en juego
        '''
        #Actualizar layout jugador
        self.jugador_layout.removeWidget(carta_usuario)
        self.jugador_layout.addWidget(self.cartas_en_juego[-1])
        
        #Actualizar layout rival
        self.vertical1.addWidget(self.cartas_rival_en_juego[-1])      


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaJuego()
    sys.exit(app.exec_())