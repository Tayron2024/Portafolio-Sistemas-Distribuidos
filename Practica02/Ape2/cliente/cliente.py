from pathlib import Path
import time


CARPETA_COMUNICACION = Path(__file__).resolve().parent.parent / "canal_comunicacion"
ARCHIVO_ENTRADA = CARPETA_COMUNICACION / "entrada_servidor.txt"
ARCHIVO_SALIDA = CARPETA_COMUNICACION / "salida_servidor.txt"
TIEMPO_ESPERA = 15
INTERVALO_REVISION = 0.5


def enviar_mensaje(mensaje):
	CARPETA_COMUNICACION.mkdir(parents=True, exist_ok=True)
	ARCHIVO_SALIDA.write_text("", encoding="utf-8")
	ARCHIVO_ENTRADA.write_text(mensaje, encoding="utf-8")

	tiempo_inicio = time.monotonic()
	while time.monotonic() - tiempo_inicio < TIEMPO_ESPERA:
		respuesta = ARCHIVO_SALIDA.read_text(encoding="utf-8")
		if respuesta:
			return respuesta
		time.sleep(INTERVALO_REVISION)

	raise TimeoutError("No se recibió respuesta del servidor.")


def iniciar_cliente():
	print("Cliente activo. Presiona Ctrl+C para salir.")

	try:
		while True:
			mensaje = input("Mensaje: ").strip()
			if not mensaje:
				print("El mensaje no puede estar vacío.")
				continue

			try:
				respuesta = enviar_mensaje(mensaje)
				print(f"Respuesta: {respuesta}")
			except TimeoutError as error:
				print(error)
	except KeyboardInterrupt:
		print("\nCliente detenido.")


if __name__ == "__main__":
	iniciar_cliente()
