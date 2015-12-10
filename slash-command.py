import json, os
from slackclient import SlackClient
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def reply():
    text = request.args.get('text')
    channel = request.args.get('channel_name')
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    sc = SlackClient(os.environ['slack_token'])
    sc.api_call('channels.join', name=text)
    #THIS DOESN'T WORK channel_id = request.args.get('id')
    #sc.api_call('channels.invite', channel=text, user=user_name)
    return 'The channel ID is: ' + channel_id #'You just created a story called ' + text + ' your new slack channel is: #' + text

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
