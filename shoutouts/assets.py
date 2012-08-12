from webassets import Bundle

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

app_coffee = Bundle(
    'assets/app/coffee/*.coffee',
    filters='coffeescript,uglifyjs',
    output='js/app.js',
    debug=False,
)



def includeme(config):

    config.add_webasset('bootstrap_css', bootstrap_css)
    config.add_webasset('bootstrap_js', bootstrap_js)
    config.add_webasset('jquery_js', jquery_js)
    config.add_webasset('app_coffee', app_coffee)

    # integrate webassets with jinja2

    config.add_jinja2_extension('webassets.ext.jinja2.AssetsExtension')
    jinja2_env = config.get_jinja2_environment()
    jinja2_env.assets_environment = config.get_webassets_env()


