from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from bot import hazibot
import dbconfig
import psycopg2

server = Flask(__name__)
CORS(server)

server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgresql:password@localhost/postgresql'
db = SQLAlchemy(server)

connection = psycopg2.connect(database="postgresql", user="postgresql", host="localhost", password="1234")

@server.route('/',methods=['GET'])
def index():
    print("index")
    return render_template('index.html'),200

@server.route('/bot',methods=["POST"])
def send_message():
    data = request.get_json()
    response = hazibot.hazibot_generate_response(data)
    return response, 202



#MODELS & DB SETUP

class User(db.Model):
    __tablename__='Users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(250))
    have_spoken = db.Column(db.Boolean,default=False)
    primary_concern= db.Column(db.String(250))
    secondary_concerns= db.Column(db.String(1000),default="None")
    has_task= db.Column(db.Boolean,default=False)
    task = db.Column(db.String(1000),default="None")
    flag_words= db.Column(db.Boolean,default=False)
    sought_help= db.Column(db.Boolean,default=False)

    def __init__(self,username,have_spoken,primary_concern,has_task,task):
        self.username=username
        self.have_spoken=have_spoken
        self.primary_concern=primary_concern
        self.has_task=has_task
        self.task=task

class Condition(db.Model):
    __tablename__='Conditions'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250))
    resource = db.Column(db.String(1000))
    task = db.Column(db.String(1000))

    def __init__(self,name,resource,task):
        self.name = name
        self.resource = resource
        self.task = task

db.create_all()

#DB SEED
# dbconfig.seed()


if __name__ == "__main__":
    server.run(debug=True) 