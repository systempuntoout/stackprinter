import app.lib.key as keys


def webapp_add_wsgi_middleware(app):
    from engineauth import middleware
    return middleware.AuthMiddleware(app)


engineauth = {
    'secret_key': keys.auth_secret
}


engineauth['provider.stackexchange'] = {
    'class_path': 'engineauth.strategies.stackexchange.StackExchangeStrategy',
    'client_id': keys.client_id,
    'client_secret': keys.client_secret,
    'scope': '',
    }


