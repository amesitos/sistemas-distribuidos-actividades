import datetime

class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.archivos = {}
        self.logs = []  # Registro de actividades
    
    def registrar_log(self, operacion, archivo, detalle):
        """Registra una operación con timestamp"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        entrada = f"[{timestamp}] {operacion}: {archivo} -> {detalle}"
        self.logs.append(entrada)
    

    # COMPLETADO
    def almacenar_archivo(self, nombre_archivo, contenido):
        """Almacena un archivo y registra la operación"""
        self.archivos[nombre_archivo] = contenido
        self.registrar_log("ALMACENAR", nombre_archivo, "Guardado exitosamente")
        return True
    
    def obtener_archivo(self, nombre_archivo):
        """Obtiene un archivo si existe, registra la operación"""
        if nombre_archivo in self.archivos:
            contenido = self.archivos[nombre_archivo]
            self.registrar_log("OBTENER", nombre_archivo, "Archivo encontrado")
            return contenido
        else:
            self.registrar_log("OBTENER", nombre_archivo, "Archivo no encontrado")
            return None
        
    def ver_logs(self):
        """Muestra todos los registros del nodo"""
        if not self.logs:
            return f"{self.nombre}: Sin actividades registradas"
        return f"\n--- Logs de {self.nombre} ---\n" + "\n".join(self.logs)

# COMPLETADO
def buscar_archivo_en_todos_los_nodos(nodos, archivo_a_buscar):
    """
    Busca un archivo en todos los nodos del sistema.
    Retorna el contenido y el nodo donde se encontró.
    """
    print(f"\n Buscando '{archivo_a_buscar}' en el sistema...")
    
    # Completado
    for nodo in nodos:
        contenido = nodo.obtener_archivo(archivo_a_buscar)
        
        if contenido is not None:
            print(f"Encontrado en {nodo.nombre}")
            return contenido, nodo.nombre
    
    print(f"Archivo {archivo_a_buscar} no se encontró en ningún nodo")
    return None, None


def mostrar_menu():
    print("\n" + "="*50)
    print("SISTEMA DE ARCHIVOS DISTRIBUIDO")
    print("="*50)
    print("1. Guardar un archivo")
    print("2. Recuperar un archivo")
    print("3. Ver logs de un nodo")
    print("4. Salir")
    print("="*50)


# ========== PROGRAMA PRINCIPAL ==========
if __name__ == "__main__":
    # Crear los nodos del sistema
    nodo1 = Nodo("Servidor_A")
    nodo2 = Nodo("Servidor_B")
    nodo3 = Nodo("Servidor_C")
    
    nodos_sistema = [nodo1, nodo2, nodo3]
    
    print("=== SISTEMA DISTRIBUIDO INICIADO ===")
    print(f"Nodos disponibles: {[n.nombre for n in nodos_sistema]}")
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ")
        
        # COMPLETAR: Guardar archivo
        if opcion == "1":
            print("\n--- GUARDAR ARCHIVO ---")
            nombre_archivo = input("Ingrese el nombre del archivo: ")
            contenido = input("Ingrese el contenido: ")
            
            print("\nNodos disponibles:")
            for i, nodo in enumerate(nodos_sistema):
                print(f"{i}. {nodo.nombre}")
            
            indice = int(input("Seleccione el nodo destino (0, 1, 2): "))
            
            if 0 <= indice < len(nodos_sistema):
                nodos_sistema[indice].almacenar_archivo(nombre_archivo, contenido)
                print(f"\nArchivo guardado en {nodos_sistema[indice].nombre}")
            else:
                print("Índice no válido")
            
        
        elif opcion == "2":
            # COMPLETAR: Recuperar archivo (transparencia de ubicación)
            print("\n--- RECUPERAR ARCHIVO ---")
            nombre_archivo = input("Ingrese el nombre del archivo: ")
            
            contenido, nodo_encontrado = buscar_archivo_en_todos_los_nodos(nodos_sistema, nombre_archivo)
            if contenido is not None:
                print(f"Archivo encontrado exitosamente.\nNombre:{nombre_archivo} \nContenido: {contenido}")
            else:
                print(f"Archivo '{nombre_archivo}' no encontrado.")
            
        elif opcion == "3":
            # COMPLETAR: Ver logs
            print("\n--- VER LOGS ---")
            nodos = [nodo1, nodo2, nodo3]  
            nombre_nodo = input("Ingrese el nombre del nodo (A, B o C): ")
            if nombre_nodo in ["A", "B", "C"]:
                nodo_index = ord(nombre_nodo) - ord("A")
                print(nodos[nodo_index].ver_logs())
            else:
                print("Nodo no válido") 
            
        elif opcion == "4":
            print("\nSaliendo del sistema...")
            print("Gracias por usar el sistema de archivos distribuido")
            break
        
        else:
            print("\n Opción no válida. Intente nuevamente.")
    
    # COMPLETAR: Al finalizar, mostrar logs de TODOS los nodos automáticamente
    print("\n" + "="*50)
    print("RESUMEN FINAL DE ACTIVIDADES")
    print("="*50)
    
    # Escriba aquí el código para mostrar todos los logs:
    for nodo in nodos_sistema:
        print(nodo.ver_logs())
    
    