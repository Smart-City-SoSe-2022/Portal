import json.encoder
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import pika
from dotenv import dotenv_values
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

config = dotenv_values(".env")
app.config['SQLALCHEMY_DATABASE_URI'] = config["DB_FULL_URI"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config["JWT_SECRET_KEY"]

db = SQLAlchemy(app)
ma = Marshmallow(app)


# TUTORIAL

@app.route('/portal/login')
def login():
    auth = request.authorization
    user = User.query.filter_by(email=auth.username).first()

    if user and check_password_hash(user.password, auth.password):
        data = {'sub': user.id, 'name': user.fullname(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30), 'address': user.address, 'email': user.email}
        token = jwt.encode(data, app.config['SECRET_KEY'], algorithm="HS256")

        return make_response(jsonify({'token': token}), 201)

    return jsonify({"msg": "Incorrect login"})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"msg": "Token is missing!"}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(email=data['email']).first()
        except:
            return jsonify({"msg": "Token is invalid"}), 403

        return f(current_user, *args, **kwargs)

    return decorated


@app.route("/unprotected")
def unprotected():
    return jsonify({"msg": "Anyone can view this!"})


@app.route("/protected")
@token_required
def protected(user):
    print(user.fullname())

    return jsonify({"msg": "You are logged in because you can see this!"})

# TUTORIAL


class User(db.Model):
    """User Model"""
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(50), nullable=False)
    plz = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, forename, lastname, gender, address, plz, email, password):
        self.forename = forename
        self.lastname = lastname
        self.gender = gender
        self.address = address
        self.plz = plz
        self.email = email
        self.password = password

    def fullname(self):
        return self.forename + " " + self.lastname


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'forename', 'lastname', 'gender', 'address', 'plz', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

#  TODO work with cookie and not with user_id
@app.route('/portal/get', methods=['GET'])
@token_required
def get_user(user):
    """Return user data"""

    return user_schema.jsonify(user)


@app.route('/portal/create', methods=['POST'])
def create_account():
    """Creates a user by reading all information from the request as json"""
    # TODO make this cleaner! with data = request.get_json()
    forename = request.json['forename']
    lastname = request.json['lastname']
    gender = request.json.get('gender')  # json.get() because this way, if value is null, there is no exception
    address = request.json['address']
    plz = request.json['plz']
    # TODO no duplicate email in db!
    email = request.json['email']
    password = request.json['password']

    hashed_password = generate_password_hash(password, method='sha256')

    user = User(forename, lastname, gender, address, plz, email, hashed_password)
    db.session.add(user)
    db.session.commit()

    routing_key = 'portal.account.created'
    data = {"id": user.id}
    publish_rabbitmq(routing_key, data)

    return jsonify({"msg": "Account created"})

#  TODO work with cookie and not with user_id
@app.route('/portal/update/<user_id>', methods=['PUT'])
def update_account(user_id):
    """Updates user account information"""
    # Update user, if user with user_id exists
    user = User.query.get(int(user_id))
    if user is not None:
        user.forename = update_if_request_contains(user.forename, request.json.get('forename'))
        user.lastname = update_if_request_contains(user.lastname, request.json.get('lastname'))
        user.gender = update_if_request_contains(user.gender, request.json.get('gender'))
        user.address = update_if_request_contains(user.address, request.json.get('address'))
        user.plz = update_if_request_contains(user.plz, request.json.get('plz'))
        user.email = update_if_request_contains(user.email, request.json.get('email'))
        # TODO password also hashed!
        user.password = update_if_request_contains(user.password, request.json.get('password'))

        db.session.commit()

        routing_key = 'portal.account.updated'
        data = {"id": user.id}
        publish_rabbitmq(routing_key, data)

        return jsonify({"TODO": "NOT IMPLEMENTED YET", "msg:": "Account information updated"})
    else:
        return jsonify({"msg": "Account not found"})

#  TODO work with cookie and not with user_id
@app.route('/portal/delete/<user_id>', methods=['DELETE'])
def delete_account(user_id):
    """Deletes the user with the given user_id, if the user exists"""
    # Delete user, if user with user_id exists
    user = User.query.get(int(user_id))
    if user is not None:
        db.session.delete(user)
        db.session.commit()

        # Put deleted user data in data for rabbitmq publish
        routing_key = 'portal.account.deleted'
        data = {"TODO": "NOT IMPLEMENTED YET", "id": int(user_id)}  # TODO Get user data and id, without password
        publish_rabbitmq(routing_key, data)
        return user_schema.jsonify(user)
    else:
        return jsonify({"msg": "Account not found"})


def update_if_request_contains(user_val, request_val):
    new_val = user_val
    if request_val is not None:
        new_val = request_val

    return new_val


def publish_rabbitmq(routing_key, data):
    """Publish a message given with data on the given routing key"""
    message = json.dumps(data)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='microservice.eventbus', exchange_type='topic')
    channel.basic_publish(
        exchange='microservice.eventbus', routing_key=routing_key, body=message)
    connection.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
