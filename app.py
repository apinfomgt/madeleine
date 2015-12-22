import json, os, requests
from slackclient import SlackClient
from flask import Flask, request, jsonify
from slackapp import slackcreate
from generate_uuid import generateuuid
from trelloapp import TrelloCreate, MyTrelloClient

app = Flask(__name__)

@app.route("/uuid", methods = ['GET'])
def get_uuid():
    return generateuuid()

@app.route("/")
@app.route("/slack/events", methods = ['GET'])
def slack_get():
    text = request.args.get('text')
    channel = request.args.get('channel_name')
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    eventid = get_uuid()
    try:
        return slackcreate(text, channel, user_id, user_name, eventid)
    except Exception,e:
        print str(e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
