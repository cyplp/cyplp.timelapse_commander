from pyramid.view import view_config

import zmq

context = zmq.Context()

orderEmetter = context.socket(zmq.REQ)
orderEmetter.connect("tcp://127.0.0.1:5559")  # TODO timeout

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {'project':'cyplp.timelapse_commander'}

@view_config(route_name='controls', renderer='templates/controls.pt')
def controls(request):
    orderEmetter.send_json({'command': 'status'})
    status = orderEmetter.recv_json()

    return {'status': status}

@view_config(route_name='batchs', renderer='templates/batchs.pt')
def batchs(request):
    return {}
