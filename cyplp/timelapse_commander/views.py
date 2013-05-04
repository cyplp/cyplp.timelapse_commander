from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {'project':'cyplp.timelapse_commander'}

@view_config(route_name='controls', renderer='templates/controls.pt')
def controls(request):
    return {}

@view_config(route_name='batchs', renderer='templates/batchs.pt')
def batchs(request):
    return {}
