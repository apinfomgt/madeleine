import json, os
from slackclient import SlackClient
from flask import Flask, request
from slack import slack

app = Flask(__name__)

@app.route("/slack/events", methods = ['GET'])
def slack_get():
    text = request.args.get('text')
    channel = request.args.get('channel_name')
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    slack(text, channel, user_id, user_name)
    return ()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
