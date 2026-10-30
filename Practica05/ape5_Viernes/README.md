# APE 005: MQTT + SQLite + RabbitMQ

Proyecto de la práctica del viernes: simula tres vehículos, guarda telemetría en SQLite y reenvía GPS y alertas a RabbitMQ.

## Requisitos

- Python 3.10 o superior
- Docker y Docker Compose
- Dependencias de `requirements.txt`

## Ejecución

```bash
python3 -m pip install -r requirements.txt
docker compose up -d
```

En terminales separadas, iniciar los consumidores antes del simulador:

```bash
python3 suscriptor_sqlite.py
python3 mqtt_rabbitmq_bridge.py
python3 simulador_sensores.py --rondas 2
python3 verificar_resultados.py
```

Cada ronda publica 9 mensajes. El simulador espera 5 segundos después de cada vehículo; para pruebas rápidas se puede usar `--pausa-vehiculo 0`.

RabbitMQ Management está en <http://localhost:15672> con `guest` / `guest`. Deben aparecer estas colas duraderas:

- `cola.gps.telemetria`: todos los GPS.
- `cola.alertas.temperatura`: temperatura mayor que 4 °C.
- `cola.combustible.nivel`: combustible menor que 20 %.

La base `telemetria.db` contiene `gps_data`, `temp_data` y `fuel_data`. Se guardan tanto los valores normales como los que generan alerta.

## Prueba controlada

Con el suscriptor y el puente activos:

```bash
python3 prueba_alertas.py
```

Publica GPS con velocidad 42, temperatura 7 y combustible 15. El primer mensaje llega a la cola GPS y los otros dos a sus respectivas colas de alerta.

## Respuestas de control

1. **MQTT vs AMQP:** MQTT es un protocolo ligero basado en publish/subscribe, ideal para dispositivos IoT con poco ancho de banda y recursos limitados. AMQP ofrece mensajería empresarial con exchanges, colas, bindings, confirmaciones y persistencia. Aquí MQTT recibe telemetría de los vehículos y RabbitMQ distribuye mensajes seleccionados.
2. **Topics vs colas:** la jerarquía de topics permite filtrar publicaciones con comodines como `flota/#` y `flota/+/gps`. Las colas almacenan mensajes para consumidores; exchanges y bindings definen cómo se enrutan hacia esas colas.
3. **QoS 0 / 1 / 2:** QoS 0 entrega como máximo una vez, QoS 1 al menos una vez y puede duplicar, y QoS 2 exactamente una vez con mayor costo. Esta práctica usa QoS 1 para no perder telemetría durante la entrega.

## Evidencias sugeridas

1. Suscripción MQTT mostrando los topics de los tres vehículos.
2. Salida de `verificar_resultados.py` con las tres tablas y alertas.
3. Consola del suscriptor mostrando alertas de 7 °C y 15 %.
4. Panel de RabbitMQ mostrando las tres colas con mensajes.

Para detener los servicios: `docker compose down`.
