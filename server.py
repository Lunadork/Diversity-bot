from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from bot import hazibot
import psycopg2


server = Flask(__name__)
CORS(server)

server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@172.17.0.2/postgres'
db = SQLAlchemy(server)
con = psycopg2.connect('postgresql://postgres:password@172.17.0.2/postgres')


import dbsetup

hazibot.setup()
dbsetup.setup()

@server.route('/',methods=['GET'])
def index():
    return render_template('index.html'),200

@server.route('/bot',methods=['POST'])
def send_message():
    data = request.get_json()
    response = hazibot.hazibot_generate_response(data)
    return response, 202

@server.route('/cbt', methods = ['GET'])
def cbt_advice():
    return render_template('cbt.html'),200
