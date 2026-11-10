# APE 02 – Cliente-servidor con archivos como canal de comunicación

| | |
|---|---|
| **Asignatura** | Sistemas Distribuidos – 6to ciclo |
| **Docente** | José O. Guamán Q. |
| **Integrante** | Tayron Morales |
| **Fechas** | 06 y 09 de octubre de 2026 |
| **Lenguaje** | Python 3 (solo librería estándar, sin dependencias) |

## Objetivo

Entender la arquitectura de un sistema distribuido desarrollando **cliente y servidor por separado**, de modo que solo se comuniquen mediante archivos de texto compartidos. Así se evidencia el **desacoplamiento** y la **comunicación indirecta por medio compartido**.

## Estructura

```
APE_02/
├── Practica_02.pdf              # Reporte técnico
└── Ape2/
    ├── servidor/servidor.py     # Servicio que procesa mensajes
    ├── cliente/cliente.py       # Programa interactivo del usuario
    └── canal_comunicacion/      # Carpeta compartida, fuera de ambos proyectos
        ├── entrada_servidor.txt # El cliente escribe aquí
        └── salida_servidor.txt  # El servidor responde aquí
```

La carpeta `canal_comunicacion/` está fuera de `servidor/` y `cliente/`, como pedía la guía.

## Cómo ejecutarlo

Requisito: Python 3.8 o superior. Se necesitan **dos terminales** abiertas en `Ape2/`.

**Terminal 1 – servidor (iniciarlo primero):**

```bash
python3 servidor/servidor.py
# Servidor activo. Presiona Ctrl+C para detenerlo.
```

**Terminal 2 – cliente:**

```bash
python3 cliente/cliente.py
# Cliente activo. Presiona Ctrl+C para salir.
Mensaje: hola mundo
Respuesta: HOLA MUNDO
```

Escribe varios mensajes (la guía pide al menos 3). El servidor imprime `Mensaje procesado: ...` por cada uno. Para ver el canal en vivo, abre una tercera terminal:

```bash
watch -n 0.5 "head canal_comunicacion/*.txt"
```

## Cómo funciona el código

### `servidor.py`

1. Calcula la ruta de la carpeta `canal_comunicacion` relativa a su propio archivo y crea los dos `.txt` si no existen (`touch`).
2. Entra en un bucle infinito que **cada 0.5 s** compara la fecha de modificación (`st_mtime_ns`) de `entrada_servidor.txt` con la última que vio.
3. Si cambió, lee el contenido. Si **no está vacío**, lo procesa con `procesar_mensaje()` (convierte a **mayúsculas**) y escribe el resultado en `salida_servidor.txt`.
4. Como solo reacciona cuando cambia la fecha de modificación, **no reprocesa el mismo mensaje**. Los archivos vacíos se ignoran.
5. `Ctrl+C` lo detiene de forma ordenada.

### `cliente.py`

1. Pide un mensaje por teclado y rechaza los vacíos.
2. Vacía `salida_servidor.txt` y escribe el mensaje en `entrada_servidor.txt`.
3. Espera la respuesta consultando `salida_servidor.txt` cada 0.5 s (simula latencia), con un **tiempo máximo de 15 s**.
4. Si llega una respuesta, la muestra. Si no, lanza `TimeoutError` y muestra *"No se recibió respuesta del servidor"*.
5. El cliente **no conoce la lógica del servidor**: solo sabe qué archivo escribir y cuál leer.

### Flujo

```
cliente.py ──escribe──▶ entrada_servidor.txt ──lee (polling 0.5 s)──▶ servidor.py
cliente.py ◀──lee────── salida_servidor.txt  ◀──escribe (MAYÚSCULAS)── servidor.py
```

## Preguntas de control (ideas principales)

- **Desacoplamiento:** cada componente se desarrolla y ejecuta sin conocer al otro; solo comparten el formato del canal.
- **Si el servidor no está corriendo:** el cliente escribe el mensaje pero nadie responde; tras 15 s recibe el timeout.
- **Varios clientes a la vez:** todos escribirían en el mismo archivo y se sobrescribirían los mensajes y las respuestas (condición de carrera).
- **Limitaciones frente a un modelo real:** no hay tiempo real (polling), no hay control de concurrencia ni identificación de cliente, y depende del sistema de archivos.
- **Cómo mejorar:** usar bloqueo de archivos, un archivo por cliente con un ID, o sustituir el medio por colas o sockets.

## Observaciones

- La carpeta `__pycache__/` incluida en el repositorio puede eliminarse; se genera sola.
- Los archivos `.txt` del canal quedaron con el último mensaje de prueba (`probando como va` → `PROBANDO COMO VA`).
