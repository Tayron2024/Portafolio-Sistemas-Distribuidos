# APE 01 – Análisis colaborativo de las arquitecturas principales de un sistema distribuido

| | |
|---|---|
| **Asignatura** | Sistemas Distribuidos – 6to ciclo, Carrera de Computación (FEIRNNR, UNL) |
| **Docente** | José O. Guamán Q. |
| **Integrantes** | Tayron Morales, Ariana Córdova, Jorge Luzuriaga, Emilio Jaramillo |
| **Fechas** | 29 de septiembre y 02 de octubre de 2026 |
| **Tipo** | Documental / de análisis (**no incluye código**) |


## Objetivo

Analizar en equipo las cuatro arquitecturas fundamentales de los sistemas distribuidos (**cliente-servidor, peer-to-peer, multicapa y microservicios**), comparar sus ventajas, desventajas, escalabilidad y tolerancia a fallos, y aplicar la más adecuada a un caso de estudio.

## Qué se hizo, por fases

| Fase | Actividad | Resultado |
|---|---|---|
| 0 | Formación de equipos de 4. | Equipo conformado. |
| 1 – Investigación | Cada integrante investigó una arquitectura (estructura, ventajas, desventajas, escalabilidad, ejemplos). | Matriz de investigación y diagramas en draw.io (Figura 1). |
| 2 – Socialización | Exposición de 5 min por equipo. | Matriz comparativa grupal con los aportes de los grupos 1, 2, 4, 5, 6 y 7. |
| 3 – Caso de estudio | Selección y justificación de la arquitectura. | Propuesta para un **ingenio azucarero** (ver abajo). |
| 4 – Reporte | Conclusiones individuales y 10 preguntas de control. | Reporte PDF. |

<img width="1093" height="1005" alt="image" src="https://github.com/user-attachments/assets/ac7aecad-43d6-4296-b648-931957d401f7" />

## Resumen de la matriz de arquitecturas

| Arquitectura | Idea central | Fortaleza | Debilidad | Ejemplos citados |
|---|---|---|---|---|
| **Cliente-servidor** | Clientes piden, un servidor centralizado responde. | Información centralizada y mantenimiento simple. | Punto único de falla y saturación del servidor. | App bancaria, Gmail, sistema universitario. |
| **Peer-to-peer** | Todos los nodos son iguales (cliente y servidor a la vez). | Alta disponibilidad y escalabilidad global. | Volatilidad de nodos y mayor consumo de ancho de banda. | Napster, Gnutella, KaZaA, Torrent, Skype, Bitcoin. |
| **Multicapa** | Capas con responsabilidades separadas (presentación, lógica, datos). | Mantenimiento y pruebas independientes por capa. | Latencia y sobrecarga si una petición cruza muchas capas. | Banca en línea, matrículas universitarias, facturación. |
| **Microservicios** | Servicios pequeños e independientes comunicados por API. | Despliegue y escalado independiente por servicio. | Alta complejidad operativa y consistencia de datos. | Amazon, Uber, Netflix, Spotify. |

## Caso de estudio: ingenio azucarero

**Problema:** garantizar la continuidad de la recepción de materia prima aunque se corte la comunicación con el centro de datos.

**Solución elegida:** arquitectura **multicapa con un nodo Servidor-Cliente local**, con modo sincrónico y asincrónico.

1. **Aislamiento de fallas en la WAN:** el nodo local es servidor para las estaciones de pesaje y cliente del Data Center central.
2. **Persistencia y resincronización diferida:** sin WAN, la planta guarda en una base de datos local y sincroniza después con reglas de resolución de conflictos.
3. **Costo/beneficio y reuso:** aprovecha la LAN existente y evita paradas de fábrica.

## Preguntas de control respondidas

Sistema distribuido vs. centralizado, cliente-servidor vs. P2P, middleware, arquitectura de 3 capas, microservicios vs. monolito, arquitectura para BitTorrent, escalabilidad horizontal y vertical, transparencia, tolerancia a fallos sin servidor central y criterios del caso de estudio.

## Pendientes detectados en el reporte

- La **conclusión de Ariana Córdova** está en blanco.
- El **diagrama del caso de estudio** (Fase 3) no aparece en el documento.




