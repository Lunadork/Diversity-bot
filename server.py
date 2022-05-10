from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from bot import hazibot
hazibot.setup()


server = Flask(__name__)
CORS(server)



@server.route('/',methods=['GET'])
def index():
    return render_template('index.html'),200

@server.route('/bot',methods=['POST'])
def send_message():
    data = request.get_json()
    response = hazibot.hazibot_generate_response(data)
    return response, 202
