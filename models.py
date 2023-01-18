from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import relationship

db = SQLAlchemy()
migrate = Migrate(db)


class Protector(db.Model):
    # this is the migration part
    __tablename__ = 'protectors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))  # nullable=False
    last_name = db.Column(db.String(80))  # nullable=False
    email = db.Column(db.String(120), unique=True)  # nullable=False
    # password = db.Column(db.String(120))  # nullable=False
    # picture = db.Column(db.String, unique=True)  # nullable=False
    # phone_number = db.Column(db.String, unique=True)  # nullable=False
    # gender_identity = db.Column(db.String)
    # address = db.Column(db.String)  # nullable=False
    # background_check = db.Column(db.Boolean )
    # active = db.Column(db.Boolean, default=False)
    # requests = db.relationship('Requests', backref='protector', lazy=True)
    # created_at = db.Column(db.DateTime, server_default=db.func.now())
    # updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # this is basic python classes
    # Here is where we whitelist what can be set on create by a user client
    # , password, picture, phone_number, gender_identity, address, active
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        # self.password = password
        # self.picture = picture
        # self.phone_number = phone_number
        # self.gender_identity = gender_identity
        # self.address = address
        # self.active = active
        #

    def to_dict(self):  # this is how we serialize (similar to_json)
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            # 'password': self.password,
            # 'picture': self.picture,
            # 'phone_number': self.phone_number,
            # 'gender_identity': self.gender_identity,
            # 'address': self.address,
            # 'active': self.active
            # 'requests':[request.to_dict() for request in Requests.query.filter_by(protector_id=self.id)]

        }

    def __repr__(self):
        return '<Protector %r>' % self.first_name


class Walkee(db.Model):
    __tablename__ = 'walkees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))  # nullable=False
    last_name = db.Column(db.String(80))  # nullable=False
    email = db.Column(db.String(120), unique=True)  # nullable=False
    # password = db.Column(db.String(120))  # nullable=False
    # picture = db.Column(db.String)  # nullable=False
    # phone_number = db.Column(db.String, unique=True)  # nullable=False
    # gender_identity = db.Column(db.String)
    # requests = db.relationship('Requests', backref='walkee', lazy=True)
    # created_at = db.Column(db.DateTime, server_default=db.func.now())
    # updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # , password, picture, phone_number, gender_identity
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        # self.password = password
        # self.picture = picture
        # self.phone_number = phone_number
        # self.gender_identity = gender_identity

    def to_dict(self):  # this is how we serialize (similar to_json)
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            # 'email': self.email,
            # 'password': self.password,
            # 'picture': self.picture,
            # 'phone_number': self.phone_number,
            # 'gender_identity': self.gender_identity
            # 'requests':[request.to_dict() for request in Requests.query.filter_by(walkee_id=self.id)]
        }

    def __repr__(self):
        return 'Walkee %r' % self.first_name


class Requests(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    walkee_id = db.Column(db.Integer)  # , db.ForeignKey('walkees.id')
    protector_id = db.Column(db.Integer)  # , db.ForeignKey('protectors.id')
    date = db.Column(db.String(1000))
    time = db.Column(db.String(1000))
    message = db.Column(db.String(1000))
    start_location = db.Column(db.String(1000), nullable=False)
    end_location = db.Column(db.String(1000), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    current = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # , protector_id, walkee_id
    def __init__(self, start_location, end_location, date, time, message, completed, current, active):
        self.start_location = start_location
        self.end_location = end_location
        self.date = date
        self.time = time
        self.message = message
        self.completed = completed
        self.current = current
        self.active = active
        # self.protector_id = protector_id
        # self.walkee_id = walkee_id

    def to_dict(self):  # this is how we serialize (similar to_json)
        return {
            'id': self.id,
            'start_location': self.start_location,
            'end_location': self.end_location,
            'date': self.date,
            'time': self.time,
            'message': self.message,
            'completed': self.completed,
            'current': self.current,
            'active': self.active
            # 'protector_id': self.protector_id,
            # 'walkee_id': self.walkee_id
        }

    def __repr__(self):
        return 'Requests %r' % self.start_location
