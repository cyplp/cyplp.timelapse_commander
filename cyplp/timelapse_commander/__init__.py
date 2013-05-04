from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('controls', '/controls')
    config.add_route('batchs', '/batchs')

    config.include('rebecca.fanstatic')
    config.add_fanstatic_resources(['js.bootstrap.bootstrap'], r'.*\.pt')

    config.scan()
    return config.make_wsgi_app()
