import os
from flask import Flask, send_file, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, Protector, Walkee, Requests
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='public')
CORS(app, origins=['*'])
app.config.from_object(Config)
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
            # token = create_access_token(identity=protector.id)
            return jsonify({'protector': protector.to_dict(), 'token': token})
        else:
            return jsonify({'error': 'invalid password'}), 422


@app.post('/protectors')
def create_protector():
    data = request.json
    protector = Protector(data['first_name'], data['last_name'], data['email'])
    print(data)
    db.session.add(protector)
    db.session.commit()
    return jsonify(protector.to_dict()), 201


@app.patch('/protectors/<int:id>')
def update_protector(id):
    data = request.json
    protector = Protector.query.get(id)
    protector.first_name = data['first_name']
    protector.last_name = data['last_name']
    protector.email = data['email']
    db.session.commit()
    return jsonify(protector.to_dict()), 201


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
    walkee = Walkee(data['first_name'], data['last_name'], data['email'])
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
            # token = create_access_token(identity=walkee.id)
            return jsonify({'walkee': walkee.to_dict(), 'token': token})
        else:
            return jsonify({'error': 'invalid password'}), 422


@app.patch('/walkees/<int:id>')
def update_walkee(id):
    data = request.json
    walkee = Walkee.query.get(id)
    walkee.first_name = data['first_name']
    walkee.last_name = data['last_name']
    walkee.email = data['email']
    db.session.commit()
    return jsonify(walkee.to_dict()), 201


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
    request = Requests.query.get(id)
    # request = data['completed']
    request.completed = data['completed']  # see if boolean is a 1 or a 0
    request.current = data['current']  # see if boolean is a 1 or a 0
    db.session.add(request)
    db.session.commit()
    return jsonify(request.to_dict()), 201


@app.post('/requests')
def create_requests():
    data = request.json
    reqs = Requests(data['start_location'], data['end_location'], data['date'],
                    data['time'], data['message'], data['completed'], data['current'])
    # print(data)
    db.session.add(reqs)
    db.session.commit()
    return jsonify(reqs.to_dict()), 201


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
