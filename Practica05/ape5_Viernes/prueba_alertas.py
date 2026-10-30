"""Publishes one GPS, one temperature alert and one fuel alert."""

import json
import time

import paho.mqtt.client as mqtt


def main() -> None:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="prueba-alertas")
    client.connect("localhost", 1883, keepalive=60)
    client.loop_start()
    messages = (
        ("flota/VH-TEST/gps", {"vehicle_id": "VH-TEST", "timestamp": "prueba", "lat": 0, "lng": 0, "speed": 42}),
        ("flota/VH-TEST/temperatura", {"vehicle_id": "VH-TEST", "timestamp": "prueba", "temperature": 7, "unit": "C"}),
        ("flota/VH-TEST/combustible", {"vehicle_id": "VH-TEST", "timestamp": "prueba", "fuel_level": 15, "unit": "%"}),
    )
    try:
        for topic, payload in messages:
            client.publish(topic, json.dumps(payload), qos=1).wait_for_publish()
            print(f"Publicado: {topic} -> {payload}")
            time.sleep(0.5)
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
