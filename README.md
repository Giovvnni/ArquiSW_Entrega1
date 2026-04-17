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




