from pyramid.config import Configurator
from webassets import Bundle
from mongoengine import connect


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # webassets

    bootstrap_css = Bundle(
        'assets/bootstrap/css/*.css',
        filters='cssmin',
        output='css/bootstrap.css',
        debug=False,
    )

    bootstrap_js = Bundle(
        'assets/bootstrap/js/*.js',
        filters='uglifyjs',
        output='js/bootstrap.js',
        debug=False,
    )

    jquery_js = Bundle(
        'assets/jquery/*.js',
        filters='uglifyjs',
        output='js/jquery.js',
        debug=False,
    )

    config.add_webasset('bootstrap_css', bootstrap_css)
    config.add_webasset('bootstrap_js', bootstrap_js)
    config.add_webasset('jquery_js', jquery_js)

    # integrate webassets with jinja2

    config.add_jinja2_extension('webassets.ext.jinja2.AssetsExtension')
    jinja2_env = config.get_jinja2_environment()
    jinja2_env.assets_environment = config.get_webassets_env()

    # mongoengine
    connect(settings['db_name'])
    
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('main', '/')
    config.add_route('submit', '/submit/')

    config.scan()
    return config.make_wsgi_app()
