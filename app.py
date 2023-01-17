import os
from flask import Flask, send_file, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, Protector, Walkee, Requests

app = Flask(__name__, static_folder='public')
CORS(app, origins=['*'])
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

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

@app.post('/protectors')
def create_protector():
    data = request.json
    protector = Protector(data['first_name'], data['last_name'], data['email'])
    print (data)
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


@app.patch('/walkees/<int:id>')
def update_walkee(id):
    data = request.json
    walkee = Walkee.query.get(id)
    walkee.first_name = data['first_name']
    walkee.last_name = data['last_name']
    walkee.email = data['email']
    db.session.commit()
    return jsonify(walkee.to_dict()), 201


@app.get('/all_requests')
def all_requests():
    requests = Requests
    if requests:
        return jsonify(requests.to_dict()), 201
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
    request.completed = data['completed'] #see if boolean is a 1 or a 0
    request.current = data['current']  # see if boolean is a 1 or a 0
    db.session.add(request)
    db.session.commit()
    return jsonify(request.to_dict()), 201

@app.post('/create_requests')
def create_requests():
    data = request.json
    request = Requests(data['start_location'], data['end_location'], data['datetime'], data['message'], data['completed'], data['current'])
    print(data)
    db.session.add(request)
    db.session.commit()
    return jsonify(request.to_dict()), 201

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=os.environ.get('PORT', 3000))