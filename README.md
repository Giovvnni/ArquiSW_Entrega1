# Proyecto Logística (arquitectura y estado actual)

Este repositorio implementa un prototipo de gestión logística con pedidos, repartidores, rutas y un sistema de eventos/notifications interno. El diseño usa patrones como Factory, Facade y Decorator para mantener separación de responsabilidades y facilitar extensiones.

Estructura principal:

- `models/`: Entidades del dominio (`pedido.py`, `repartidor.py`, `route.py`).
- `factories/`: Fábricas para instanciar entidades (`PedidoFactory.py`, `RepartidorFactory.py`, `RouteFactory.py`).
- `decorators/`: Extensiones para `Pedido` (`PedidoDecorator.py`).
- `facades/`: `LogisticaFacade.py` — orquesta creación, validación, asignación y ciclo de rutas.
- `managers/` (o módulos del mismo propósito): `EventBus`, `EventLogger`, `NotificationManager`, `PedidoManager`, `RepartidorManager`, `RouteManager` (gestión en memoria y pub/sub).
- `main.py`: Ejecutor de ejemplo y flujo de depuración.

Casos de uso implementados:

1. Gestión de pedidos
   - a. Crear pedidos desde distintos canales
   - b. Validar información
   - c. Gestionar estados (Creado → Validado → Asignado → En ruta → Entregado)

2. Gestión de repartidores
   - a. Registrar repartidores
   - b. Gestionar disponibilidad
   - c. Asignar pedidos
   - d. Monitorear ubicación (soporta ubicaciones textuales)

3. Gestión de rutas
   - a. Definir rutas (waypoints)
   - b. Ajustar dinámicamente (modificar/actualizar ruta en tiempo de ejecución)
   - c. Seguimiento (marcar waypoints alcanzados, estado de la ruta)

4. Monitoreo y tracking
   - a. Visualizar estados (consultas en memoria via `PedidoManager` / fachada)
   - b. Notificar clientes (gestor de notificaciones suscrito a eventos)
   - c. Registrar eventos (bus de eventos y `EventLogger` en memoria)

Módulos clave y responsabilidades:

- `models/pedido.py`: Entidad `Pedido` con máquina de estados, validaciones por canal, acumulador de eventos pendientes y método `flush_events()` para publicar eventos en el `EventBus`.
- `models/repartidor.py`: Entidad `Repartidor` que mantiene asignaciones, ubicación (texto) y estado de ruta.
- `models/route.py`: Modelo `Route` con lista de waypoints, estado y marcado de waypoint alcanzado.
- `factories/PedidoFactory.py`: Normaliza `canal_detalle` según `canal_origen` y crea instancias de `Pedido`.
- `factories/RouteFactory.py`: Crea rutas simples a partir de origen/destino.
- `facades/LogisticaFacade.py`: Orquestador principal. Expone métodos para crear/validar/asignar pedidos, definir e iniciar rutas, avanzar waypoints y marcar entregas.
- `managers/EventBus.py`: Implementa pub/sub central (sin dependencias externas). Soporta publicación síncrona/ordenada cuando se requieren garantías de orden.
- `managers/EventLogger.py`: Suscriptor del bus que registra eventos en memoria (útil para auditoría durante ejecución).
- `managers/NotificationManager.py`: Suscribe a eventos relevantes (`pedido.estado_cambiado`, `pedido.entregado`) y emite notificaciones (por ahora imprime y almacena en memoria).
- `managers/RepartidorManager.py`: Registro y consulta de repartidores, asignación básica (requiere registro explícito).
- `managers/RouteManager.py`: Gestión y seguimiento de rutas asignadas a repartidores.

Patrones de diseño utilizados:

- `Factory Method`: fábricas en `factories/` para instanciar entidades del dominio.
- `Facade`: `LogisticaFacade` encapsula la coordinación entre fábricas, managers y modelos.
- `Decorator`: `decorators/PedidoDecorator.py` permite extender validaciones o priorización sin modificar `Pedido`.
- `Event Bus` / Pub-Sub: desacopla generación de eventos y consumidores (logs, notificaciones).

Aplicación de SOLID (resumen):

- **SRP (Single Responsibility)**: Cada clase tiene una responsabilidad clara — `models/pedido.py` gestiona los datos y la máquina de estados del pedido; `models/repartidor.py` gestiona asignaciones y ubicación; las fábricas (`factories/`) solo crean instancias; la fachada (`facades/LogisticaFacade.py`) coordina.
- **OCP (Open/Closed)**: El uso de decoradores (`decorators/PedidoDecorator.py`) y validadores por canal permite extender reglas y comportamientos (por ejemplo, validaciones adicionales) sin modificar la implementación base de `Pedido`.
- **LSP (Liskov Substitution)**: Se definen interfaces en `interfaces.py` (`IPedido`, `IRepartidor`, `IPedidoFactory`, etc.) para asegurar que implementaciones alternativas puedan sustituir las concretas sin romper contratos.
- **ISP (Interface Segregation)**: Las interfaces están diseñadas pequeñas y específicas (p. ej. `IPedidoFactory` solo expone `crear_pedido`) para evitar que los clientes dependan de métodos que no usan.
- **DIP (Dependency Inversion)**: Módulos de alto nivel (como la fachada) dependen de abstracciones (interfaces de fábricas y managers) en lugar de implementaciones concretas; las dependencias concretas se inyectan vía fábricas y managers.

Ejecución rápida (ejemplo):

```bash
python3 main.py
```

Salida esperada (resumen):

- Repartidor R1 registrado y ubicado en Centro de distribución.
- Flujo de un pedido: Creado → Validado → Asignado → En ruta → Entregado.
- Notificaciones al destinatario en los estados relevantes.
- `EventLogger` contiene una secuencia de eventos que incluye `pedido.estado_cambiado` y `pedido.entregado` (con payload detallado: `tipo_entrega`, `punto_origen`, `canal_detalle`).

Pruebas manuales y verificación:

- El archivo `main.py` incluye un flujo de ejemplo que crea un `Pedido`, registra un `Repartidor` (`R1`), crea una `Route`, avanza la ruta y muestra logs/notificaciones.

---

## Entregable 2 — Servicio web y frontend

Para esta parte del proyecto se agregó una capa de servicio web sobre el dominio que ya existía, sin tocar nada de lo anterior. La idea era exponer el sistema como una API REST y construir un frontend que la consuma.

### Estructura nueva

El proyecto quedó dividido en dos carpetas principales:

- `backend/` — todo lo de Python: el dominio del E1 más los controllers, services y repositories nuevos
- `frontend/` — aplicación Next.js que consume la API

Dentro de `backend/src/` está la lógica del servicio web organizada en tres capas:

- `controllers/` reciben los requests HTTP y responden JSON, sin lógica de negocio
- `services/` orquestan los casos de uso, son los únicos que hablan con la fachada
- `repositories/` envuelven los managers del E1 para que los services no dependan de cómo está implementado el almacenamiento

### Decisiones de arquitectura

Se eligió arquitectura en capas en vez de microservicios principalmente porque el dominio completo vive en memoria y los managers comparten estado. Separar eso en servicios distintos hubiera obligado a meter una base de datos o un broker de mensajes, lo que estaba fuera del alcance. Con capas se mantiene todo simple y funcional.

El frontend es un cliente separado en Next.js que hace fetch directamente desde el navegador. Se habilitó CORS en el backend para permitir eso. Se descartó usar Server-Side Rendering con llamadas al backend desde el servidor de Next.js porque así no se vería el flujo cliente-servidor en las DevTools del browser, que es justamente lo que se quería demostrar.

En cuanto a serverless, `NotificationManager` y `EventLogger` son los dos componentes que técnicamente podrían correr como funciones en la nube (se activan por evento, hacen algo corto y terminan). Sin embargo, como todo el estado está en memoria, moverlos a serverless no tiene sentido sin antes agregar persistencia externa. Por eso se dejaron como están.

### Cómo correr el proyecto

**Backend** (desde la carpeta `backend/`):

```bash
cd backend
pip install -r requirements.txt
python src/app.py
```

Queda corriendo en `http://localhost:3000`.

**Frontend** (desde la carpeta `frontend/`):

```bash
cd frontend
npm install
npm run dev
```

Queda corriendo en `http://localhost:3001`.

El flujo de prueba básico es: crear un pedido desde la página de Pedidos, validarlo, registrar un repartidor, asignarlo al pedido, definir una ruta y avanzar waypoints. El estado se puede seguir en tiempo real desde la página de Tracking.

---

## Entregable 3 — Arquitectura Tecnológica e Integración

Este entregable no agrega servicios nuevos. La arquitectura propuesta para producción (SQL/NoSQL, Redis, API Gateway) está documentada en `entregable3_presentacion.txt`. Lo que sigue describe cómo ejecutar los casos de uso y dónde se evidencian las decisiones tecnológicas en el código.

### Tecnologías implementadas

Las dos tecnologías del curso efectivamente implementadas son el **Event Bus en memoria** (tópico pub/sub) y la **API REST**.

El Event Bus es lo más interesante de ver: cuando un pedido cambia de estado, `Pedido.flush_events()` publica el evento en el bus y tanto `NotificationManager` como `EventLogger` lo reciben en paralelo sin que el modelo los conozca directamente. Es el patrón tópico funcionando: un evento, múltiples consumidores, sin acoplamiento entre ellos. El `publish()` soporta `blocking=True` para cuando el orden importa (simula cola) y modo async por defecto para fan-out.

Los archivos relevantes son `managers/EventBus.py` (el bus en sí), `managers/NotificationManager.py` y `managers/EventLogger.py` (los dos suscriptores), y `models/pedido.py` con `flush_events()` en la línea 159.

Para verlo sin levantar el servidor:

```bash
cd backend
python main.py
```

La salida muestra cómo ambos suscriptores reaccionan al mismo `pedido.estado_cambiado` de forma independiente.

La API REST está en `backend/src/controllers/`, dividida en cuatro blueprints (uno por caso de uso), y el frontend la consume desde `frontend/lib/api.ts`.

### Cómo ejecutar los casos de uso

El flujo completo se puede seguir desde el frontend en `http://localhost:3001`, o directamente con curl contra `http://localhost:3000`.

**Gestión de pedidos** — `http://localhost:3001/pedidos`

```bash
# crear pedido
curl -X POST http://localhost:3000/api/v1/pedidos \
  -H "Content-Type: application/json" \
  -d '{"origen": {"direccion": "Bodega Central", "id_punto_origen": "B1"}, "destino": {"direccion": "Av. Siempre Viva 742", "nombre_destinatario": "Juan", "medio_contacto": "email"}, "tipo_entrega": "normal", "canal_origen": "web", "tipo_carga": "paquete", "peso_volumen": "2kg"}'

# validar y asignar (reemplazar <id> con el id retornado)
curl -X POST http://localhost:3000/api/v1/pedidos/<id>/validar
curl -X POST http://localhost:3000/api/v1/pedidos/<id>/asignar \
  -H "Content-Type: application/json" -d '{"repartidor_id": "R1"}'
```

**Gestión de repartidores** — `http://localhost:3001/repartidores`

```bash
curl -X POST http://localhost:3000/api/v1/repartidores \
  -H "Content-Type: application/json" \
  -d '{"id": "R1", "capacidad": 10, "ubicacion": "Centro de distribución"}'
```

**Gestión de rutas** — `http://localhost:3001/rutas`

```bash
curl -X POST http://localhost:3000/api/v1/rutas \
  -H "Content-Type: application/json" \
  -d '{"id": "RUTA-1", "repartidor_id": "R1", "waypoints": [{"address": "Punto A"}, {"address": "Av. Siempre Viva 742"}]}'

curl -X POST http://localhost:3000/api/v1/rutas/RUTA-1/iniciar
curl -X POST http://localhost:3000/api/v1/rutas/RUTA-1/waypoint
```

**Monitoreo y tracking** — `http://localhost:3001/tracking`

```bash
curl http://localhost:3000/api/v1/tracking/<id>
curl http://localhost:3000/api/v1/tracking/<id>/notificaciones
```

El endpoint `/notificaciones` retorna lo que `NotificationManager` fue acumulando a medida que llegaban eventos del bus. El controller de tracking no sabe nada de ese proceso, lo que evidencia el desacoplamiento de la integración asíncrona.
