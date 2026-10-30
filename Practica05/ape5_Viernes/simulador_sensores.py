"""Publishes one telemetry round for three vehicles through MQTT."""

import argparse
import json
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883
VEHICLES = ("VH-001", "VH-002", "VH-003")
SENSORS = ("gps", "temperatura", "combustible")


def build_payload(vehicle_id: str, sensor: str, vehicle_index: int) -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    if sensor == "gps":
        return {
            "vehicle_id": vehicle_id,
            "timestamp": timestamp,
            "lat": -4.0079 + vehicle_index * 0.01,
            "lng": -79.2119 - vehicle_index * 0.01,
            "speed": 42 + vehicle_index * 5,
        }
    if sensor == "temperatura":
        return {
            "vehicle_id": vehicle_id,
            "timestamp": timestamp,
            "temperature": (4.0, 7.0, 3.0)[vehicle_index],
            "unit": "C",
        }
    return {
        "vehicle_id": vehicle_id,
        "timestamp": timestamp,
        "fuel_level": (75.0, 15.0, 50.0)[vehicle_index],
        "unit": "%",
    }


def wait_for_connection(client: mqtt.Client) -> None:
    connected = client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    if connected != mqtt.MQTT_ERR_SUCCESS:
        raise ConnectionError(f"No se pudo conectar a MQTT: codigo {connected}")
    client.loop_start()
    time.sleep(0.5)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rondas", type=int, default=1)
    parser.add_argument("--pausa-vehiculo", type=float, default=5.0)
    parser.add_argument("--host", default=BROKER_HOST)
    args = parser.parse_args()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="simulador-ape5")
    client.connect(args.host, BROKER_PORT, keepalive=60)
    client.loop_start()
    try:
        for round_number in range(1, args.rondas + 1):
            for vehicle_index, vehicle_id in enumerate(VEHICLES):
                for sensor in SENSORS:
                    topic = f"flota/{vehicle_id}/{sensor}"
                    payload = build_payload(vehicle_id, sensor, vehicle_index)
                    result = client.publish(topic, json.dumps(payload), qos=1)
                    result.wait_for_publish()
                    print(f"Ronda {round_number}: {topic} -> {payload}")
                if vehicle_id != VEHICLES[-1]:
                    time.sleep(args.pausa_vehiculo)
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
