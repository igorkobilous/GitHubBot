from .core import Controller
from .controllers import SearchController


_routes = {
    'search': SearchController
}


def get_controller_cls(value):
    controller_cls = _routes.get(value)

    if controller_cls is None:
        raise Exception
    elif not issubclass(controller_cls, Controller):
        raise Exception

    return controller_cls
