"""
Modulo contiene la clase Logica del servidor
"""
from cartas import get_penguins

class Logica:
    def __init__(self, parent):
        # Esto permite ejecutar funciones de la clase Servidor
        self.parent = parent
        self.usuarios = {}
        # cada id de cliente contiene su baraja en otro diccionario
        self.barajas = {}
        self.selecciones = {}
        self.mazos_triunfo = {}
        self.revisando_ganador = False
        self.en_juego = False
        self.en_espera = False

    def barajar(self):
        for i in self.usuarios:
            self.barajas[i] = get_penguins()

    def validar_login(self, nombre: str, id_cliente):
        datos_invalidos = []
        #Verifico restricciones
        for i in self.usuarios.values():
            if nombre.lower() == str(i).lower():
                datos_invalidos.append("Nombre ocupado")      
        if len(self.usuarios) == 2:
            datos_invalidos.append("Sala llena")
        if len(nombre) == 0 or len(nombre) >= 10:
            datos_invalidos.append("Largo no permitido")
        if not nombre.isalpha():
            datos_invalidos.append("Debe ser alfanumerico")
        #Notifico Correcto
        if len(datos_invalidos) == 0:
            self.parent.log(id_cliente, "Ingresar sala espera", f"Sala con cupo")
            self.parent.log(id_cliente, "Ingresa Nombre", f"nombre = {nombre} -> aceptado")
            self.usuarios[id_cliente] = nombre 
            if len(self.usuarios) == 2:
                self.barajar()
                self.en_espera = True
                for i in self.usuarios:
                    if i != id_cliente:
                        id_1 = str(i)
                        n1 = self.usuarios[i]
                return {"comando": "respuesta_sala_completada",
                        "p1": n1,
                        "id_1": id_1,
                        "p2": nombre,
                        "id_2": id_cliente}
            return {
                "comando": "respuesta_validacion_login",
                "estado": "aceptado",
                "nombre": nombre}
        #Notifico Incorrecto
        if len(self.usuarios) == 2:
            self.parent.log(id_cliente, "Ingresar sala espera", f"Sala llena")
        if len(datos_invalidos) == 1:
            if datos_invalidos[0] == "Sala llena":
                self.parent.log(id_cliente, "Ingresa Nombre", 
                                f"nombre = {nombre} -> correcto pero sala llena")
        else:
            self.parent.log(id_cliente, "Ingresa Nombre", f"nombre = {nombre} -> rechazado")
        return {
            "comando": "respuesta_validacion_login",
            "estado": "rechazado",
            "error": datos_invalidos}

    def pedir_mazo(self, id_cliente):
        self.en_espera = False
        self.en_juego = True
        jugador = self.usuarios[id_cliente]
        for i in self.usuarios:
            if i != id_cliente:
                rival = self.usuarios[i]
                rival_id = i

        self.parent.log("-", "Comienzo partida", f"{jugador} vs {rival}")

        diccionario = {"comando": "respuesta_mazo",
                        "nombre": jugador,
                        "rival": rival,
                        "id_1": id_cliente,
                        "mazo_1": self.barajas[id_cliente],
                        "mazo_2": self.barajas[rival_id]}
        return diccionario

    def procesar_mensaje(self, mensaje, id_cliente):
        try:
            comando = mensaje["comando"]
        except KeyError:
            return {}
        if comando == "validar_login":
            respuesta = self.validar_login(
                mensaje["nombre usuario"], id_cliente)
        elif comando == "volver_inicio":
            self.eliminar_nombre(id_cliente)
            respuesta = {"comando": "respuesta_volver_inicio"}
        elif comando == "pedir_mazo":
            respuesta = self.pedir_mazo(id_cliente)
        elif comando == "seleccionar_carta":
            self.seleccionar_carta(id_cliente, mensaje["id"])
            respuesta = False
        elif comando == "no_time":
            self.parent.log(id_cliente, "Tiempo Ronda finalizado", f"se lanza carta automatica")
            respuesta = False
        elif comando == "chat":
            for i in self.usuarios:
                if str(i) != str(id_cliente):
                    self.parent.notificar_otros_usuarios(i, mensaje)
            respuesta = False
        return respuesta

    def seleccionar_carta(self, id_cliente, id_carta):
        baraja = self.barajas[id_cliente]
        self.selecciones[id_cliente] = [baraja[str(id_carta)], id_carta]
        tipo = baraja[str(id_carta)]["elemento"]
        self.parent.log(id_cliente, "Carta Lanzada", \
                        f"{self.usuarios[id_cliente]} lanza carta tipo {tipo}")
        if len(self.selecciones) == 2:
            for u in self.usuarios:
                self.parent.notificar_otros_usuarios(u, {"comando": "fin_timer"})

            if self.revisando_ganador == False:
                self.revisando_ganador = True
                resultado = self.ganador_ronda()
                clientes = []
                for i in self.selecciones:
                    clientes.append(i)
                
                if resultado == "1":
                    self.parent.log("-", "Ronda Finalizada", \
                                    f"Ganador: {self.usuarios[clientes[0]]}")
                    if clientes[0] in self.mazos_triunfo:
                        self.mazos_triunfo[clientes[0]].append(self.selecciones[clientes[0]][1])
                    else:
                        self.mazos_triunfo[clientes[0]] = [self.selecciones[clientes[0]][1]]
                
                elif resultado == "2":
                    self.parent.log("-", "Ronda Finalizada", \
                                    f"Ganador: {self.usuarios[clientes[1]]}")
                    if clientes[1] in self.mazos_triunfo:
                        self.mazos_triunfo[clientes[1]].append(self.selecciones[clientes[1]][1])
                    else:
                        self.mazos_triunfo[clientes[1]] = [self.selecciones[clientes[1]][1]]

                verificador = self.check_final()

                if verificador == False:

                    if resultado == "0":
                        self.parent.log("-", "Ronda Finalizada", f"Empate")
                        # Cliente 0
                        dic = {"comando": "empate",
                            "usuario": str(self.selecciones[clientes[0]][1]),
                            "rival": str(id_carta)}
                        self.parent.notificar_otros_usuarios(clientes[0], dic)
                        # Cliente 1
                        dic = {"comando": "empate",
                            "usuario": str(id_carta),
                            "rival": str(self.selecciones[clientes[0]][1])}                    
                        self.parent.notificar_otros_usuarios(clientes[1], dic)
                    
                    elif resultado == "1": # Gana Cliente 0

                        dic = {"comando": "gano",
                            "usuario": str(self.selecciones[clientes[0]][1]),
                            "rival": str(id_carta)}
                        self.parent.notificar_otros_usuarios(clientes[0], dic)
                        dic = {"comando": "pierdo",
                            "usuario": str(id_carta),
                            "rival": str(self.selecciones[clientes[0]][1])}                    
                        self.parent.notificar_otros_usuarios(clientes[1], dic)
                    
                    elif resultado == "2": # Gana Cliente 1

                        dic = {"comando": "pierdo",
                            "usuario": str(self.selecciones[clientes[0]][1]),
                            "rival": str(id_carta)}
                        self.parent.notificar_otros_usuarios(clientes[0], dic)
                        dic = {"comando": "gano",
                            "usuario": str(id_carta),
                            "rival": str(self.selecciones[clientes[0]][1])}                    
                        self.parent.notificar_otros_usuarios(clientes[1], dic) 
                self.revisando_ganador = False 
                self.selecciones = {}                                   
    
    def check_final(self):
       
        for i in self.usuarios: 
            for indice in self.mazos_triunfo:
                if indice == i:
                    mazo_cliente = self.barajas[i]
                    color = {}
                    elementos = {"agua": 0,
                                "nieve": 0,
                                "fuego": 0}

                    lista = self.mazos_triunfo[i]
                    for id_carta in lista:
                        atributos = mazo_cliente[str(id_carta)]
                        color[atributos["color"]] = 0
                        elementos[atributos["elemento"]] += 1
                    
                    if len(color) == 3:
                        verificador = True
                        for e in elementos:
                            if elementos[e] > 2:
                                self.ganador(int(i))
                                return True
                        for e in elementos:
                            if verificador == True:
                                if elementos[e] > 0:
                                    verificador = True
                                else:
                                    verificador = False
                        if verificador == True:
                            self.ganador(int(i))
                            return True
        return False

    def ganador_ronda(self):
        '''
        Retorna 0 -> empate, 1 -> primer key de selecciones y 2 -> segundo key
        '''
        p1 = ""
        p2 = ""
        for i in self.selecciones:
            if p1 == "":
                p1 = self.selecciones[i][0]
            else:
                p2 = self.selecciones[i][0]
        if  p1["elemento"] == p2["elemento"] and  p1["puntos"] == p2["puntos"]:
            return "0"
        else:
            if p1["elemento"] != p2["elemento"]:
                if p1["elemento"] == "fuego" and p2["elemento"] == "nieve":
                    return "1"
                elif p1["elemento"] == "nieve" and p2["elemento"] == "agua":
                    return "1"
                elif p1["elemento"] == "agua" and p2["elemento"] == "fuego":
                    return "1"
                elif p2["elemento"] == "fuego" and p1["elemento"] == "nieve":
                    return "2"
                elif p2["elemento"] == "nieve" and p1["elemento"] == "agua":
                    return "2"
                elif p2["elemento"] == "agua" and p1["elemento"] == "fuego":
                    return "2"
            else:
                if p1["puntos"] > p2["puntos"]:
                    return "1"
                else:
                    return "2"

    def ganador(self, i):
        self.parent.log("-", "Termino Partida", f"Ganador: {self.usuarios[i]}")
        self.parent.notificar_otros_usuarios(i, {"comando": "resultado",
                                                "texto": "FELICIDADES, HAS GANADO"})
        for id in self.usuarios:
            if int(id) != int(i):
                self.parent.notificar_otros_usuarios(int(id), {"comando": "resultado",
                                                        "texto": "MALA SUERTE, HAZ PERDIDO"})
        self.reset()

    def reset(self):
        self.usuarios = {}
        self.barajas = {}
        self.selecciones = {}
        self.mazos_triunfo = {}
        self.revisando_ganador = False
        self.en_juego = False
        self.en_espera = False

    def eliminar_nombre(self, id):
        self.parent.notificar_otros_usuarios(id, {"comando": "cerrar_chat"})
        self.usuarios.pop(id, None)
        for i in self.usuarios:
            if self.en_espera == True:
                self.parent.notificar_otros_usuarios(i, {"comando": "desconexion_rival",
                                                        "restante": self.usuarios[i]})
                self.en_espera = False
            elif self.en_juego == True:
                self.ganador(i)
           