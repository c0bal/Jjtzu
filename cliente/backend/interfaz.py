"""
Ventana principal del cliente que se encarga de funcionar como backend de la
mayoria de ventanas, de conectar señales y de procesar los mensajes recibidos
por el cliente
"""
from PyQt5.QtCore import QObject, pyqtSignal
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_cuenta import VentanaCuenta
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_final import VentanaFinal
from frontend.ventana_chat import VentanaChat

class Interfaz(QObject):
    senal_abrir_mensaje_espera = pyqtSignal(str)
    senal_abrir_ventana_espera = pyqtSignal()
    senal_login_rechazado = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.ventana_inicio = VentanaInicio()
        self.ventana_cuenta = VentanaCuenta()
        self.ventana_juego = VentanaJuego()
        self.ventana_final = VentanaFinal()
        self.ventana_chat = VentanaChat()
        # -----------------------------------------

    def mostrar_ventana_inicio(self):
        self.ventana_inicio.iniciar()

    def cerrar_final(self):
        self.ventana_final.close()
        self.mostrar_ventana_inicio()

    def manejar_mensaje(self, mensaje: dict):
        """
        Maneja un mensaje recibido desde el servidor.
        """
        try:
            comando = mensaje["comando"]
        except KeyError: 
            return {}

        if comando == "respuesta_validacion_login":
            if mensaje["estado"] == "aceptado":
                self.ventana_inicio.reset()
                self.ventana_inicio.close()
                self.ventana_cuenta.esperando(mensaje["nombre"])
            elif mensaje["estado"] == "rechazado":
                self.senal_login_rechazado.emit(mensaje["error"])
        
        elif comando == "respuesta_sala_completada":
            self.ventana_inicio.close()
            self.ventana_cuenta.iniciar(mensaje)
        
        elif comando == "desconexion_rival":
            self.ventana_cuenta.detener()
            self.ventana_cuenta.esperando(mensaje["restante"])
        
        elif comando == "respuesta_volver_inicio":
            self.ventana_cuenta.detener()
            self.ventana_cuenta.close()
            self.ventana_inicio.reset()
            self.mostrar_ventana_inicio()
        
        elif comando == "respuesta_mazo":
            self.ventana_chat.iniciar(mensaje["nombre"])
            self.ventana_juego.cargar_datos(mensaje)
            self.ventana_cuenta.detener()
            self.ventana_cuenta.close()
        
        elif comando == "empate":
            self.ventana_juego.timer.stop()
            self.ventana_juego.mostrar_resultados(mensaje)
        elif comando == "gano":
            self.ventana_juego.timer.stop()
            self.ventana_juego.mostrar_resultados(mensaje)
        elif comando == "pierdo":
            self.ventana_juego.timer.stop()
            self.ventana_juego.mostrar_resultados(mensaje)
        
        elif comando == "resultado":
            self.ventana_juego.timer.stop()
            self.ventana_juego.close()
            self.ventana_chat.close()
            self.ventana_chat = VentanaChat()
            self.ventana_juego = VentanaJuego()
            self.ventana_final.iniciar(mensaje)
        
        elif comando == "fin_timer":
            self.ventana_juego.permitido = False
            self.ventana_juego.timer.stop()
        
        elif comando == "chat":
            self.ventana_chat.recibir_mensaje(mensaje["mensaje"])
        
        elif comando == "cerrar_chat":
            self.ventana_chat.close()
            self.ventana_chat = VentanaChat()

