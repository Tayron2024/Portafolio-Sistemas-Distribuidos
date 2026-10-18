from pathlib import Path
import time


CARPETA_COMUNICACION = Path(__file__).resolve().parent.parent / "canal_comunicacion"
ARCHIVO_ENTRADA = CARPETA_COMUNICACION / "entrada_servidor.txt"
ARCHIVO_SALIDA = CARPETA_COMUNICACION / "salida_servidor.txt"
INTERVALO_REVISION = 0.5


def procesar_mensaje(mensaje):
	return mensaje.upper()


def iniciar_servidor():
	CARPETA_COMUNICACION.mkdir(parents=True, exist_ok=True)
	ARCHIVO_ENTRADA.touch(exist_ok=True)
	ARCHIVO_SALIDA.touch(exist_ok=True)
	ultima_modificacion = None

	print("Servidor activo. Presiona Ctrl+C para detenerlo.")

	try:
		while True:
			modificacion_actual = ARCHIVO_ENTRADA.stat().st_mtime_ns

			if modificacion_actual != ultima_modificacion:
				ultima_modificacion = modificacion_actual
				mensaje = ARCHIVO_ENTRADA.read_text(encoding="utf-8")

				if mensaje.strip():
					respuesta = procesar_mensaje(mensaje)
					ARCHIVO_SALIDA.write_text(respuesta, encoding="utf-8")
					print(f"Mensaje procesado: {mensaje.strip()}")

			time.sleep(INTERVALO_REVISION)
	except KeyboardInterrupt:
		print("\nServidor detenido.")


if __name__ == "__main__":
	iniciar_servidor()
