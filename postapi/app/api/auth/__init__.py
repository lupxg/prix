BASE_ROUTE = 'auth'

def register_route(api, app, root='api'):
    from .endpoint import api as authapi

    api.add_namespace(authapi, path=f'/{root}/{BASE_ROUTE}') 
