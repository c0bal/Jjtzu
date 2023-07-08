"""
Módulo principal del servidor
"""
import sys
from servidor import Servidor
from utils import data_json
import socket

if __name__ == "__main__":
    HOST = socket.gethostname()
    PORT = data_json("PORT")
    servidor = Servidor(HOST, PORT)

    try:
        while True:
            input("[Presione Ctrl+C para cerrar servidor]\n\
----------------------------------\n\
| Cliente_id | Evento | Detalles |\n")

    except KeyboardInterrupt:
        print("\n\n")
        print("Cerrando servidor...".center(80, " "))
        print("".center(82, "-"))
        print("".center(82, "-") + "\n")
        servidor.socket_servidor.close()
        sys.exit()
