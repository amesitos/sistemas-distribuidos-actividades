import socket
import json

# =====================================================================
# CLIENTE CON SOCKET - Se conecta al servidor por red
# =====================================================================

def enviar_peticion(servicio, accion, parametros=None):
    """Envía una petición al servidor y devuelve la respuesta"""
    
    # Crear socket cliente
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectar al servidor
    HOST = 'localhost'
    PORT = 5000
    cliente_socket.connect((HOST, PORT))
    
    # Preparar petición en formato JSON
    peticion = {
        "servicio": servicio,
        "accion": accion,
        "parametros": parametros or {}
    }
    
    # Enviar petición
    peticion_json = json.dumps(peticion)
    cliente_socket.sendall(peticion_json.encode('utf-8'))
    
    # Recibir respuesta
    datos = cliente_socket.recv(4096)
    respuesta = json.loads(datos.decode('utf-8'))
    
    # Cerrar conexión
    cliente_socket.close()
    
    return respuesta


# =====================================================================
# APLICACIÓN CLIENTE (FRONTEND SIMULADO)
# =====================================================================

if __name__ == "__main__":
    
    print("--- DEMOSTRACIÓN 1: INTERFAZ ESPECÍFICA (Aproximación a Objeto Remoto) ---")
    
    # El cliente llama al servidor por red usando sockets
    libro = enviar_peticion("ebooks", "obtener_detalles_libro", {"libro_id": "1"})
    print(f"[Cliente] Datos del libro expuesto: {libro}")
    
    pedido = enviar_peticion("ebooks", "registrar_orden_compra", {"libro_id": "1", "cantidad": 2})
    print(f"[Cliente] Resultado del pedido específico: {pedido}\n")


    print("--- DEMOSTRACIÓN 2: INTERFAZ UNIFORME (Estilo REST) ---")
    
    # El cliente interactúa mapeando todo a Recursos (URLs) y Verbos (GET/POST)
    libro_rest = enviar_peticion("rest", None, {"metodo": "GET", "url": "/libros/1", "datos": None})
    print(f"[Cliente REST] Recurso obtenido: {libro_rest}")
    
    nuevo_pedido = enviar_peticion("rest", None, {
        "metodo": "POST",
        "url": "/pedidos",
        "datos": {"libro_id": "1", "cantidad": 2}
    })
    print(f"[Cliente REST] Resultado POST: {nuevo_pedido}")
   
    ## FLUJO PRINCIPAL PARA SIMULAR NOTIFICACIÓN
    
    if "url_recurso" in nuevo_pedido:
        print("\n--- NOTIFICACIÓN POR CORREO ---")
        resultado_correo = enviar_peticion("notificaciones", None, {
            "email": "amesitos123@gmail.com",
            "datos_pedido": nuevo_pedido
        })
        print(f"{resultado_correo['mensaje']}")
    
    print(f"\n--- PETICIÓN PUT PARA MODIFICAR ESTADO DEL PEDIDO ---")
    
    url_pedido = nuevo_pedido.get("url_recurso")
    
    modificar_estado = enviar_peticion("rest", None, {
        "metodo": "PUT",
        "url": url_pedido,
        "datos": {"estado": "pagado"}
    })
    print(f"[Cliente REST] Resultado PUT: {modificar_estado}")
    
    print(f"\n--- PETICIÓN DELETE PARA ELIMINAR LIBRO ---")
    
    eliminar_libro = enviar_peticion("rest", None, {
        "metodo": "DELETE",
        "url": "/libros/2",
        "datos": None
    })
    print(f"[Cliente REST] Resultado DELETE: {eliminar_libro}")
    
    print(f"\n--- PETICIÓN GET PARA SOLICITAR LIBRO ELIMINADO ---")
       
    libro_borrado = enviar_peticion("rest", None, {
        "metodo": "GET",
        "url": "/libros/2",
        "datos": None
    })
    print(f"[Cliente REST] Resultado GET: ID 2 - {libro_borrado}")

    print(f"\n--- PETICIÓN GET PARA SOLICITAR LIBRO INEXISTENTE ---")
    
    libro_999 = enviar_peticion("rest", None, {
        "metodo": "GET",
        "url": "/libros/999",
        "datos": None
    })
    print(f"[Cliente REST] Resultado GET: ID 999 - {libro_999}")