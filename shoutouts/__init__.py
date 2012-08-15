from pyramid.config import Configurator

from pyramid_beaker import session_factory_from_settings

    
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # sessions
    config.set_session_factory(session_factory_from_settings(settings))

    # models
    config.include('shoutouts.models')

    # security
    config.include('shoutouts.auth')

    # webassets
    config.include('shoutouts.assets')

    # routes
    config.include('shoutouts.routes')
    
    config.scan()

    return config.make_wsgi_app()
