# Actividad #5 - Comunicación y Arquitectura de Capas
**Fecha:** 26 de mayo de 2026

## Descripción
Sistema distribuido con arquitectura de capas que implementa comunicación cliente-servidor mediante sockets TCP/IP. Incluye microservicio independiente de notificaciones y demuestra dos estilos de interfaces: específica (objeto remoto) y uniforme (REST).

## Tema
- Comunicación por sockets
- Arquitectura en capas
- Microservicios
- Interfaces específicas vs. uniformes (REST)

## Archivos
- `cliente.py` - Cliente que envía peticiones al servidor
- `servidor.py` - Servidor principal (puerto 5000) con servicios de ebooks
- `microservicio.py` - Microservicio de notificaciones (puerto 5001)

## Ejecución

1. **Iniciar el microservicio de notificaciones:**
```bash
python microservicio.py
```

2. **Iniciar el servidor principal:**
```bash
python servidor.py
```

3. **Ejecutar el cliente (en otra terminal):**
```bash
python cliente.py
```

**Nota:** Los tres componentes deben ejecutarse en orden y en terminales separadas.
