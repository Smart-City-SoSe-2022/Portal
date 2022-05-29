import json.encoder
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import pika
from dotenv import dotenv_values

app = Flask(__name__)
CORS(app)

config = dotenv_values(".env")
app.config['SQLALCHEMY_DATABASE_URI'] = config["DB_FULL_URI"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    """User Model"""
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50))
    address = db.Column(db.String(50), nullable=False)
    plz = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, forename, lastname, gender, address, plz, email, password):
        self.forename = forename
        self.lastname = lastname
        self.gender = gender
        self.address = address
        self.plz = plz
        self.email = email
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'forename', 'lastname', 'gender', 'address', 'plz', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

#  TODO work with cookie and not with user_id
@app.route('/portal/get', methods=['GET'])
def get_users():
    """Return user data"""

    # Should return data from a single user, but not implemented yet
    all_users = User.query.all()

    return users_schema.jsonify(all_users)


@app.route('/portal/create', methods=['POST'])
def create_account():
    """Creates a user by reading all information from the request as json"""
    forename = request.json['forename']
    lastname = request.json['lastname']
    gender = request.json.get('gender')  # json.get() because this way, if value is null, there is no exception
    address = request.json['address']
    plz = request.json['plz']
    email = request.json['email']
    password = request.json['password']

    user = User(forename, lastname, gender, address, plz, email, password)
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
    credentials = pika.PlainCredentials(config["RABBITMQ_USER"], config["RABBITMQ_PASSWORD"])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.104.41.215', credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='microservice.eventbus', exchange_type='topic')
    channel.basic_publish(
        exchange='microservice.eventbus', routing_key=routing_key, body=message)
    connection.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
