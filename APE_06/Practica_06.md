# APE 06 – Microservicios con RabbitMQ y Spring Boot (Parte 2: Fleet Monitor)

| | |
|---|---|
| **Asignatura** | Sistemas Distribuidos – 6to ciclo |
| **Docente** | José O. Guamán Q. |
| **Fechas** | 27 y 30 de octubre de 2026 |
| **Stack** | Java 25, Spring Boot 3.5.16, Spring AMQP, Spring Web, Spring Data JPA + H2, Maven, RabbitMQ (Docker) |

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `Practica_06.pdf` | Guía de la práctica con el código a implementar, preguntas de control y rúbrica. |
| `Practica_06.zip` | Proyecto `practica_06/` (código, `pom.xml`, `start.sh`, Docker Compose, guiones de video y el JAR compilado). |
| `README.md` | Este archivo. |

## Objetivo

Continuar la práctica 5 con una aplicación **Spring Boot** que **consume las colas de RabbitMQ**, declara el exchange y los bindings, **reenvía las alertas a una cola de notificaciones** y expone una **API REST** para consultar el estado de la flota de un sistema de monitoreo logístico.

## Flujo de datos

```
Sensores ─MQTT─▶ Mosquitto ─▶ Puente Python (APE 5) ─AMQP─▶ RabbitMQ
                                                              │
                  ┌───────────────────────────────────────────┤
                  ▼                                           ▼
 cola.gps.telemetria ─▶ GpsConsumer     cola.alertas.temperatura ─┐
                        (log del GPS)   cola.combustible.nivel ───┴▶ AlertConsumer
                                                                       │ reenvía
                                                                       ▼
                                                           cola.notificaciones

                 API REST (Spring Web, :8080)  /api/fleet/...
```

## Estructura del proyecto

```
practica_06/
├── pom.xml
├── docker-compose-rabbitmq.yml
├── start.sh                         # Arranque rápido
├── idk/                             # Guiones para el video de la práctica
├── src/main/resources/application.properties
└── src/main/java/com/fleet/monitor/
    ├── FleetMonitorApplication.java
    ├── config/RabbitMQConfig.java
    ├── model/GpsMessage.java
    ├── consumer/GpsConsumer.java
    ├── consumer/AlertConsumer.java
    └── controller/FleetController.java
```

## Cómo ejecutarlo

Requisitos: **Java 25** (la guía menciona JDK 17, pero el `pom.xml` está en 25), **Maven 3.8+** y **Docker** con Docker Compose.

```bash
unzip Practica_06.zip && cd practica_06
```

### Opción rápida

```bash
chmod +x start.sh && ./start.sh
```

El script levanta RabbitMQ, espera 5 s, compila con `mvn clean package -DskipTests`, inicia el JAR y prueba `/api/fleet/status`.

### Paso a paso

```bash
# 1. RabbitMQ
docker compose -f docker-compose-rabbitmq.yml up -d

# 2. Aplicación
mvn spring-boot:run
```

| Servicio | URL | Credenciales |
|---|---|---|
| API REST | <http://localhost:8080> | — |
| Panel de RabbitMQ | <http://localhost:15672> | `admin` / `admin123` |
| Consola H2 | <http://localhost:8080/h2-console> | JDBC `jdbc:h2:mem:fleetdb`, usuario `sa`, sin contraseña |

### Probar la API

```bash
curl http://localhost:8080/api/fleet/status
curl http://localhost:8080/api/fleet/vehicle/VH-001/telemetria
```

### Probar los consumidores

Con la app corriendo, abre el panel de RabbitMQ → **Exchanges → `exchange.fleet` → Publish message** y publica un JSON con una de estas *routing keys*:

| Routing key | Cola destino | Qué debería pasar en los logs |
|---|---|---|
| `gps.routing` | `cola.gps.telemetria` | `GPS recibido: ...` |
| `temp.alert` | `cola.alertas.temperatura` | `ALERTA TEMPERATURA: ...` y copia en `cola.notificaciones` |
| `fuel.routing` | `cola.combustible.nivel` | `ALERTA COMBUSTIBLE: ...` y copia en `cola.notificaciones` |

Ejemplo de cuerpo:

```json
{"vehicle_id":"VH-002","timestamp":"2026-11-02T10:00:00Z","temperature":7.0,"unit":"C"}
```

### Integración con la práctica 5 (extremo a extremo)

La Parte 1 y la Parte 2 usan **credenciales distintas** de RabbitMQ y los **mismos puertos** (5672 y 15672), por lo que no pueden correr a la vez:

1. Levanta solo un RabbitMQ.
2. Si usas el de la práctica 5 (`guest`/`guest`), cambia `spring.rabbitmq.username` y `password` en `application.properties` a `guest`.
3. Si usas el de esta práctica (`admin`/`admin123`), el puente de la práctica 5 necesita esas credenciales, porque `pika` usa `guest` por defecto.

Después arranca la app Spring Boot, el puente y el simulador de la práctica 5.

## Cómo funciona el código

- **`RabbitMQConfig`** declara el `DirectExchange` **`exchange.fleet`**, cuatro colas **durables** (`cola.gps.telemetria`, `cola.alertas.temperatura`, `cola.combustible.nivel` y `cola.notificaciones`) y tres bindings con las routing keys `gps.routing`, `temp.alert` y `fuel.routing`.
- **`GpsConsumer`** usa `@RabbitListener` sobre la cola GPS y registra cada mensaje en el log. El comentario del código deja pendiente el almacenamiento en base de datos.
- **`AlertConsumer`** tiene dos `@RabbitListener` (temperatura y combustible). Cada alerta se escribe en el log como `WARN` y se reenvía con `RabbitTemplate` a `cola.notificaciones`.
- **`FleetController`** expone `GET /api/fleet/status` y `GET /api/fleet/vehicle/{id}/telemetria`.
- **`GpsMessage`** modela los campos del JSON de GPS (`vehicleId`, `timestamp`, `lat`, `lng`, `speed`).
- **`application.properties`** configura el puerto 8080, H2 en memoria, la conexión a RabbitMQ (`localhost:5672`, `admin`/`admin123`) y los logs en nivel `DEBUG`.

## Preguntas de control de la guía

Exchanges de RabbitMQ (direct, fanout, topic, headers), colas durables y reinicio del broker, pub/sub vs. punto a punto, y seguridad en MQTT y RabbitMQ (autenticación, autorización, TLS y control de acceso). Las respuestas aún deben redactarse en el reporte final.

## Rúbrica de evaluación (de la guía)

| Criterio | Puntaje máx. |
|---|---|
| Funcionamiento (back-end y front-end) | 3 |
| Documento de práctica (enlace a Git, metodología, resultados, preguntas de control, bibliografía, conclusiones y video) | 3 |
| Defensa de la práctica | 4 |

## Observaciones

- La API REST devuelve **datos fijos de ejemplo** (3 vehículos y 2 alertas) tal como pedía la guía; todavía no consulta la telemetría real recibida.
- H2 y JPA están configurados, pero ningún consumidor persiste datos aún.
- Nadie consume `cola.notificaciones`: los mensajes se acumulan ahí y pueden verse en el panel de RabbitMQ.
- Los guiones de `idk/` mencionan **Spring Boot 3.2 y Java 17**, mientras el `pom.xml` usa **Spring Boot 3.5.16 y Java 25**. Conviene alinear estos datos antes de grabar el video.
- El `README.md` original del proyecto contenía rutas absolutas de otra máquina; las instrucciones de este archivo las reemplazan.
