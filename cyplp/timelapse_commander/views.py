import urllib2

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from pyramid.response import FileIter

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
                        'interval': int(request.POST['interval']),
                        'filename': request.POST['fileName'],
                        'batch': request.POST['batchName']})

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
    return {'name': request.matchdict['name'],
            'images': [image['value'] for image in images]}


@view_config(route_name='image')
def image(request):
    print  request.matchdict['id']
    url = 'http://localhost:5984/timelapse/%s/doc.jpg' % request.matchdict['id']
    print url

    # import rpdb
    # rpdb.set_trace()

    req = urllib2.urlopen(url)
    # tmp = req.read()
    response = request.response
    response.content_type = 'image/jpeg'
    response.app_iter = FileIter(req)
    return response
