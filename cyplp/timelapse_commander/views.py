from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import zmq

import couchdbkit
from couchdbkit.designer import push

from model import StorageFile

context = zmq.Context()

# server object
server = couchdbkit.Server()

# create database
db = server.get_or_create_db('timelapse')
StorageFile.set_db(db)

push('couchdb/_design/storagefile', db)

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):

    return {'project':'cyplp.timelapse_commander'}

@view_config(route_name='controls', renderer='templates/controls.pt')
def controls(request):
    orderEmetter = context.socket(zmq.REQ)
    orderEmetter.connect("tcp://127.0.0.1:5559")  # TODO timeout

    orderEmetter.send_json({'command': 'status'})
    status = orderEmetter.recv_json()

    return {'status': status}

@view_config(route_name='launch', renderer='json')
def launch(request):
    # TODO get params
    orderEmetter = context.socket(zmq.REQ)
    orderEmetter.connect("tcp://127.0.0.1:5559")  # TODO timeout

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
    orderEmetter = context.socket(zmq.REQ)
    orderEmetter.connect("tcp://127.0.0.1:5559")  # TODO timeout

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
    allBatch = StorageFile.view('batchpy/pyall', group=True)
    batches = allBatch.all()
    return {'batches': batches}

@view_config(route_name='batch', renderer='templates/batch.pt')
def batch(request):

    images =  db.view('plop/all', key=request.matchdict['name']).all()
    print images
    return {'name': request.matchdict['name'],
            'images': [image['value'] for image in images]}
