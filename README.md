# Portafolio de Sistemas Distribuidos

**Universidad Nacional de Loja – FEIRNNR, Carrera de Computación**
**Asignatura:** Sistemas Distribuidos · **Ciclo:** 6to · **Docente:** José O. Guamán Q.
**Estudiante:** Tayron Morales (junto con los compañeros indicados en cada práctica)

Este repositorio reúne las **Actividades Práctico-Experimentales (APE)** de la unidad *Envío de mensajes distribuido*. Cada carpeta contiene el reporte en PDF, el código (cuando la práctica lo requiere) y un `README.md` con las instrucciones para ejecutarlo.

## Resumen de las prácticas

| Práctica | Tema | Tipo | Tecnologías | Integrantes |
|---|---|---|---|---|
| [**APE 01**](APE_01/README.md) | Análisis colaborativo de las arquitecturas distribuidas (cliente-servidor, P2P, multicapa y microservicios) | Análisis documental | Draw.io | Tayron Morales, Ariana Córdova, Jorge Luzuriaga, Emilio Jaramillo |
| [**APE 02**](APE_02/README.md) | Cliente-servidor con archivos de texto como canal | Código | Python | Tayron Morales |
| [**APE 03**](APE_03/README.md) | Sincronización de procesos: semáforos, mutex y problemas clásicos de concurrencia | Código | Java, Spring Boot, React, Vite | Mateo Rojas, Leonardo Sánchez, Tayron Morales |
| [**APE 04**](APE_04/README.md) | Asignación de pedidos con IPC, sockets TCP y un agente de IA (Ollama) | Código | Python, sockets, `multiprocessing`, Open WebUI | Tayron Morales, Mateo Rojas, Leonardo Sánchez |
| [**APE 05**](APE_05/README.md) | Mensajería pub/sub con MQTT, RabbitMQ y SQLite | Código | Python, Mosquitto, RabbitMQ, SQLite, Docker | Tayron Morales |
| [**APE 06**](APE_06/README.md) | Microservicios con RabbitMQ y Spring Boot (Fleet Monitor) | Código | Java, Spring Boot, Spring AMQP, H2, Docker | — (no figura en el PDF) |

## Estructura del repositorio

```
Portafolio-Sistemas-Distribuidos/
├── README.md                  # Este archivo
├── APE_01/  README.md · APE 1 SD.pdf · Pratica_01.md
├── APE_02/  README.md · Practica_02.pdf · Ape2/ (servidor, cliente, canal_comunicacion)
├── APE_03/  README.md · Practica_03.pdf · Practica_03.zip (5 microservicios + frontend)
├── APE_04/  README.md · Practica_04.pdf · Practica_04.zip (cliente, gateway, servidores)
├── APE_05/  README.md · Practica_05.pdf · Practica_05.zip (MQTT + RabbitMQ + SQLite) · Ape5.md
└── APE_06/  README.md · Practica_06.pdf · Practica_06.zip (Spring Boot + RabbitMQ)
```

## Hilo conductor: de la arquitectura a la mensajería

Las seis prácticas siguen una progresión: primero se entienden los modelos y después se construyen formas cada vez más completas de comunicar procesos.

```
APE 01  Qué arquitecturas existen y cuándo usar cada una
   │
APE 02  Comunicación indirecta por medio compartido (archivos)
   │
APE 03  Cómo coordinar hilos y procesos que comparten recursos (sincronización)
   │
APE 04  Comunicación entre procesos (IPC) y entre máquinas (sockets TCP) + decisión con IA
   │
APE 05  Mensajería asíncrona desacoplada: MQTT → RabbitMQ → SQLite
   │
APE 06  Microservicios que consumen colas y exponen una API REST
```

| Concepto | Dónde se trabaja |
|---|---|
| Arquitecturas cliente-servidor, P2P, multicapa y microservicios | APE 01 (teoría), APE 02 (cliente-servidor), APE 06 (microservicios) |
| Desacoplamiento | APE 02, APE 05 y APE 06 |
| Exclusión mutua, semáforos y condiciones de carrera | APE 03 |
| IPC y sockets TCP | APE 04 |
| Pub/sub, topics, colas y QoS | APE 05 y APE 06 |
| Tolerancia a fallos y persistencia de mensajes | APE 01 (caso del ingenio), APE 05 y APE 06 (colas duraderas) |
| IA como apoyo a decisiones del sistema | APE 04 |

## Requisitos generales

| Herramienta | Versión sugerida | Se usa en |
|---|---|---|
| Python | 3.10 o superior | APE 02, 04, 05 |
| Java (JDK) | 25 (los ejercicios 1, 2 y 5 de APE 03 declaran 21) | APE 03, 06 |
| Maven | 3.9 o superior | APE 03, 06 |
| Node.js y npm | 18 o superior | APE 03 (frontend) |
| Docker y Docker Compose | Reciente | APE 05, 06 |
| Acceso a Open WebUI / Ollama | Opcional (con respaldo Round Robin) | APE 04 |

## Puertos utilizados

| Puerto | Servicio | Práctica |
|---|---|---|
| 8081 – 8085 | Microservicios de los ejercicios 1 al 5 | APE 03 |
| 5173 | Frontend (Vite) | APE 03 |
| 6000 | Gateway | APE 04 |
| 7001 / 7002 | Workers (servidores) | APE 04 |
| 3000 | Open WebUI (servidor de IA) | APE 04 |
| 1883 | Broker MQTT (Mosquitto) | APE 05 |
| 5672 / 15672 | RabbitMQ (AMQP / panel web) | APE 05 y 06 |
| 8080 | API REST Fleet Monitor | APE 06 |

> **Ojo:** APE 05 y APE 06 usan los mismos puertos de RabbitMQ (5672 y 15672) con credenciales distintas. No levantes ambos a la vez; revisa la sección de integración en el README de APE 06.

## Cómo ejecutar cada práctica

Los pasos completos están en el README de cada carpeta. Este es el resumen:

| Práctica | Comando principal |
|---|---|
| APE 01 | No tiene código; leer `APE 1 SD.pdf` o `Pratica_01.md`. |
| APE 02 | `python3 servidor/servidor.py` y, en otra terminal, `python3 cliente/cliente.py` (desde `Ape2/`). |
| APE 03 | `mvn spring-boot:run` en cada `ejercicio-N`, más `npm install && npm run dev` en `frontend/`. |
| APE 04 | `pip install -r requirements.txt` y `python3 main.py` (configurar variables de entorno para usar la IA). |
| APE 05 | `docker compose up -d`, luego `suscriptor_sqlite.py`, `mqtt_rabbitmq_bridge.py` y `simulador_sensores.py`. |
| APE 06 | `./start.sh`, o `docker compose -f docker-compose-rabbitmq.yml up -d` y `mvn spring-boot:run`. |

## Notas del portafolio

- **APE 01:** falta la conclusión de Ariana Córdova y el diagrama del caso de estudio en el reporte.
- **APE 04:** el título del PDF dice "servicio REST con Node.js", pero el trabajo es en Python con IPC, sockets y IA.
- **APE 05:** el encabezado del PDF conserva la plantilla de la práctica 1.
- **APE 06:** la API devuelve datos fijos de ejemplo y las respuestas de las preguntas de control están pendientes. Los guiones de video indican Java 17 y Spring Boot 3.2, y el proyecto usa Java 25 y Spring Boot 3.5.16.
- Varias carpetas incluyen artefactos generados (`target/`, `dist/`, `__pycache__/`) que se pueden regenerar y excluir del repositorio con un `.gitignore`.
