from models.route import Route


class RouteFactory:
    @staticmethod
    def crear_ruta(id, waypoints=None, metadata=None):
        return Route(id, waypoints=waypoints, metadata=metadata)
