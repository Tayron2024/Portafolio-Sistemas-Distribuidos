"""Routes selected MQTT telemetry to durable RabbitMQ queues."""

import json

import pika
import paho.mqtt.client as mqtt


MQTT_HOST = "localhost"
MQTT_PORT = 1883
RABBITMQ_HOST = "localhost"
QUEUES = (
    "cola.gps.telemetria",
    "cola.alertas.temperatura",
    "cola.combustible.nivel",
)


def main() -> None:
    rabbit = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = rabbit.channel()
    for queue in QUEUES:
        channel.queue_declare(queue=queue, durable=True)

    def publish(queue: str, payload: dict) -> None:
        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(payload),
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )
        print(f"RabbitMQ: {queue} <- {payload}")

    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"Puente conectado a MQTT: {reason_code}")
        client.subscribe("flota/#", qos=1)

    def on_message(client, userdata, message):
        try:
            payload = json.loads(message.payload.decode("utf-8"))
            if message.topic.endswith("/gps"):
                publish("cola.gps.telemetria", payload)
            elif message.topic.endswith("/temperatura") and payload["temperature"] > 4:
                publish("cola.alertas.temperatura", payload)
            elif message.topic.endswith("/combustible") and payload["fuel_level"] < 20:
                publish("cola.combustible.nivel", payload)
        except (KeyError, json.JSONDecodeError, pika.exceptions.AMQPError) as error:
            print(f"Mensaje no procesado en {message.topic}: {error}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="puente-rabbitmq")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    print("Puente activo para flota/#. Ctrl+C para detener.")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Puente detenido")
    finally:
        client.disconnect()
        rabbit.close()


if __name__ == "__main__":
    main()
