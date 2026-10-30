"""Stores MQTT telemetry in SQLite and prints threshold alerts."""

import json
import sqlite3

import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883
DATABASE = "telemetria.db"


def initialize_database(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS gps_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT NOT NULL,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            speed REAL NOT NULL,
            timestamp TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS temp_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT NOT NULL,
            temperature REAL NOT NULL,
            unit TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS fuel_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT NOT NULL,
            fuel_level REAL NOT NULL,
            unit TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
        """
    )
    connection.commit()


def save_message(connection: sqlite3.Connection, topic: str, payload: dict) -> None:
    sensor = topic.rsplit("/", 1)[-1]
    if sensor == "gps":
        connection.execute(
            "INSERT INTO gps_data (vehicle_id, lat, lng, speed, timestamp) VALUES (?, ?, ?, ?, ?)",
            (payload["vehicle_id"], payload["lat"], payload["lng"], payload["speed"], payload["timestamp"]),
        )
    elif sensor == "temperatura":
        connection.execute(
            "INSERT INTO temp_data (vehicle_id, temperature, unit, timestamp) VALUES (?, ?, ?, ?)",
            (payload["vehicle_id"], payload["temperature"], payload["unit"], payload["timestamp"]),
        )
        if payload["temperature"] > 4:
            print(f"ALERTA TEMPERATURA: {payload['vehicle_id']} = {payload['temperature']} C")
    elif sensor == "combustible":
        connection.execute(
            "INSERT INTO fuel_data (vehicle_id, fuel_level, unit, timestamp) VALUES (?, ?, ?, ?)",
            (payload["vehicle_id"], payload["fuel_level"], payload["unit"], payload["timestamp"]),
        )
        if payload["fuel_level"] < 20:
            print(f"ALERTA COMBUSTIBLE: {payload['vehicle_id']} = {payload['fuel_level']} %")
    else:
        return
    connection.commit()


def main() -> None:
    connection = sqlite3.connect(DATABASE)
    initialize_database(connection)

    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"Suscriptor conectado a MQTT: {reason_code}")
        for topic in ("flota/+/gps", "flota/+/temperatura", "flota/+/combustible"):
            client.subscribe(topic, qos=1)

    def on_message(client, userdata, message):
        try:
            save_message(connection, message.topic, json.loads(message.payload.decode("utf-8")))
        except (KeyError, json.JSONDecodeError, sqlite3.Error) as error:
            print(f"Mensaje invalido en {message.topic}: {error}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="suscriptor-sqlite")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    print("Escuchando flota/+/gps, flota/+/temperatura y flota/+/combustible. Ctrl+C para detener.")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Suscriptor detenido")
    finally:
        client.disconnect()
        connection.close()


if __name__ == "__main__":
    main()
