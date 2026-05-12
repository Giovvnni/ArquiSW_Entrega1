import sys
import os

# Agrega la raíz del proyecto al path para imports del dominio (factories, facades, etc.)
# y el directorio src/ para imports locales (repositories, services, controllers)
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ROOT)
sys.path.insert(0, _SRC)

from flask import Flask
from flask_cors import CORS

from factories.PedidoFactory import PedidoFactory
from factories.RepartidorFactory import RepartidorFactory
from factories.RouteFactory import RouteFactory
from facades.LogisticaFacade import LogisticaFacade

from repositories.pedido_repository import PedidoRepository
from repositories.repartidor_repository import RepartidorRepository
from repositories.ruta_repository import RutaRepository
from services.pedido_service import PedidoService
from services.repartidor_service import RepartidorService
from services.ruta_service import RutaService
from services.tracking_service import TrackingService
from controllers.pedido_controller import create_pedido_bp
from controllers.repartidor_controller import create_repartidor_bp
from controllers.ruta_controller import create_ruta_bp
from controllers.tracking_controller import create_tracking_bp


def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3001"])

    # Instancia compartida del dominio (todo el estado en memoria queda aquí)
    facade = LogisticaFacade(PedidoFactory, RepartidorFactory, route_factory=RouteFactory)

    # Repositories: envuelven los managers del E1
    pedido_repo = PedidoRepository(facade.pedido_manager)
    repartidor_repo = RepartidorRepository(facade.repartidor_manager)
    ruta_repo = RutaRepository(facade.route_manager)

    # Services: orquestan los casos de uso
    pedido_service = PedidoService(facade, pedido_repo)
    repartidor_service = RepartidorService(facade, repartidor_repo, pedido_repo)
    ruta_service = RutaService(facade, ruta_repo)
    tracking_service = TrackingService(facade)

    # Controllers: presentación HTTP — solo reciben request y delegan al service
    app.register_blueprint(create_pedido_bp(pedido_service, repartidor_service))
    app.register_blueprint(create_repartidor_bp(repartidor_service))
    app.register_blueprint(create_ruta_bp(ruta_service))
    app.register_blueprint(create_tracking_bp(tracking_service))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000, debug=True)
