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


@app.route('/portal/create', methods=['POST'])
def create_account():
    """Creates a user by reading all information from the request as json"""
    data = request.get_json()

    email = data['email']
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email ist bereits vergeben!"}), 200

    forename = data['forename']
    lastname = data['lastname']
    gender = data.get('gender')  # data.get() because this way, if value is null, there is no exception and gender NULL
    address = data['address']
    plz = data['plz']
    password = data['password']

    hashed_password = generate_password_hash(password, method='sha256')

    user = User(forename, lastname, gender, address, plz, email, hashed_password)
    db.session.add(user)
    db.session.commit()

    routing_key = 'portal.account.created'
    data = {"id": user.id}
    publish_rabbitmq(routing_key, data)

    return jsonify({"msg": "Account wurde erstellt."}), 201


@app.route('/portal/login', methods=['GET'])
def login():
    auth = request.authorization
    user = User.query.filter_by(email=auth.username).first()

    if user and check_password_hash(user.password, auth.password):
        # User / email exists and password is correct, create token so user is logged in
        data = {'sub': user.id, 'name': user.fullname(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}
        token = jwt.encode(data, app.config['SECRET_KEY'], algorithm="HS256")

        resp = make_response(jsonify({'msg': "Login erfolgreich."}), 200)
        resp.set_cookie('JWT', token, samesite=None)

        return resp

    return jsonify({"msg": "Falsche Logindaten!"})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'JWT' in request.cookies:
            token = request.cookies['JWT']

        if not token:
            return jsonify({"msg": "Token fehlt!"}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['sub'])
            if current_user is None:
                return jsonify({"msg": "Token ist ungültig!"}), 401
        except:
            return jsonify({"msg": "Token ist ungültig!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/portal/get', methods=['GET'])
@token_required
def get_user(user):
    """Return user data"""
    return user_schema.jsonify(user), 200


@app.route('/portal/update', methods=['PUT'])
@token_required
def update_account(user):
    """Updates user account information"""
    data = request.get_json()

    email = data.get('email')
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email ist bereits vergeben!"}), 200

    user.forename = update_if_request_contains(user.forename, data.get('forename'))
    user.lastname = update_if_request_contains(user.lastname, data.get('lastname'))
    user.gender = update_if_request_contains(user.gender, data.get('gender'))
    user.address = update_if_request_contains(user.address, data.get('address'))
    user.plz = update_if_request_contains(user.plz, data.get('plz'))
    user.email = update_if_request_contains(user.email, data.get('email'))
    user.password = update_if_request_contains_password(user.password, data.get('password'))

    db.session.commit()

    routing_key = 'portal.account.updated'
    data = {"id": user.id}
    publish_rabbitmq(routing_key, data)

    return {}, 204


@app.route('/portal/delete', methods=['DELETE'])
@token_required
def delete_account(user):
    """Deletes the user and publishes its data to RabbitMQ"""
    db.session.delete(user)
    db.session.commit()

    # Put deleted user data in data for rabbitmq publish
    routing_key = 'portal.account.deleted'
    data = user_schema.jsonify(user).get_json()
    publish_rabbitmq(routing_key, data)
    return {}, 204


def update_if_request_contains(user_val, request_val):
    new_val = user_val
    if request_val is not None:
        new_val = request_val

    return new_val


def update_if_request_contains_password(user_pass, request_pass):
    new_val = user_pass
    if request_pass is not None:
        hashed_password = generate_password_hash(request_pass, method='sha256')
        new_val = hashed_password

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
