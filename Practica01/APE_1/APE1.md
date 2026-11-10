# Práctica 01 – Análisis Colaborativo de las Arquitecturas Principales en un Sistema Distribuido

**Universidad Nacional de Loja – FEIRNNR, Carrera de Computación**
**Asignatura:** Sistemas Distribuidos | **Ciclo:** 6to | **Docente:** José O. Guamán Q.
**Unidad:** Envío de mensajes distribuido
**Fechas:** 29 de septiembre y 02 de octubre de 2026

**Integrantes del equipo:**
- Tayron Fernando Morales Villamagua
- Ariana Alejandra Córdova Betancourt
- Jorge Luis Luzuriaga Betancourt
- Emilio Ramiro Jaramillo

---

## 1. ¿De qué trató la práctica?

La práctica consistió en **analizar de forma colaborativa las cuatro arquitecturas fundamentales de los sistemas distribuidos**: cliente-servidor, peer-to-peer (P2P), multicapa (n-tier) y microservicios. El trabajo se dividió en cuatro fases: investigar, socializar, resolver un caso de estudio y redactar el reporte final.

### Objetivos

1. Identificar las características estructurales y funcionales de cada arquitectura.
2. Comparar ventajas, desventajas, escalabilidad y tolerancia a fallos mediante una **matriz de análisis colaborativa**.
3. Diseñar el diagrama de un **caso de estudio**, eligiendo la arquitectura más adecuada y justificándola técnicamente.

### Herramientas

- Computadora personal con conexión a internet.
- Guía de práctica y plantilla de matriz comparativa.
- Procesador de texto y **draw.io** para los diagramas.

---

## 2. Metodología ejecutada

| Fase | Duración | Actividad |
|------|----------|-----------|
| 0 | 10 min | Formación de equipos de 4 integrantes (asignados por el docente). |
| 1 – Investigación | 50 min | Cada integrante investigó una arquitectura y completó su sección de la matriz. El equipo elaboró los diagramas en draw.io. |
| 2 – Socialización | 30 min | Cada equipo expuso 5 minutos; el resto completó una matriz comparativa grupal. |
| 3 – Caso de estudio | 55 min | Selección de la arquitectura más adecuada, justificación con mínimo 3 argumentos técnicos, diagrama de la solución e identificación de transparencia, escalabilidad y tolerancia a fallos. |
| 4 – Reporte y entrega | 25 min | Conclusiones individuales, compilación de la matriz final y los diagramas, y entrega en la plataforma. |

---

## 3. Fase 1 – Investigación y diagramas

Se elaboró la **Figura 1** en draw.io, con un diagrama por arquitectura:

- **Cliente-servidor:** varios clientes conectados a un servidor a través de la red.
- **Multicapa:** el usuario final interactúa con la capa de presentación, que se comunica con la lógica de negocio, el acceso a datos y la capa de datos. Todo se agrupa en un *Nivel de Aplicación* y un *Nivel de Datos*.
- **Cliente-servidor (estrella):** varios clientes conectados a un único servidor central.
- **Microservicios:** aplicaciones móvil y web que acceden a un *API Gateway*, el cual enruta hacia tres microservicios, cada uno con su propia base de datos.

### Matriz de investigación (resumen)

#### Cliente-Servidor
- **Estructura:** el cliente (dispositivo o aplicación que interactúa con el usuario) envía peticiones; el servidor las espera y devuelve una respuesta; la red es el medio físico o inalámbrico.
- **Ventajas:** centraliza información y recursos, permite que varios clientes usen los mismos servicios y el mantenimiento se hace en el servidor sin modificar cada cliente.
- **Desventajas:** si el servidor falla, los clientes quedan sin servicio; con demasiadas solicitudes puede saturarse.
- **Escalabilidad:** vertical (más recursos al servidor) y horizontal (más servidores).
- **Ejemplo:** una app bancaria. El cliente es el teléfono o navegador y el servidor es el sistema central del banco, que valida identidad, consulta la base de datos de cuentas y devuelve el resultado.

#### Peer-to-Peer
- **Estructura:** red virtual superpuesta sobre la red física, con simetría de roles y nodos en los bordes. Sus modelos topológicos son semicentralizado, descentralizado no estructurado y descentralizado estructurado.
- **Ventajas:** colaboración directa e intercambio de recursos, menores costos de infraestructura, alta disponibilidad y tolerancia a fallos.
- **Desventajas:** dificultades de direccionamiento, volatilidad de la red, alto consumo de ancho de banda y riesgos de seguridad y confianza.
- **Escalabilidad:** lineal (más usuarios, más demanda de recursos) y de redes masivas.
- **Ejemplos:** Napster (directorio central), Gnutella (descentralizado) y KaZaA/FastTrack (supernodos).

#### Multicapa
- **Estructura:** capa de presentación, capa de lógica de negocio, capa de acceso a datos y capa de datos. No se limita a tres o cuatro capas.
- **Ventajas:** cada capa se administra, mantiene y prueba de forma independiente, y es adecuada para aplicaciones de gran escala.
- **Desventajas:** una operación sencilla puede atravesar varias capas innecesariamente, lo que agrega sobrecarga y puede ser excesivo para proyectos pequeños.
- **Escalabilidad:** vertical (RAM, CPU) y horizontal (más servidores).
- **Ejemplo:** un sistema de facturación de cuatro capas (presentación, negocio, entidad y datos).

#### Microservicios
- **Estructura:** API Gateway, microservicios independientes, una base de datos por servicio y un registro/puerto de servicios.
- **Ventajas:** autonomía de los equipos, servicios simples, despliegue rápido, múltiples tecnologías y subdominios bien definidos.
- **Desventajas:** interacciones complejas o ineficientes, alta complejidad operativa, datos fragmentados y pruebas/depuración complicadas.
- **Escalabilidad:** horizontal (más instancias) y vertical.
- **Ejemplos:** Amazon (el servicio de Pedidos consulta el stock al de Inventario mediante una API, sin acoplamiento directo de datos) y Uber (el patrón *Saga* ejecuta una transacción compensatoria si falla el cobro tras asignar al conductor).

---

## 4. Fase 2 – Socialización y matriz comparativa grupal

Cada grupo expuso su investigación y se consolidó una matriz con la información de los **Grupos 1, 2, 4, 5, 6 y 7**. Las ideas más repetidas fueron:

| Criterio | Cliente-Servidor | Peer-to-Peer | Multicapa | Microservicios |
|----------|------------------|--------------|-----------|----------------|
| **Estructura** | Cliente solicita, servidor procesa y responde. | Todos los nodos son iguales, sin servidores ni clientes fijos. | Capas con responsabilidades separadas (presentación, lógica, datos). | Servicios pequeños e independientes comunicados por red mediante un API Gateway. |
| **Ventajas** | Información centralizada, mantenimiento en el servidor, seguridad y manejo de usuarios. | Escalabilidad alta, cada nodo comparte información, si un nodo falla el resto sigue. | Organización jerárquica, los errores no se propagan, pruebas por capa, uso de cachés en la capa media. | Despliegue independiente, libertad tecnológica, resiliencia, equipos autónomos. |
| **Desventajas** | Saturación del servidor y punto único de falla. | Volatilidad de nodos, información repetida, difícil depurar fallos, carga al ancho de banda. | Latencia cuando muchas peticiones cruzan las capas y mayor complejidad inicial. | Latencia entre servicios, complejidad de gestión, consistencia de datos y mayor superficie de ataque. |
| **Escalabilidad** | Principalmente vertical: se mejora el hardware del servidor. | Alta y global, depende de cuántos nodos participen. | Por capas, intermedia entre un monolito y los microservicios. | Alta y granular: se escala solo el servicio con más demanda. |
| **Ejemplos** | Sistema universitario, Netflix/YouTube, Banco de Loja, Gmail, juegos en línea. | Skype, Torrent, Bitcoin, Gnutella, Windows Delivery Optimization. | Banca en línea, sistema de matrículas, tienda universitaria. | Netflix, SoundCloud, Spotify, Uber, J.P. Morgan, Deuna, apps de comida. |

---

## 5. Fase 3 – Caso de estudio

### Problema
Garantizar la **continuidad operativa de la recepción de materia prima en un ingenio azucarero**, un proceso de misión crítica expuesto a cortes de comunicación.

### Arquitectura seleccionada
**Arquitectura Multicapa con patrón Servidor-Cliente local**, habilitada para funcionar en **modo sincrónico y asincrónico**.

### Justificación técnica

1. **Aislamiento de fallas en la red WAN.** Un nodo Servidor-Cliente local actúa como *servidor* ante las estaciones de pesaje y como *cliente* frente al Data Center central. Así, la operación en planta no depende de la disponibilidad del enlace remoto.
2. **Persistencia y resincronización diferida.** Si se corta la conexión WAN, la planta pasa a *modo asincrónico* y registra las transacciones en una base de datos local. Al restablecerse la red, servicios en segundo plano sincronizan los datos con el sistema central mediante reglas de resolución de conflictos.
3. **Alta relación costo/beneficio y reuso de infraestructura.** Se aprovecha la red LAN existente y se evitan pérdidas por paradas de fábrica, sin reestructurar los sistemas corporativos.

### Dónde se aplican los conceptos clave

- **Transparencia:** los operarios de las estaciones de pesaje trabajan igual esté la WAN disponible o no, sin notar la complejidad de la sincronización.
- **Escalabilidad:** se pueden añadir estaciones de pesaje a la LAN local y recursos al nodo local o al Data Center.
- **Tolerancia a fallos:** el modo asincrónico con base de datos local mantiene el servicio ante cortes de red.

---

## 6. Fase 4 – Conclusiones individuales

- **Tayron Morales:** ningún modelo es universalmente superior. La elección depende de equilibrar el acoplamiento, los costos de infraestructura y las necesidades del negocio. La fortaleza de un sistema distribuido está en ocultar su complejidad (transparencia) y garantizar la continuidad mediante replicación, operación asincrónica y tolerancia a fallos parciales.
- **Jorge Luzuriaga:** el ingeniero debe conocer todas las opciones y elegir según el contexto: presupuesto, alcance del proyecto o preferencias del usuario final.
- **Ariana Córdova:** *(en el documento original esta sección está en blanco; falta redactarla).*
- **Emilio Jaramillo:** cada arquitectura tiene estructura, ventajas, desventajas, ejemplos y escalabilidad distintos, por lo que el diseñador debe seleccionar la más efectiva según los parámetros del sistema que quiere desarrollar.

---

## 7. Preguntas de control (resumen de respuestas)

1. **Sistema distribuido vs. centralizado:** un sistema distribuido son varios computadores que trabajan juntos por red y no dependen de un único equipo. Sus características son compartición de recursos, comunicación entre nodos, concurrencia, escalabilidad, tolerancia a fallos y transparencia.
2. **Comunicación cliente-servidor vs. P2P:** en cliente-servidor, los clientes piden y un servidor centralizado responde. En P2P, cada dispositivo es cliente y servidor a la vez, y se comunican directamente.
3. **Middleware:** coordina la comunicación y el acceso a servicios entre aplicaciones y equipos. Se ubica entre el sistema operativo y las aplicaciones, ocultando parte de la complejidad de la distribución.
4. **Arquitectura de tres capas:** presentación (interfaz), lógica de negocio (reglas y operaciones) y datos (almacenamiento). Separarlas permite modificar una capa sin afectar a las demás y facilita pruebas, actualización y escalabilidad.
5. **Microservicios vs. monolito:** ofrecen despliegue, escalado y mantenimiento independientes y diversidad tecnológica. Como desafíos, introducen más complejidad de comunicación, monitoreo, seguridad, gestión de datos y despliegue.
6. **Arquitectura para BitTorrent:** P2P, porque los usuarios comparten partes de los archivos directamente, lo que reparte la carga y evita depender de un único servidor.
7. **Escalabilidad horizontal y vertical:** la vertical aumenta recursos de un servidor (RAM, CPU, almacenamiento). La horizontal agrega más servidores o nodos. Las arquitecturas distribuidas favorecen la horizontal.
8. **Transparencia:** el sistema oculta que los recursos están distribuidos. Dos tipos son la transparencia de ubicación (no importa dónde está el recurso) y la de acceso (no importa cómo se accede a él).
9. **Si un servidor central falla:** P2P puede seguir funcionando porque no depende de un único servidor, aunque algunos servicios podrían verse afectados según el diseño.
10. **Criterios decisivos del caso de estudio:** cantidad de usuarios, escalabilidad, disponibilidad, distribución de recursos, tolerancia a fallos, facilidad de mantenimiento y forma de comunicación entre componentes.

---

## 8. Resultado y aprendizaje general

Con la práctica se logró:

- Comprender la **estructura, ventajas y limitaciones** de las cuatro arquitecturas principales.
- Construir una **matriz comparativa colaborativa** a partir de las exposiciones de varios grupos.
- Aplicar lo aprendido en un **caso real** (el ingenio azucarero), eligiendo una arquitectura híbrida (multicapa con servidor-cliente local) y justificándola con criterios de transparencia, escalabilidad y tolerancia a fallos.
- Reforzar la idea central de que **no existe una arquitectura universalmente mejor**: la decisión depende del contexto, el presupuesto y los requisitos del sistema.
