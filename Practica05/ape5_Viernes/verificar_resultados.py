"""Checks SQLite counts and reports stored alerts."""

import sqlite3


def main() -> None:
    with sqlite3.connect("telemetria.db") as connection:
        for table in ("gps_data", "temp_data", "fuel_data"):
            count = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table}: {count} registros")
        temperature_alerts = connection.execute(
            "SELECT vehicle_id, temperature FROM temp_data WHERE temperature > 4"
        ).fetchall()
        fuel_alerts = connection.execute(
            "SELECT vehicle_id, fuel_level FROM fuel_data WHERE fuel_level < 20"
        ).fetchall()
        print(f"Alertas de temperatura: {temperature_alerts}")
        print(f"Alertas de combustible: {fuel_alerts}")


if __name__ == "__main__":
    main()
