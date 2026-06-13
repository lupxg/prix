BASE_ROUTE = 'up'

def register_route(api, app, root='api'):
    from .controller import api as healthapi

    api.add_namespace(healthapi, path=f'/{root}/{BASE_ROUTE}') 
