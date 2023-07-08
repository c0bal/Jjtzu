def encriptar(msg : bytearray) -> bytearray:
    a = b''
    b = b''
    c = b''
    for i in range(len(msg)):
        if i % 3 == 0:
            a += msg[i].to_bytes(1, byteorder='big')
        elif i % 3 == 1:
            b += msg[i].to_bytes(1, byteorder='big')
        elif i % 3 == 2:
            c += msg[i].to_bytes(1, byteorder='big')
    
    centrales = b[1:-1]
    suma_centrales = 0
    for i in range(len(centrales)):
        suma_centrales += centrales[i]
    total = a[0] + suma_centrales+c[-1]
    
    if total % 2 == 1:
        n = int(1).to_bytes(1, byteorder='big')
        crypto = n + a + c + b 
    elif total % 2 == 0:
        n = int(0).to_bytes(1, byteorder='big')
        crypto = n + c + a + b  
    return crypto

def desencriptar(msg : bytearray) -> bytearray:
    descrypto = b''
    largo = len(msg) - 1
    crypto = msg[1:]
    largo_a = 0
    largo_b = 0
    largo_c = 0

    for i in range(largo):
        if i % 3 == 0:
            largo_a += 1
        elif i % 3 == 1:
            largo_b += 1
        elif i % 3 == 2:
            largo_c += 1
    if msg[0] == 0:
        c = crypto[0:largo_c]
        a = crypto[largo_c: largo_c + largo_a]
        b = crypto[largo_c + largo_a:]
    elif msg[0] == 1:
        a = crypto[0:largo_a]
        c = crypto[largo_a: largo_c + largo_a]
        b = crypto[largo_c + largo_a:] 

    for i in range(largo_c):
        descrypto += a[i].to_bytes(1, byteorder='big')
        descrypto += b[i].to_bytes(1, byteorder='big')
        descrypto += c[i].to_bytes(1, byteorder='big')

    if largo_b > largo_c:
        descrypto += a[largo_c].to_bytes(1, byteorder='big')
        descrypto += b[largo_c].to_bytes(1, byteorder='big')
    elif largo_a > largo_b:
        descrypto += a[largo_c].to_bytes(1, byteorder='big')
    return descrypto

if __name__ == "__main__":
    #Testear encriptar
    msg_original = bytearray(b'\x05\x08\x03\x02\x04\x03\x05\x09\x05\x09\x01')
    msg_esperado = bytearray(b'\x01\x05\x02\x05\x09\x03\x03\x05\x08\x04\x09\x01')
    msg_encriptado = encriptar(msg_original)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")
    
    # Testear desencriptar
    msg_original = bytearray(b'\x05\x08\x03\x02\x04\x03\x05\x09\x05\x09\x01')
    msg_desencriptado = desencriptar(msg_esperado)
  
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")
