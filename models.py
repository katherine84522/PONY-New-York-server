from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db)

class Protector(db.Model):
    # this is the migration part
    __tablename__ = 'protectors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    picture = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, unique=True, nullable=False)
    gender_identity = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer)
    address = db.Column(db.String, nullable=False)
    zone_id = db.Column(db.Integer, nullable=False)
    background_check = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # this is basic python classes
    # Here is where we whitelist what can be set on create by a user client
    def __init__(self, first_name, last_name, email, password, picture, phone_number, gender_identity, address, active):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.picture = picture
        self.phone_number = phone_number
        self.gender_identity = gender_identity
        self.address = address
        self.active = active      

    def __repr__(self):
        return '<User %r>' % self.username

class Walkee(db.Model):
    __tablename__ = 'walkees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    picture = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, unique=True, nullable=False)
    gender_identity = db.Column(db.String, nullable=False)

    def __init__(self, first_name, last_name, email, password, picture, phone_number, gender_identity):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.picture = picture
        self.phone_number = phone_number
        self.gender_identity = gender_identity


class Current_Requests(db.Model):
    __tablename__ = 'current_requests'
    id = db.Column(db.Integer, primary_key=True)
    walkee_id = db.Column(db.Integer)
    protector_id = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    message = db.Column(db.String(1000))
    start_location = db.Column(db.String(1000), nullable=False)
    end_location = db.Column(db.String(1000), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, start_location, end_location, message):
        self.start_location = start_location
        self.end_location = end_location
        self.message = message


class Future_Requests(db.Model):
    __tablename__ = 'future_requests'
    id = db.Column(db.Integer, primary_key=True)
    walkee_id = db.Column(db.Integer)
    protector_id = db.Column(db.Integer)
    message = db.Column(db.String(1000))
    start_location = db.Column(db.String(1000), nullable=False)
    end_location = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.String(150), nullable=False)
    time = db.Column(db.String(150), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, start_location, end_location, message, date, time):
        self.start_location = start_location
        self.end_location = end_location
        self.message = message
        self.date = date
        self.time = time

class Zone(db.Model):
    __tablename__ = 'zone'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))

    def __init__(self, name):
        self.name = name
         



