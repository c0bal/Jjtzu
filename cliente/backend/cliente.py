"""
Modulo contiene implementación principal del cliente
"""
from PyQt5.QtCore import pyqtSignal, QObject
import socket
import json
from threading import Thread
from backend.cripto import encriptar, desencriptar

class Cliente(QObject):
    senal_mostrar_ventana_inicio = pyqtSignal()
    senal_manejar_mensaje = pyqtSignal(dict)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False
        self.iniciar_cliente()

    def iniciar_cliente(self):
        """
        Se encarga de iniciar el cliente y conectar el socket
        """
        try:
            self.socket_cliente.connect((self.host, self.port))
            self.conectado = True
            self.comenzar_a_escuchar()
            self.senal_mostrar_ventana_inicio.emit()

        except ConnectionError as e:
            print(f"\n-ERROR: El servidor no está inicializado. {e}-")
        except ConnectionRefusedError as e:
            print(f"\n-ERROR: No se pudo conectar al servidor.{e}-")

    def comenzar_a_escuchar(self):
        thread = Thread(target=self.escuchar_servidor, daemon=True)
        thread.start()

    def escuchar_servidor(self):
        try:
            while True:
                mensaje = self.recibir()
                if mensaje:
                    self.senal_manejar_mensaje.emit(mensaje)
        except ConnectionError as e:
            print("ERROR: El servidor se ha desconectado.", e)

    def recibir(self):
        largo_mensaje_bytes = self.socket_cliente.recv(4)
        largo_mensaje = int.from_bytes(largo_mensaje_bytes, byteorder="big")
        
        #Recibir mensaje
        bytes_mensaje = bytearray()
        cant_chunks = largo_mensaje // 32
        chunk_sobra = False
        if largo_mensaje % 32 != 0:
            chunk_sobra = True
      
        for _ in range(cant_chunks):
            tamano_chunk_bytes = self.socket_cliente.recv(4)
            bytes_mensaje += self.socket_cliente.recv(32)
        if chunk_sobra:
            tamano_chunk_bytes = self.socket_cliente.recv(4)
            bytes_mensaje += self.socket_cliente.recv(largo_mensaje % 32)
            ceros = self.socket_cliente.recv(32 - (largo_mensaje % 32))

        #Terminar decodificacion
        mensaje = self.decodificar_mensaje(bytes_mensaje)
        return mensaje

    def enviar(self, mensaje):
        """
        Envía un mensaje a un cliente.
        """
        #Codificar mensaje
        bytes_mensaje = self.codificar_mensaje(mensaje)
        #Enviar mensaje
        self.socket_cliente.sendall(bytes_mensaje)

    def codificar_mensaje(self, mensaje):
        try:
            #Encripto
            mensaje_json = json.dumps(mensaje)
            mensaje_bytes = encriptar(bytearray(mensaje_json.encode()))
            #Obtengo el largo
            largo_mensaje_bytes = len(mensaje_bytes).to_bytes(4, byteorder = "big")
            #Codifico
            mensaje_codificado_con_chunk = bytearray()
            numero = 1
            mensaje_codificado_con_chunk += largo_mensaje_bytes
            c = 0
            for _ in range(len(mensaje_bytes) // 32):
                mensaje_codificado_con_chunk += numero.to_bytes(4, byteorder = "little")
                mensaje_codificado_con_chunk += mensaje_bytes[c:c+32]
                numero += 1
                c += 32
            if len(mensaje_bytes) % 32 != 0:
                ceros_byte = b''.zfill(32-(len(mensaje_bytes) % 32))
                mensaje_codificado_con_chunk += numero.to_bytes(4, byteorder = "little")
                mensaje_codificado_con_chunk += mensaje_bytes[c:]
                mensaje_codificado_con_chunk += ceros_byte
            return mensaje_codificado_con_chunk
        except json.JSONDecodeError:
            print("ERROR: NO SE PUEDO CODIFICAR EL MENSAJE")
            return b""

    def decodificar_mensaje(self, mensaje_bytes):
        try:
            mensaje = json.loads(desencriptar(bytearray(mensaje_bytes)).decode())
            return mensaje
        except json.JSONDecodeError:
            print("ERROR: No se pudo decodificar el mensaje")
            return {}