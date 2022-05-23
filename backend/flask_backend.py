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
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    password = db.Column(db.String(50))
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, forename, lastname, gender, password):
        self.forename = forename
        self.lastname = lastname
        self.gender = gender
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'forename', 'lastname', 'gender', 'password', 'creation_date')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


@app.route('/create', methods=['POST'])
def create_account():
    forename = request.json['forename']
    lastname = request.json['lastname']
    gender = request.json['gender']
    password = request.json['password']

    user = User(forename, lastname, gender, password)
    db.session.add(user)
    db.session.commit()

    # return 'Account created'
    return user_schema.jsonify(user)


@app.route('/get', methods=['GET'])
def get_users():
    all_users = User.query.all()

    return users_schema.jsonify(all_users)


@app.route('/message', methods=['POST'])
def send_message():
    routing_key = request.json['routing_key']
    message = request.json['message']

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='microservice.eventbus', exchange_type='topic')
    channel.basic_publish(
        exchange='microservice.eventbus', routing_key=routing_key, body=message)
    connection.close()

    return f"Message sent: {message}"


if __name__ == '__main__':
    app.run(debug=True)
