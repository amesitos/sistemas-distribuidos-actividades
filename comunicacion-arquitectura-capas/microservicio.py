import socket
import json

# =====================================================================
# MICROSERVICIO INDEPENDIENTE DE NOTIFICACIONES
# =====================================================================

class MicroservicioNotificaciones:
    """Microservicio que corre en su propio proceso y puerto"""
    
    def __init__(self):
        self._correos_enviados = []
        
    def enviar_correo_confirmacion(self, email, datos_pedido):
        self._correos_enviados.append({"email": email, "datos": datos_pedido})
        mensaje = f"Correo enviado a {email}:\nTu pedido ha sido confirmado.\nDetalles: {datos_pedido}"
        return {"status": "enviado", "mensaje": mensaje}


def iniciar_microservicio():
    """Inicia el microservicio en su propio puerto"""
    servicio_notificaciones = MicroservicioNotificaciones()
    
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    HOST = 'localhost'
    PORT = 5001  # Puerto diferente al servidor principal
    servidor_socket.bind((HOST, PORT))
    
    servidor_socket.listen(1)
    print(f"[MICROSERVICIO NOTIFICACIONES] Escuchando en {HOST}:{PORT}...")
    
    while True:
        cliente_socket, direccion_cliente = servidor_socket.accept()
        print(f"[MICROSERVICIO] Conexión recibida desde {direccion_cliente}")
        
        try:
            datos = cliente_socket.recv(4096)
            peticion = json.loads(datos.decode('utf-8'))
            
            print(f"[MICROSERVICIO] Petición recibida: {peticion}")
            
            # Procesar la petición de notificación
            email = peticion.get("email")
            datos_pedido = peticion.get("datos_pedido")
            
            respuesta = servicio_notificaciones.enviar_correo_confirmacion(email, datos_pedido)
            
            respuesta_json = json.dumps(respuesta)
            cliente_socket.sendall(respuesta_json.encode('utf-8'))
            print(f"[MICROSERVICIO] Respuesta enviada: {respuesta}\n")
            
        except Exception as e:
            print(f"[MICROSERVICIO] Error: {e}")
            error = {"error": str(e)}
            cliente_socket.sendall(json.dumps(error).encode('utf-8'))
            
        finally:
            cliente_socket.close()


if __name__ == "__main__":
    iniciar_microservicio()

