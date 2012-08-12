
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('main', '/')
    config.add_route('login', '/login/')
    config.add_route('logout', '/logout/')
    config.add_route('signup', '/signup/')
    config.add_route('submit', '/submit/')


