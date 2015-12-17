import json, os
from slackclient import SlackClient
from flask import Flask, request
from slackapp import slackcreate

app = Flask(__name__)

@app.route("/")
@app.route("/slack/events", methods = ['GET'])
def slack_get():
    text = request.args.get('text')
    channel = request.args.get('channel_name')
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    return slackcreate(text, channel, user_id, user_name)

@app.route('/trello/events', methods=['POST'])
def trello_new_event():
    if not request.json or not 'title' in request.json:
        abort(400)
    cardid = request.json['card']['id']
    name = request.json['card']['name']
    description = request.json['card']['desc']
    #update this with uuid function when we have it
    guid = '123456789'
    newboard = TrelloCreate()._create_event_board(name=name,guid=guid,description=description)
    url = newboard.url
    card = MyTrelloClient()._get_card(cardid)
    TrelloCreate()._update_event_card(newboard,card)
    return jsonify({'result': True})

@app.route('/trello/events', methods=['HEAD'])
def head():
    return jsonify({'result': True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
