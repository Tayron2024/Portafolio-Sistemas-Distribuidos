# APE 03 – Sincronización de procesos: exclusión mutua, semáforos y problemas clásicos de concurrencia

| | |
|---|---|
| **Asignatura** | Sistemas Distribuidos – 6to ciclo |
| **Docente** | José O. Guamán Q. |
| **Integrantes** | Mateo Rojas, Leonardo Sánchez, Tayron Morales |
| **Fechas** | 06 y 09 de octubre de 2026 |
| **Stack** | Java + Spring Boot 3.5.6 (backend, un microservicio por ejercicio) y React + Vite (frontend) |
| **Repositorio original** | <https://github.com/Sebaslsst/Sistemas_Distribuidos_APE3.git> |

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `Practica_03.pdf` | Reporte con enunciados, pseudocódigo, capturas, tabla de cumplimiento y preguntas de control. |
| `Practica_03.zip` | Código fuente (`APE_3/`): 5 microservicios + frontend. |
| `README.md` | Este archivo. |

Estructura interna de `Practica_03.zip`:

```
APE_3/
├── ejercicio-1/   # Estacionamiento        → puerto 8081
├── ejercicio-2/   # Cajero automático      → puerto 8082
├── ejercicio-3/   # Productor-Consumidor   → puerto 8083
├── ejercicio-4/   # Puente                 → puerto 8084
├── ejercicio-5/   # Centro de impresión    → puerto 8085
└── frontend/      # Interfaz web React + Vite (puerto 5173)
```

## Objetivo

Aplicar mecanismos de sincronización (semáforos, mutex, variables de condición) para evitar condiciones de carrera y coordinar hilos que comparten recursos, resolviendo cinco problemas clásicos.

## Cómo ejecutarlo

**Requisitos:** Java (25 recomendado; los ejercicios 3 y 4 lo declaran en su `pom.xml`, y los 1, 2 y 5 declaran Java 21), Maven 3.9+, Node.js 18+ y npm.

```bash
unzip Practica_03.zip && cd APE_3
```

Cada microservicio se levanta en **su propia terminal**:

```bash
cd ejercicio-1 && mvn spring-boot:run     # 8081
cd ejercicio-2 && mvn spring-boot:run     # 8082
cd ejercicio-3 && mvn spring-boot:run     # 8083
cd ejercicio-4 && mvn spring-boot:run     # 8084
cd ejercicio-5 && mvn spring-boot:run     # 8085
```

Frontend:

```bash
cd frontend && npm install && npm run dev
```

Abre la URL que muestre Vite (normalmente <http://localhost:5173>). Desde ahí se elige cualquiera de los cinco ejercicios, se inicia la simulación y se ven el estado y los eventos en tiempo real. Solo hace falta tener levantado el microservicio del ejercicio que se quiera probar.

### Probar sin el frontend (API REST)

Cada ejercicio expone `POST .../start`, `GET .../status` y `GET .../events`:

```bash
curl -X POST http://localhost:8081/api/parking/start \
     -H 'Content-Type: application/json' -d '{"capacity":4}'
curl http://localhost:8081/api/parking/status
curl http://localhost:8081/api/parking/events
```

## Los cinco ejercicios

### Ejercicio 1 – Estacionamiento (semáforo contador) · `:8081` · `/api/parking`

- **Problema:** 10 vehículos concurrentes compiten por un número limitado de plazas.
- **Código:** `Semaphore spaces` inicializado con la capacidad. Cada vehículo es un hilo que hace `acquire()`, permanece 300 ms y hace `release()` al salir. Un `CountDownLatch` hace que los 10 arranquen a la vez.
- **Parámetros:** `capacity` ∈ {1, 4, 10}, para contestar la pregunta de análisis (¿y si el semáforo vale 1 o 10?).
- **Resultado:** `maxConcurrent` nunca supera la capacidad elegida.

### Ejercicio 2 – Cajero automático (exclusión mutua) · `:8082` · `/api/atm`

- **Problema:** saldo inicial de $1000 con tres procesos simultáneos: retiro de $300, retiro de $250 y depósito de $200.
- **Código:** `ReentrantLock(true)` (justo) protege la lectura y modificación del saldo, con una pausa dentro de la sección crítica para provocar la carrera si no hubiera mutex.
- **Resultado esperado:** saldo final **$650** en cualquier orden.

### Ejercicio 3 – Fábrica (productor-consumidor) · `:8083` · `/api/production`

- **Problema:** almacén de **5 piezas**, con productores y consumidores concurrentes.
- **Código:** `LinkedBlockingQueue(5)` más dos semáforos, `spaces` (5) y `elements` (0). El productor hace `spaces.acquire()`, inserta y hace `elements.release()`. El consumidor hace lo inverso.
- **Parámetros:** `producers` (1–10), `consumers` (1–10) y `piecesPerWorker` (1–50). Las piezas se reparten entre consumidores.
- **Resultado:** todas las piezas producidas se consumen y el almacén nunca pasa de 5.

### Ejercicio 4 – Puente de una dirección (control de acceso) · `:8084` · `/api/bridge`

- **Problema:** varios vehículos pueden cruzar en el mismo sentido, pero nunca norte y sur a la vez.
- **Código:** `ReentrantLock(true)` + `Condition`. Un vehículo espera mientras la dirección activa sea la contraria. Al salir el último, la dirección pasa a `NINGUNA` y se hace `signalAll()`.
- **Parámetros:** `north` (1–30), `south` (1–30) y `crossingMillis` (50–5000).
- **Nota sobre inanición:** el código se apoya en el bloqueo justo, pero no limita explícitamente cuántos vehículos seguidos pueden pasar en una dirección. Ese límite sería la mejora para el "reto" del enunciado.

### Ejercicio 5 – Centro de impresión (orden de ejecución) · `:8085` · `/api/printing`

- **Problema:** cada documento debe seguir **Diseño → Revisión → Impresión**.
- **Código:** tres semáforos encadenados, `design` (1), `review` (0) y `print` (0). Cada etapa hace `acquire()` del suyo y `release()` del siguiente; impresión vuelve a habilitar diseño. Se repite para 3 documentos.
- **Resultado:** el orden siempre es correcto. Si se elimina un `release()`, el sistema se bloquea.

## Resultados del reporte

| Ejercicio | Resultado esperado | ¿Cumple? |
|---|---|---|
| 1 | Máximo 4 vehículos dentro. | Sí |
| 2 | Saldo final $650. | Sí |
| 3 | Todo se consume y el almacén ≤ 5. | Sí |
| 4 | Una sola dirección activa. | Sí |
| 5 | Diseño → Revisión → Impresión. | Sí |

El PDF también incluye análisis de preguntas (semáforo en 1 o 10; qué pasa sin mutex; `espacios=0` o `elementos=5`) y preguntas de control (condición de carrera, mutex vs. semáforo binario, deadlock y condiciones de Coffman), además de la declaración de uso de IA.

## Observaciones

- El PDF menciona barreras de sincronización y lectores-escritores en sus objetivos y conclusiones, pero los cinco ejercicios implementados no los incluyen.
- `Practica_03.zip` incluye carpetas `target/` (compilados) y `frontend/dist/`. Se regeneran con `mvn` y `npm run build`.
