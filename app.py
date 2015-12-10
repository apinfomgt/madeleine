import json, os
from slackclient import SlackClient
from flask import Flask, request

app = Flask(__name__)

@app.route("/slack/events", methods = ['GET'])
def reply():
    text = request.args.get('text')
    channel = request.args.get('channel_name')
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
