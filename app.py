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

@app.post('/protector')
def create_protector():
    data = request.form
    protector = Protector(data['first_name'], data['last_name'], data['email'])
    print (data)
    db.session.add(protector)
    db.session.commit()
    return jsonify(protector.to_dict()), 201

@app.post('/walkee')
def create_walkee():
    data = request.form
    walkee = Walkee(data['first_name'], data['last_name'], data['email'])
    print(data)
    db.session.add(walkee)
    db.session.commit()
    return jsonify(walkee.to_dict()), 201


@app.get('/walkee/<int:id>')
def show_walkee(id):
    walkee = Walkee.query.get(id)
    if walkee:
        return jsonify(walkee.to_dict())
    else:
        return {}, 404


@app.get('/protector/<int:id>')
def show_protector(id):
    protector = Protector.query.get(id)
    if protector:
        return jsonify(protector.to_dict())
    else:
        return {}, 404



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=os.environ.get('PORT', 3000))