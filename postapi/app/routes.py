def register_routes(api, app, root='api'): 
    from .posts import register_route as attach_posts
    from .up import register_route as attach_health
    from .api.auth import register_route as attach_auth

    attach_posts(api, app, root)
    attach_health(api, app, root)
    attach_auth(api, app, root)
