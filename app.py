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

def set_guid():
    return get_uuid()

def set_eventid():
    if guid is None:
        guid = eventid
@app.route("/")
@app.route("/slack/events", methods = ['GET'])
def slack_get():
    text = request.args.get('text')
    channel = request.args.get('channel_name')
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    guid = set_guid()
    # create event in Trello
    newboard = TrelloCreate()._create_event_board(name=text,guid=guid,description=None)
    url = newboard.url
    TrelloCreate()._create_event_card(name=text,guid=guid,url=url,description=None)
    try:
        return slackcreate(text, channel, user_id, user_name, guid)
    except Exception,e:
        print str(e)

@app.route('/trello/events', methods=['POST'])
def trello_new_event():
    try:
        response = request.data
        data = json.loads(response)
        print data
        cardid = data['action']['data']['card']['id']
        print cardid
        name = data['action']['data']['card']['name']
        print name
        try:
            description = data['action']['data']['card']['desc']
        except:
            description = 'Enter description'
        print description
        #update this with uuid function when we have it
        guid = get_uuid()
        print 'creating new board'
        newboard = TrelloCreate()._create_event_board(name=name,guid=guid,description=description)
        print newboard
        url = newboard.url
        print url
        card = MyTrelloClient()._get_card(cardid)
        print card
        TrelloCreate()._update_event_card(newboard,card)
        # create event in Slack
        slackcreate(name, None, None, None, guid)
        return jsonify({'result': True})
    except Exception as e:
        print(str(e))
        return jsonify({'result': 'Error'})

    return jsonify({'result': True})

@app.route('/trello/events', methods=['HEAD'])
def head():
    return jsonify({'result': True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
