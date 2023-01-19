import os
from flask import Flask, send_file, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, Protector, Walkee, Requests
import platform
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit
import sys


app = Flask(__name__, static_folder='public')
CORS(app, origins=['*'])
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins='*')


@app.get('/')
def home():
    return send_file('welcome.html')


@app.get('/example')
def example():
    return {'message': 'Your app is running python'}


@app.get('/protectors/<int:id>')
def show_protector(id):
    protector = Protector.query.get(id)
    if protector:
        return jsonify(protector.to_dict())
    else:
        return {}, 404


@app.post('/protector_login')
def pro_login():
    data = request.json
    protector = Protector.query.filter_by(email=data['email']).first()
    if not protector:
        return jsonify({'error': 'no account found'}), 404
    else:
        given_password = data['password']
        if protector.password == given_password:
            # authenticate the protector
            token = create_access_token(identity=protector.id)
            return jsonify({'protector': protector.to_dict(), 'token': token})
        else:
            return jsonify({'error': 'invalid password'}), 422


@app.post('/protectors')
def create_protector():
    data = request.json
    protector = Protector(data['first_name'], data['last_name'], data['email'], data['password'], data['picture'],  data['phone_number'], data['gender_identity'], data['address'])
    # add to above: 
    print(data)
    db.session.add(protector)
    db.session.commit()
    return jsonify(protector.to_dict()), 201


@app.patch('/protectors/<int:id>')
def update_protector(id):
    data = request.json
    protector = Protector.query.get(id)
    for key, value in data.items():
        setattr(protector, key, value)
    # protector.first_name = data['first_name']
    # protector.last_name = data['last_name']
    # protector.email = data['email']
    # protector.password = data['password']
    # protector.picture= data['picture']
    # protector.phone_number = data['phone_number']
    # protector.gender_identity = data['gender_identity']
    # protector.address = data['address']
    db.session.commit()
    return jsonify(protector.to_dict()), 201


@app.delete('/protectors/<int:id>')
# @jwt_required()
def delete_protector(id):
    protector = Protector.query.get(id)
    if protector:
        db.session.delete(protector)
        db.session.commit()
        # current_protector = get_jwt_identity()
        print('Deleting protector successfully...')
        return jsonify(protector.to_dict)
    else:
        return {'error': 'No protector found, soz'}, 404


@app.get('/walkees/<int:id>')
def show_walkee(id):
    walkee = Walkee.query.get(id)
    if walkee:
        return jsonify(walkee.to_dict())
    else:
        return {}, 404


@app.post('/walkees')
def create_walkee():
    data = request.json
    walkee = Walkee(data['first_name'], data['last_name'], data['email'], data['password'],
                    data['picture'],  data['phone_number'], data['gender_identity'])
    # add to above: 
    print(data)
    db.session.add(walkee)
    db.session.commit()
    return jsonify(walkee.to_dict()), 201


@app.post('/walkee_login')
def walkee_login():
    data = request.json
    walkee = Walkee.query.filter_by(email=data['email']).first()
    if not walkee:
        return jsonify({'error': 'no account found'}), 404
    else:
        given_password = data['password']
        if walkee.password == given_password:
            # authenticate the walkee
            token = create_access_token(identity=walkee.id)
            return jsonify({'walkee': walkee.to_dict(), 'token': token})
        else:
            return jsonify({'error': 'invalid password'}), 422


@app.patch('/walkees/<int:id>')
def update_walkee(id):
    data = request.json
    print(request.values, file=sys.stderr)
    walkee = Walkee.query.get(id)
    for key, value in data.items(): 
        setattr(walkee, key, value)
        # walkee[key] = value
    #walkee.first_name = data['first_name']
   #walkee.last_name = data['last_name'] if data['last_name'] else None
    #walkee.email = data['email']
    
    # walkee.password = data['password']
    # walkee.picture= data['picture']
    # walkee.phone_number = data['phone_number']
    # walkee.gender_identity = data['gender_identity']
    db.session.commit()
    return jsonify(walkee.to_dict()), 201


@app.delete('/walkees/<int:id>')
# @jwt_required()
def delete_walkee(id):
    walkee = Walkee.query.get(id)
    if walkee:
        db.session.delete(walkee)
        db.session.commit()
        # current_walkee = get_jwt_identity()
        print('Deleting walkee successfully...')
        return jsonify(walkee.to_dict)
    else:
        return {'error': 'No walkee found'}, 404


@app.get('/requests')
def all_requests():
    requests = Requests.query.all()
    if requests:
        return jsonify([r.to_dict() for r in requests]), 201
    else:
        return {}, 404


@app.get('/requests/<int:id>')
def get_requests(id):
    request = Requests.query.get(id)
    if request:
        return jsonify(request.to_dict()), 201
    else:
        return {}, 404

@app.patch('/requests/<int:id>')
def update_requests(id):
    data = request.json
    req = Requests.query.get(id)

    # if data['protector_id']:
    #     req.protector_id = data['protector_id']
    for key, value in data.items():
        setattr(req, key, value)
    db.session.add(req)
    db.session.commit()
    return jsonify(req.to_dict()), 201

    # if the request has been started then active becomes true && the protector_id is assigned by the protector who is logged in
    # if a request has been completed, then the completed needs to be turned true (from the onclick on the front end)
    # if req.include
    # request = data['completed']
    # req.completed = data['completed'] 
    # req.active = data['active'] # see if boolean is a 1 or a 0

@app.post('/requests')
def create_requests():
    data = request.json
    reqs = Requests(data['start_location'], data['end_location'], data['date'],
                    data['time'], data['message'], data['completed'], data['current'], data['active'], data['walkee_id'])
    # print(data)
    db.session.add(reqs)
    db.session.commit()
    return jsonify(reqs.to_dict()), 201


@app.delete('/requests/<int:id>')
def delete_request(id):
    req = Requests.query.get(id)
    if req:
        db.session.delete(req)
        db.session.commit()
        print('Deleting req successfully...')
        return jsonify(req.to_dict)
    else:
        return {'error': 'No request found'}, 404


@socketio.on('connect')
def connected():
    '''This function is an event listener that gets called when the client connects to the server'''
    print(f'Client {request.sid} has connected')
    emit('connect', {'data': f'id: {request.sid} is connected'})


@socketio.on('data')
def handle_message(data):
    '''This function runs whenever a client sends a socket message to be broadcast'''
    print(f'Message from Client {request.sid} : ', data)
    emit('data', {'data': 'data', 'id': request.sid}, broadcast=True)


@socketio.on("disconnect")
def disconnected():
    '''This function is an event listener that gets called when the client disconnects from the server'''
    print(f'Client {request.sid} has disconnected')
    emit('disconnect',
         f'Client {request.sid} has disconnected', broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.environ.get('PORT', 3000))
