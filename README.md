# Proyecto Logística (arquitectura y patrones)

Estructura organizada por patrones de diseño para la entrega del ramo.

Estructura principal:

- `models/`: Entidades del dominio (`pedido.py`, `repartidor.py`).
- `factories/`: `PedidoFactory`, `RepartidorFactory` (Factory Method).
- `decorators/`: Decoradores para `Pedido` (Decorator).
- `facades/`: `LogisticaFacade` (Facade).
- `main.py`: Ejecutor de ejemplo.

Casos de uso implementados:

- Crear pedido: creación de pedidos desde un canal (fábrica + `models.pedido`).
- Validar pedido: validación de campos mínimos y reglas operativas (`models.pedido.validar`).
- Registrar repartidor: creación y registro de repartidores (`factories.RepartidorFactory` + `models.repartidor`).
- Asignar pedido: asignación de pedido a repartidor (fachada coordina validación y asignación).

Patrones de diseño utilizados:

- `Factory Method`: en `factories/` para centralizar creación de `Pedido` y `Repartidor`.
- `Decorator`: en `decorators/PedidoDecorator.py` para extender comportamiento de validación/prioridad sin modificar la clase base.
- `Facade`: en `facades/LogisticaFacade.py` para simplificar y coordinar interacciones entre subsistemas.

Aplicación de SOLID (resumen):

- **SRP (Single Responsibility)**: `Pedido` gestiona datos/estado del pedido; `Repartidor` gestiona asignaciones; fábricas solo crean instancias; la fachada coordina.
- **OCP (Open/Closed)**: El uso de decoradores permite extender validaciones/comportamientos sin modificar `Pedido`.
- **LSP (Liskov Substitution)**: `Pedido` y `Repartidor` implementan interfaces (`interfaces.py`) que garantizan que sus sustitutos mantengan el contrato.
- **ISP (Interface Segregation)**: Se definieron interfaces pequeñas (`IPedido`, `IRepartidor`, `IPedidoFactory`, `IRepartidorFactory`) para no forzar a las clases a depender de métodos que no usan.
- **DIP (Dependency Inversion)**: La fachada depende de abstracciones de fábricas (`IPedidoFactory`, `IRepartidorFactory`) en lugar de implementaciones concretas.

Ejecución rápida:

```bash
python3 main.py
```

Salida esperada:

- `Pedido 123 estado: Asignado, repartidor: R1`

