from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from bot import hazibot

server = Flask(__name__)
CORS(server)

@server.route('/',methods=['GET'])
def index():
    print("index")
    return render_template('index.html'),200

@server.route('/bot',methods=["POST"])
def send_message():
    data = request.get_json()
    predicted_intent = hazibot.predict_class(data['message'])
    res = hazibot.get_response(predicted_intent, hazibot.intents)
    return res, 202



if __name__ == "__main__":
    server.run(debug=True) 