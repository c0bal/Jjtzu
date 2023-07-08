"""
Modulo contiene la implementación principal del servidor
"""
import json
import socket
import threading
from logica import Logica
import threading
from cripto import desencriptar, encriptar

class Servidor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_servidor = None
        self.logica = Logica(self)
        self.id_cliente = 0
        self.command_log("Inicializando servidor...")
        self.sockets = {}
        self.iniciar_servidor()

    def iniciar_servidor(self):
        """
        Crea el socket, lo enlaza y comienza a escuchar
        """
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen()
        self.command_log(f"Servidor escuchando en = {self.host} : {self.port}")
        self.comenzar_a_aceptar()

    def comenzar_a_aceptar(self):
        """
        Crea y comienza el thread encargado de aceptar clientes
        """
        thread = threading.Thread(target=self.aceptar_clientes, daemon=True)
        thread.start()

    def aceptar_clientes(self):
        """
        Es arrancado como thread para de aceptar clientes, este se ejecuta
        siempre que se este conectado y acepta el socket del servidor. Luego
        se crea y comienza a escuchar al cliente. para finalmente aumentar en 1
        el id_cliente.
        """
        try:
            while True:
                
                socket_cliente, address = self.socket_servidor.accept()
                self.sockets[self.id_cliente] = socket_cliente 
                self.log(self.id_cliente, "Conectarse", "conectado")
                thread_cliente = threading.Thread(
                    target = self.escuchar_cliente,
                    args = (self.id_cliente, socket_cliente),
                    daemon = True
                )
                thread_cliente.start()
                self.id_cliente += 1
        except ConnectionError as error:
            self.command_log("Hubo un error con un cliente")
        
    def escuchar_cliente(self, id_cliente, socket_cliente):
        self.log(id_cliente, "Escuchar", "escuchando")
        try:
            while True:
                mensaje = self.recibir_mensaje(socket_cliente)
                respuesta = self.logica.procesar_mensaje(mensaje, id_cliente)
                if respuesta:
                    self.enviar_mensaje(respuesta, socket_cliente)
                    self.notificar_otros_usuarios(id_cliente, respuesta)

        except ConnectionError as error:
            self.eliminar_cliente(id_cliente)

    def notificar_otros_usuarios(self, id_cliente, respuesta):
        if respuesta["comando"] == "respuesta_sala_completada":
            self.enviar_mensaje(respuesta, self.sockets[int(respuesta["id_1"])])
        
        elif respuesta["comando"] == "cerrar_chat":
            self.enviar_mensaje(respuesta, self.sockets[id_cliente])

        elif respuesta["comando"] == "desconexion_rival":
            self.enviar_mensaje(respuesta, self.sockets[id_cliente])
        
        elif respuesta["comando"] == "empate":
            self.enviar_mensaje(respuesta, self.sockets[id_cliente])
        elif respuesta["comando"] == "gano":
            self.enviar_mensaje(respuesta, self.sockets[id_cliente])
        elif respuesta["comando"] == "pierdo":
            self.enviar_mensaje(respuesta, self.sockets[id_cliente])    
        
        elif respuesta["comando"] == "resultado":
            self.enviar_mensaje(respuesta, self.sockets[id_cliente])  

        elif respuesta["comando"] == "fin_timer":
            self.enviar_mensaje(respuesta, self.sockets[id_cliente])  
        
        elif respuesta["comando"] == "chat":
            self.enviar_mensaje(respuesta, self.sockets[id_cliente])

    def recibir_mensaje(self, socket_cliente):
      
        largo_mensaje_bytes = socket_cliente.recv(4)
        largo_mensaje = int.from_bytes(largo_mensaje_bytes, byteorder="big")
        
        #Recibir mensaje
        bytes_mensaje = bytearray()
        cant_chunks = largo_mensaje // 32
        chunk_sobra = False
        if largo_mensaje % 32 != 0:
            chunk_sobra = True
      
        for _ in range(cant_chunks):
            tamano_chunk_bytes = socket_cliente.recv(4)
            bytes_mensaje += socket_cliente.recv(32)
        if chunk_sobra:
            tamano_chunk_bytes = socket_cliente.recv(4)
            bytes_mensaje += socket_cliente.recv(largo_mensaje % 32)
            ceros = socket_cliente.recv(32 - (largo_mensaje % 32))

        #Terminar decodificacion
        mensaje = self.decodificar_mensaje(bytes_mensaje)
        return mensaje

    def eliminar_cliente(self, id_cliente):
        try:
            # Cerramos el socket
            self.log(id_cliente, "Desconectando", "socket eliminado")
            self.sockets[id_cliente].close()
            self.sockets.pop(id_cliente, None)
            self.logica.eliminar_nombre(id_cliente)

        except KeyError as e:
            self.command_log(f"ERROR: {e}")

    def decodificar_mensaje(self, mensaje_bytes):
        try:
            mensaje = json.loads(desencriptar(bytearray(mensaje_bytes)).decode())
            return mensaje
        except json.JSONDecodeError:
            print("ERROR: No se pudo decodificar el mensaje")
            return {}

    def log(self, cliente, evento, detalles):
        print(f"| {cliente} | {evento} | {detalles} |")

    def command_log(self, mensaje: str):
        """
        Imprime un mensaje en consola
        """
        print(mensaje)

    def enviar_mensaje(self, mensaje, socket_cliente):
        #Encripto y codifico
        bytes_mensaje = self.codificar_mensaje(mensaje)
        #Enviar mensaje
        socket_cliente.sendall(bytes_mensaje)

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