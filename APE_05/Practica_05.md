# APE 05 – Mensajería distribuida con MQTT, RabbitMQ y SQLite (telemetría de flota)

| | |
|---|---|
| **Asignatura** | Sistemas Distribuidos – 6to ciclo |
| **Docente** | José O. Guamán Q. |
| **Integrante** | Tayron Morales (reporte individual) |
| **Lenguaje** | Python 3.10+ (`paho-mqtt`, `pika`) + Docker |

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `Practica_05.pdf` | Reporte: arquitectura pub/sub con broker, matriz comparativa y reporte individual. |
| `Practica_05.zip` | Código fuente (`ape5_Viernes/`). |
| `Ape5.md` | Documentación original del proyecto. |
| `README.md` | Este archivo. |

> La plantilla del PDF conserva el encabezado de la práctica 1, pero el contenido desarrolla la arquitectura **publicador/suscriptor con brokers** aplicada a la telemetría de vehículos.

## Objetivo

Simular tres vehículos que publican telemetría (GPS, temperatura y combustible) por **MQTT**, guardarla en **SQLite** y reenviar a **RabbitMQ** los mensajes relevantes (todo el GPS y solo las alertas), aplicando el patrón pub/sub.

## Arquitectura

```
simulador_sensores.py ──MQTT (QoS 1)──▶ Mosquitto :1883
   topics: flota/<vehículo>/<sensor>          │
                                              ├──▶ suscriptor_sqlite.py ──▶ telemetria.db (SQLite)
                                              │        (guarda todo e imprime alertas)
                                              └──▶ mqtt_rabbitmq_bridge.py ──AMQP──▶ RabbitMQ :5672
                                                       ├─ cola.gps.telemetria         (todo el GPS)
                                                       ├─ cola.alertas.temperatura    (temp > 4 °C)
                                                       └─ cola.combustible.nivel      (combustible < 20 %)
```

## Estructura (`ape5_Viernes/`)

| Archivo | Función |
|---|---|
| `docker-compose.yml` | Levanta **Mosquitto** (1883) y **RabbitMQ** con panel de administración (5672 y 15672). |
| `mosquitto.conf` | Escucha en `0.0.0.0:1883`, acceso anónimo. |
| `simulador_sensores.py` | Publicador: 3 vehículos × 3 sensores = **9 mensajes por ronda**. |
| `suscriptor_sqlite.py` | Suscriptor a `flota/+/gps`, `flota/+/temperatura` y `flota/+/combustible`. Guarda en SQLite e imprime alertas. |
| `mqtt_rabbitmq_bridge.py` | Puente MQTT → RabbitMQ. Se suscribe a `flota/#` y enruta por tipo y umbral. |
| `prueba_alertas.py` | Prueba controlada: un GPS, una alerta de temperatura (7 °C) y una de combustible (15 %). |
| `verificar_resultados.py` | Cuenta los registros por tabla y lista las alertas guardadas. |
| `telemetria.db` | Base SQLite ya generada con datos de pruebas. |

## Cómo ejecutarlo

Requisitos: Python 3.10+, Docker y Docker Compose.

```bash
unzip Practica_05.zip && cd ape5_Viernes
python3 -m pip install -r requirements.txt
docker compose up -d            # Mosquitto + RabbitMQ
```

Abre **tres terminales** en esa carpeta y arranca primero los consumidores:

```bash
# Terminal 1 – guarda en SQLite
python3 suscriptor_sqlite.py

# Terminal 2 – puente hacia RabbitMQ
python3 mqtt_rabbitmq_bridge.py

# Terminal 3 – publica la telemetría
python3 simulador_sensores.py --rondas 2
# Prueba rápida, sin pausas:
python3 simulador_sensores.py --rondas 2 --pausa-vehiculo 0
```

Verificar resultados (ejecutar en `ape5_Viernes/`):

```bash
python3 verificar_resultados.py
```

Panel de RabbitMQ: <http://localhost:15672> (usuario `guest`, contraseña `guest`). Deben aparecer las tres colas duraderas con mensajes.

Prueba controlada de alertas (con suscriptor y puente activos):

```bash
python3 prueba_alertas.py
```

Para detener todo: `Ctrl+C` en cada terminal y `docker compose down`.

### Opciones de `simulador_sensores.py`

| Opción | Por defecto | Descripción |
|---|---|---|
| `--rondas` | 1 | Número de rondas de publicación. |
| `--pausa-vehiculo` | 5.0 | Segundos de espera entre un vehículo y el siguiente. |
| `--host` | localhost | Dirección del broker MQTT. |

## Cómo funciona el código

- **Simulador:** publica en `flota/<VH-00X>/<sensor>` con **QoS 1** y espera la confirmación. Valores fijos por vehículo: temperaturas 4, 7 y 3 °C; combustible 75, 15 y 50 %. Así, VH-002 genera ambas alertas, y VH-001, con 4 °C exacto, no (el umbral es estrictamente mayor que 4).
- **Suscriptor SQLite:** crea las tablas `gps_data`, `temp_data` y `fuel_data` si no existen. Guarda todos los valores, normales y de alerta, y escribe `ALERTA TEMPERATURA` o `ALERTA COMBUSTIBLE` en consola.
- **Puente:** declara las tres colas como **durables** y publica mensajes **persistentes** por el exchange por defecto. El GPS va siempre a su cola; temperatura solo si `> 4`; combustible solo si `< 20`. Los mensajes malformados se registran sin detener el puente.

## Resumen del reporte

- **Matriz comparativa:** cliente-servidor, peer-to-peer, microservicios y pub/sub con broker, según acoplamiento, escalabilidad, tolerancia a fallos, transparencia, ejemplo y complejidad.
- **Argumentos a favor de pub/sub:**
  1. Desacoplamiento: los vehículos siguen publicando aunque los consumidores estén caídos, porque las colas retienen los mensajes.
  2. Filtrado por topics y routing: cada consumidor recibe solo lo relevante.
  3. Colas duraderas y QoS 1: evitan perder telemetría ante reinicios.
- **Límite señalado:** no es ideal cuando se necesita una respuesta inmediata y sincrónica; ahí conviene cliente-servidor o REST.

## Preguntas de control (de `Ape5.md`)

1. **MQTT vs. AMQP:** MQTT es ligero y pensado para IoT. AMQP (RabbitMQ) ofrece exchanges, colas, bindings, confirmaciones y persistencia.
2. **Topics vs. colas:** los topics se filtran con comodines (`flota/#`, `flota/+/gps`). Las colas almacenan mensajes para consumidores.
3. **QoS:** 0 = como máximo una vez; 1 = al menos una vez (puede duplicar); 2 = exactamente una vez. Aquí se usa QoS 1.

## Notas

- Si ya tienes otro RabbitMQ usando los puertos 5672 y 15672 (por ejemplo el de la práctica 06), detenlo antes de levantar este.
- `verificar_resultados.py` y `suscriptor_sqlite.py` usan `telemetria.db` en la carpeta actual, así que conviene ejecutarlos desde `ape5_Viernes/`.
