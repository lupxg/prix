BASE_ROUTE = 'posts'

def register_route(api, app, root='api'):
    from .endpoint import api as postapi

    api.add_namespace(postapi, path=f'/{root}/{BASE_ROUTE}') 
