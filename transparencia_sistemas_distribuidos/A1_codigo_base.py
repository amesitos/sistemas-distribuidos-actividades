class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.archivos = {}
    
    def almacenar_archivo(self, nombre_archivo, contenido):
        self.archivos[nombre_archivo] = contenido
    
    def obtener_archivo(self, nombre_archivo):
        if nombre_archivo in self.archivos:
            return self.archivos[nombre_archivo]
        else:
            return None

def buscar_archivo_en_todos_los_nodos(nodos, archivo_a_buscar):
    print(f"\n Buscando '{archivo_a_buscar}'...")
    
    for i, nodo in enumerate(nodos):
        print(f"Paso {i+1}: Preguntando a {nodo.nombre}...")
        contenido = nodo.obtener_archivo(archivo_a_buscar)
        
        if contenido is not None:
            print(f"✓ Encontrado en {nodo.nombre}")
            return contenido
        else:
            print(f"✗ {nodo.nombre} no tiene el archivo")
    
    print("Archivo no encontrado en ningún nodo")
    return None

# Crear sistema distribuido
nodo1 = Nodo("Servidor_1")
nodo2 = Nodo("Servidor_2")
nodo3 = Nodo("Servidor_3")

# SIN TRANSPARENCIA: Cada nodo almacena sus archivos de forma independiente
nodo1.almacenar_archivo("datos.txt", "Contenido secreto")
nodo2.almacenar_archivo("foto.jpg", "datos_imagen")
nodo3.almacenar_archivo("video.mp4", "datos_video")

nodos_sistema = [nodo1, nodo2, nodo3]

# Pruebas
# CON TRANSPARENCIA: El usuario no sabe dónde está cada archivo, solo pide por su nombre
resultado = buscar_archivo_en_todos_los_nodos(nodos_sistema, "foto.jpg")
resultado = buscar_archivo_en_todos_los_nodos(nodos_sistema, "no_existe.txt")