from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    return {'project':'cyplp.timelapse_commander'}
