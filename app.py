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

# @app.route('/protectors')
# def create_protector():
#     if request.method == "POST":
#         create_protector = create_protector(
#             first_name = request.form['first_name'],
#             last_name = request.form['last_name'],
#             email = request.form['email']
#         )
#         db.session.add(create_protector)
#         db.session.commit()
#         return jsonify(create_protector.to_dict()), 201

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
    data = request.form
    request = Requests.query.get(id)
    # request = data['completed']
    request.completed = data['completed']
    request.current = data['current']
    db.session.add(request)
    db.session.commit()
    return jsonify(request.to_dict()), 201

@app.post('/create_requests')
def create_requests():
    data = request.form
    request = Requests(data['start_location'], data['end_location'], data['datetime'], data['message'], data['completed'], data['current'])
    print(data)
    db.session.add(request)
    db.session.commit()
    return jsonify(request.to_dict()), 201


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=os.environ.get('PORT', 3000))