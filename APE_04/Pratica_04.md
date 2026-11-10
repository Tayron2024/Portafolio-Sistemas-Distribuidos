# APE 04 – Asignación de pedidos con IPC, sockets TCP y un agente de IA (Ollama)

| | |
|---|---|
| **Asignatura** | Sistemas Distribuidos – 6to ciclo |
| **Docente** | José O. Guamán Q. |
| **Integrantes** | Tayron Morales, Mateo Rojas, Leonardo Sánchez |
| **Fechas** | 13 y 16 de octubre de 2026 |
| **Lenguaje** | Python 3 (dependencia externa: `requests`) |
| **Repositorio base del docente** | <https://github.com/joseguaman1/distribuidos.git> |

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `Practica_04.pdf` | Reporte técnico con arquitectura, resultados y preguntas de control. |
| `Practica_04.zip` | Código fuente del sistema. |
| `README.md` | Este archivo. |

> El PDF lleva el título de plantilla "Implementar un servicio REST con Node.js", pero el contenido y el código son de IPC + sockets TCP + IA en **Python**.

## Objetivo

Combinar **comunicación entre procesos (IPC)** en una misma máquina y **comunicación en red (sockets TCP)** entre máquinas, e integrar un **agente de IA local (Ollama, vía Open WebUI)** que decide a qué servidor enviar cada mensaje, con **Round Robin** como respaldo.

## Arquitectura

```
┌────────────── cliente_system ──────────────┐        ┌──── gateway-system ────┐        ┌── servidores-system ──┐
│ productor.py ─Queue (IPC)─▶ procesador.py  │        │ gateway.py (:6000)     │        │ worker 7001 (CRÍTICO) │
│  (temp, vib, timestamp)    (calcula alerta)│        │   │ pregunta a         │  TCP   │ worker 7002 (NORMAL)  │
│                │                           │  TCP   │   ▼                    │ ─────▶ │ (imprimen el pedido)  │
│        memoria compartida ─▶ cliente.py ───┼──────▶ │ agente_ia.py ──HTTP──▶ Open WebUI / Ollama
│                (3 hilos, cada 2 s)         │        │   └─ si falla: Round Robin   │
└────────────────────────────────────────────┘        └────────────────────────┘        └───────────────────────┘
```

| Archivo | Ubicación | Función |
|---|---|---|
| `main.py` | raíz | Lanza los 4 procesos: dos workers (7001, 7002), el gateway y el cliente. |
| `productor.py` | `cliente_system/ipc_system/controls/` | Cada segundo genera `temp` (20–100), `vib` (0–10) y `timestamp`, y los pone en una `multiprocessing.Queue`. |
| `procesador.py` | idem | Saca de la cola, calcula `alerta = temp > 75 or vib > 7` y guarda el dato en memoria compartida (`Manager().dict()`). |
| `ipc_system/main.py` | `cliente_system/` | Crea la cola, la memoria compartida y los procesos productor/procesador (`iniciar_ipc()`). |
| `app.py` | `cliente_system/` | Inicia el IPC y crea **3 hilos cliente**. |
| `cliente.py` | `cliente_system/` | Cada 2 s lee el último dato de la memoria compartida y lo envía en JSON por TCP al gateway. |
| `gateway.py` | `gateway-system/` | Escucha en `:6000`, consulta al agente de IA y reenvía el JSON al worker elegido. Un hilo por conexión. |
| `agente_ia.py` | `gateway-system/` | Llama por HTTP a Open WebUI para clasificar el pedido como `CRITICO` o `NORMAL`. |
| `worker.py` / `server.py` | `servidores-system/` | Servidor TCP que recibe el JSON y lo imprime. `server.py` es un envoltorio de `worker.py`. |

### Lógica de decisión del agente

1. El gateway envía el pedido al modelo con el prompt *"Clasifica el siguiente pedido como CRITICO o NORMAL. Responde únicamente con una de esas dos palabras."*
2. Si la respuesta contiene `CRITICO` va al worker de índice 0 (**7001**); si contiene `NORMAL`, al de índice 1 (**7002**).
3. Si hay error de red, timeout (30 s), credenciales inválidas o respuesta no reconocida, se usa **Round Robin** alternando entre los workers.

## Cómo ejecutarlo

Requisito: Python 3.9 o superior.

```bash
unzip Practica_04.zip && cd <carpeta del proyecto>
python3 -m pip install -r requirements.txt
```

### Opción A – Todo en una sola máquina (solo Round Robin, sin IA)

```bash
python3 main.py
```

Sin configurar nada, la URL de la IA (`http://ip_servidor:3000/...`) no se resuelve, así que el gateway **usa Round Robin automáticamente**. En consola verás `[IPC-Productor]`, `[IPC-Procesador]`, `[CLIENTE] Enviado`, `[GATEWAY] Cliente ... -> ('127.0.0.1', 700X)` y `[WORKER 700X] Recibido`. Se detiene con `Ctrl+C`.

### Opción B – Con el agente de IA

El código lee **variables de entorno** (no carga el `.env` por sí solo). Usa `.env.example` como guía:

```bash
export OPEN_WEBUI_URL=http://<ip-del-servidor-ia>:3000/api/chat/completions
export OPEN_WEBUI_API_KEY=<tu_api_key>
export OPEN_WEBUI_MODEL=qwen3-coder:30b
python3 main.py
```

La API de la universidad que cita el reporte es `http://10.10.180.10:3000`, y requiere estar en esa red.

### Opción C – Varias computadoras (misma red)

Arranca cada parte por separado:

```bash
# PC de los servidores (por cada worker)
cd servidores-system && python3 worker.py 7001
cd servidores-system && python3 worker.py 7002

# PC del gateway (exporta también las variables de la IA)
export WORKERS=<ip-pc-servidores>:7001,<ip-pc-servidores>:7002
cd gateway-system && python3 gateway.py

# PC del cliente
export GATEWAY_HOST=<ip-pc-gateway> GATEWAY_PORT=6000
cd cliente_system && python3 app.py
```

| Variable | Valor por defecto | Uso |
|---|---|---|
| `WORKERS` | `127.0.0.1:7001,127.0.0.1:7002` | Lista `host:puerto` de los servidores. |
| `GATEWAY_HOST` / `GATEWAY_PORT` | `127.0.0.1` / `6000` | Dónde se conecta el cliente. |
| `OPEN_WEBUI_URL` | `http://ip_servidor:3000/api/chat/completions` | Endpoint de Open WebUI. |
| `OPEN_WEBUI_API_KEY` | (vacía) | Token Bearer. |
| `OPEN_WEBUI_MODEL` | `qwen3-coder:30b` | Modelo de Ollama. |

Abre los puertos **6000, 7001 y 7002** en el firewall de cada máquina.

## Mensaje que viaja por la red

```json
{ "temp": 85.2, "vib": 8.1, "timestamp": 1720000000.0, "alerta": true }
```

## Preguntas de control (resumen)

- **IPC vs. TCP:** IPC (colas de `multiprocessing`) comunica procesos de **una misma máquina**; TCP comunica procesos de **máquinas distintas** por red.
- **Agente IA y generador en equipos distintos:** no comparten memoria; se comunican con mensajes serializados (JSON).
- **Si un worker cae:** el envío TCP falla, el gateway captura el error y sigue. El reporte propone reintentar en otro worker y encolar para reintentar.
- **IA vs. reglas fijas:** la IA aporta cuando intervienen muchos factores variables (carga, distancia, prioridad); las reglas fijas son mejores para condiciones simples, rápidas y deterministas.

## Observaciones sobre el código

- Los **3 hilos cliente** envían el mismo último dato cada 2 s, así que el gateway recibe duplicados.
- El prompt solo envía los datos del pedido; **no incluye carga ni distancia de los nodos**, aunque el objetivo de la práctica menciona evaluar ambos factores.
- Si un worker no responde, el gateway registra el error pero **no reintenta** en otro (la mejora está descrita solo en el reporte).
- Gateway y workers leen un único `recv(4096)`, por lo que no soportan mensajes mayores a 4 KB.
- Las secciones **Conclusiones** y **Declaración de IA** del PDF conservan el texto de la plantilla.
