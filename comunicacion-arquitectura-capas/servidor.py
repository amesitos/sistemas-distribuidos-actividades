import uuid
import socket
import json

# =====================================================================
# SIMULACIÓN DE MICROSERVICIOS (BACKEND) CON SOCKETS
# =====================================================================

class ServicioEbooks:
    """Simula un microservicio con una Interfaz Específica (Estilo Objeto Remoto)"""
    def __init__(self):
        # Base de datos simulada en el servidor (Objeto con estado)
        self._inventario = {
            "1": {"titulo": "Sistemas Distribuidos 101", "precio": 25.0},
            "2": {"titulo": "El mito del mes hombre", "precio": 30.0}
        }
        self._pedidos = {}

    # --- INTERFAZ ESPECÍFICA ---
    def detalles_libro(self, libro_id):
        return self._inventario.get(libro_id, None)

    def registrar_orden_compra(self, libro_id, cantidad):
        if libro_id in self._inventario:
            id_pedido = str(uuid.uuid4())[:8]
            total = self._inventario[libro_id]["precio"] * cantidad
            self._pedidos[id_pedido] = {"libro_id": libro_id, "cantidad": cantidad, "total": total}
            return {"id_pedido": id_pedido, "total": total, "estado": "creado"}
        return {"error": "Libro no encontrado"}


class ServicioRestEbooks:
    """Simula un microservicio accesible mediante una Interfaz Uniforme (Estilo REST)"""
    def __init__(self):
        self._recursos = {
            "/libros/1": {"titulo": "Sistemas Distribuidos 101", "precio": 25.0},
            "/libros/2": {"titulo": "El mito del mes hombre", "precio": 30.0},
            "/pedidos": {}
        }

    # --- INTERFAZ UNIFORME (Solo 4 operaciones fijas) ---
    def peticion_http(self, metodo, url, parametros=None):
        metodo = metodo.upper()
        
        if metodo == "GET":
            # Obtener el estado de un recurso
            return self._recursos.get(url, {"error": "404 Not Found"})
            
        elif metodo == "POST":
            # Crear un nuevo recurso
            if url == "/pedidos":
                id_pedido = str(uuid.uuid4())[:8]
                nueva_url = f"/pedidos/{id_pedido}"
                self._recursos[nueva_url] = {
                    "libro_id": parametros.get("libro_id"),
                    "cantidad": parametros.get("cantidad"),
                    "estado": "creado"
                }
                return {"status": "201 Created", "url_recurso": nueva_url}
                
        elif metodo == "PUT":
            # Modificar un recurso existente (Transferir nuevo estado)
            if url in self._recursos:
                self._recursos[url].update(parametros)
                return {"status": "200 OK", "recurso": self._recursos[url]}
                
        elif metodo == "DELETE":
            # Eliminar un recurso
            if url in self._recursos:
                del self._recursos[url]
                return {"status": "200 OK", "mensaje": "Recurso eliminado"}
                
        return {"error": "405 Method Not Allowed o Recurso Inválido"}


# =====================================================================
# SERVIDOR CON SOCKET 
# =====================================================================

def llamar_microservicio_notificaciones(email, datos_pedido, reintentos=3):
    """
    Se conecta al microservicio de notificaciones independiente
    Implementa TOLERANCIA A FALLOS:
    - Timeout de 2 segundos para evitar bloqueos
    - Reintentos automáticos (3 intentos por defecto)
    - Respuesta degradada: el sistema continúa sin notificaciones
    """
    HOST = 'localhost'
    PORT = 5001
    
    for intento in range(reintentos):
        try:
            cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # TIMEOUT: Evita que el servidor se quede bloqueado esperando
            cliente_socket.settimeout(2.0)  # 2 segundos máximo
            
            # Conectar al microservicio en su puerto
            cliente_socket.connect((HOST, PORT))
            
            peticion = {
                "email": email,
                "datos_pedido": datos_pedido
            }
            
            peticion_json = json.dumps(peticion)
            cliente_socket.sendall(peticion_json.encode('utf-8'))
            
            datos = cliente_socket.recv(4096)
            respuesta = json.loads(datos.decode('utf-8'))
            
            cliente_socket.close()
            
            return respuesta
            
        except socket.timeout:
            print(f"[SERVIDOR] ⚠️ Timeout en microservicio de notificaciones (intento {intento + 1}/{reintentos})")
            if intento < reintentos - 1:
                continue
                
        except ConnectionRefusedError:
            print(f"[SERVIDOR] ⚠️ Microservicio de notificaciones NO disponible (intento {intento + 1}/{reintentos})")
            if intento < reintentos - 1:
                continue
                
        except Exception as e:
            print(f"[SERVIDOR] ⚠️ Error en microservicio: {str(e)} (intento {intento + 1}/{reintentos})")
            if intento < reintentos - 1:
                continue
        finally:
            try:
                cliente_socket.close()
            except:
                pass
    
    # RESPUESTA DEGRADADA: El sistema continúa funcionando
    print("[SERVIDOR] ℹ️ Continuando sin notificaciones (modo degradado)")
    return {
        "status": "degradado",
        "mensaje": "Pedido procesado correctamente, pero el servicio de notificaciones está temporalmente no disponible. La notificación se enviará más tarde.",
        "advertencia": "Microservicio de notificaciones no responde"
    }


def iniciar_servidor():

    # instancias de los servicios (solo ebooks y rest, notificaciones es independiente)
    srv_especifico = ServicioEbooks()
    srv_rest = ServicioRestEbooks()
    
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    HOST = 'localhost'
    PORT = 5000
    servidor_socket.bind((HOST, PORT))
    
    servidor_socket.listen(1) # una en cola
    print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}...")
    
    while True:
        cliente_socket, direccion_cliente = servidor_socket.accept()
        print(f"[SERVIDOR] Cliente conectado desde {direccion_cliente}")
        
        try:
            datos = cliente_socket.recv(4096)
            peticion = json.loads(datos.decode('utf-8'))
            
            print(f"[SERVIDOR] Petición recibida: {peticion}")
            
            servicio = peticion.get("servicio")
            accion = peticion.get("accion")
            parametros = peticion.get("parametros", {})
            
            respuesta = {}
            if servicio == "ebooks":
                if accion == "detalles_libro":
                    respuesta = srv_especifico.detalles_libro(parametros.get("libro_id"))
                elif accion == "registrar_orden_compra":
                    respuesta = srv_especifico.registrar_orden_compra(
                        parametros.get("libro_id"),
                        parametros.get("cantidad")
                    )
                    
            elif servicio == "rest":
                respuesta = srv_rest.peticion_http(
                    parametros.get("metodo"),
                    parametros.get("url"),
                    parametros.get("datos")
                )
                
            elif servicio == "notificaciones":
                # TOLERANCIA A FALLOS: Intenta conectar al microservicio
                # Si falla, el sistema continúa funcionando (modo degradado)
                # No afecta al resto de operaciones del servidor
                respuesta = llamar_microservicio_notificaciones(
                    parametros.get("email"),
                    parametros.get("datos_pedido")
                )
            
            respuesta_json = json.dumps(respuesta)
            cliente_socket.sendall(respuesta_json.encode('utf-8'))
            print(f"[SERVIDOR] Respuesta enviada: {respuesta}\n")
            
        except Exception as e:
            print(f"[SERVIDOR] Error: {e}")
            error = {"error": str(e)}
            cliente_socket.sendall(json.dumps(error).encode('utf-8'))
            
        finally:
            # Cerrar conexión
            cliente_socket.close()


if __name__ == "__main__":
    iniciar_servidor()
