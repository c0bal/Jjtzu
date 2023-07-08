# Tarea 3: DCCard-Jitsu 🐧🥋


**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<Descripción El juego funciona y me base en la estructura y codigo de la af3 por lo que puede haber alto porcentaje de similitud con otros. Sin embargo, todo lo demas es propio y funciona bastante acorde con todo el enunciado. Puede que existan bugs en la tarea que no encontre. IMPORTANTE: a veces en una carta el juego tira error y se cae, no pude encontrar cual pero la mayoria de las veces funciona el codigo. Se puede cerrar el servidor con ctr+c por si es necesario. (El chat se puede cerrar cuando quieras)

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores
#### Networking: 26 pts (19%)
##### ✅ Protocolo	
##### ✅ Correcto uso de sockets		
##### ✅ Conexión	
##### ✅ Manejo de Clientes	
##### ✅ Desconexión Repentina
#### Arquitectura Cliente - Servidor: 31 pts (23%)			
##### ✅ Roles			
##### ✅ Consistencia		
##### ✅ Logs
#### Manejo de Bytes: 27 pts (20%)
##### ✅ Codificación			
##### ✅ Decodificación			
##### ✅ Encriptación		
##### ✅ Desencriptación	
##### ✅ Integración
#### Interfaz Gráfica: 27 pts (20%)	
##### ✅ Ventana inicio		
##### ✅ Sala de Espera			
##### ✅ Ventana de juego							
##### ✅ Ventana final
#### Reglas de DCCard-Jitsu: 17 pts (13%)
##### ✅ Inicio del juego			
##### ✅ Ronda				
##### ✅ Termino del juego
#### Archivos: 8 pts (6%)
##### ✅ Parámetros (JSON)		
##### ✅ Cartas.py	
##### ✅ Cripto.py
#### Bonus: 8 décimas máximo
##### ❌ Cheatcodes	
##### ❌ Bienestar	
##### ✅ Chat

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py``` del servidor y se debe correr en terminales el main.py de los clientes


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. Todo lo que tenga que ver con Pyqt5
2. libreria os.path modulo join

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. Todo lo que tenga que ver con ventanas las cuales son controladas desde interfaz.py y los .py entregados como cartas.py y cripto.py
## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

Que el usuario no intente buggear el juego.
