import json, os
from slackclient import SlackClient
from flask import Flask, request
from slackapp import SlackCreate

app = Flask(__name__)

@app.route("/")
@app.route("/slack/events", methods = ['GET'])
def slack_get():
    text = request.args.get('text')
    channel = request.args.get('channel_name')
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    return SlackCreate().slackcreate(text, channel, user_id, user_name)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
