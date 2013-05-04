from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

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

@view_config(route_name='launch', renderer='json')
def launch(request):
    # TODO get params

    orderEmetter.send_json({'command': 'start',
                        'interval': 1,
                        'filename': 'tmp/crnnwaza3%d.nef',
                        'batch': "testCoucdb"})

    orderEmetter.send_json({'command': 'status'})

    ack = orderEmetter.recv_json()

    if ack == 'ack':
        request.session.flash({"status": 'alert-success',
                               'message' : "Job launched"})
    else:
        request.session.flash({"status": 'alert-error',
                               'message' : "Job failed"})

    raise HTTPFound(request.route_path('controls'))

@view_config(route_name='stop', renderer='json')
def stop(request):
    orderEmetter.send_json({'command': 'stop',})
    ack = orderEmetter.recv_json()

    if ack == 'ack':
        request.session.flash({"status": 'alert-success',
                               'message' : "Job stop"})
    else:
        request.session.flash({"status": 'alert-error',
                               'message' : "Job failed"})

    raise HTTPFound(request.route_path('controls'))


@view_config(route_name='batchs', renderer='templates/batchs.pt')
def batchs(request):
    return {}
