"""
Módulo principal del cliente.
"""
import sys
import socket
from PyQt5.QtWidgets import QApplication
from backend.cliente import Cliente
from backend.interfaz import Interfaz
from utils import data_json

if __name__ == "__main__":
    HOST = socket.gethostname()
    PORT = data_json("PORT")
    
    try:
        # =========> Instanciamos la APP <==========
        app = QApplication(sys.argv)
        
        # =========> Iniciamos el cliente <==========
        cliente = Cliente(HOST, PORT)
        interfaz = Interfaz()

        # =========> Conectamos señales <==========
        
        # Cliente
        cliente.senal_mostrar_ventana_inicio.connect(
            interfaz.mostrar_ventana_inicio)
        cliente.senal_manejar_mensaje.connect(
            interfaz.manejar_mensaje)
        
        # Señales ventana de inicio
        interfaz.ventana_inicio.senal_enviar_login.connect(
            cliente.enviar)

        # Senales ventana espera
        interfaz.senal_abrir_ventana_espera.connect(
            cliente.enviar)
        interfaz.ventana_cuenta.senla_enviar_volver.connect(
            cliente.enviar)
        interfaz.ventana_cuenta.senal_preparar_juego.connect(
            cliente.enviar)

        # Senales ventana juego
        interfaz.ventana_juego.senal_tiempo_agotado.connect(
            cliente.enviar)
        interfaz.ventana_juego.senal_seleccionar_carta.connect(
            cliente.enviar)

        # ventana final
        interfaz.ventana_final.senal_voler_inicio.connect(
            interfaz.cerrar_final)

        # Senales interfaz
        interfaz.senal_login_rechazado.connect(
            interfaz.ventana_inicio.mostrar_error)
        
        # Chat
        interfaz.ventana_chat.senal_enviar_chat.connect(
            cliente.enviar)

        sys.exit(app.exec_())

    except ConnectionError as e:
        print("Ocurrió un error.", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente...")
        cliente.salir()
        sys.exit()
