from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from pyramid_beaker import set_cache_regions_from_settings

def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    sessionFactory = session_factory_from_settings(settings)
    set_cache_regions_from_settings(settings)

    config = Configurator(settings=settings)
    config.set_session_factory(sessionFactory)

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')

    config.add_route('controls', '/controls')
    config.add_route('launch', '/controls/launch')
    config.add_route('stop', '/controls/stop')

    config.add_route('batchs', '/batchs')
    config.add_route('batch', '/batch/{name}')

    config.add_route('image', '/image/{id}.jpg')
    config.include('rebecca.fanstatic')
    config.add_fanstatic_resources(['js.bootstrap.bootstrap'], r'.*\.pt')

    config.scan()
    return config.make_wsgi_app()
