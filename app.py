import json, os, requests, re
from slackclient import SlackClient
from flask import Flask, request, jsonify
from slackapp import slackcreate
from generate_uuid import generateuuid
from getimage import getimage
from trelloapp import TrelloCreate, MyTrelloClient, TrelloPublish
from threading import Thread

app = Flask(__name__)

@app.route("/uuid", methods = ['GET'])
def get_uuid():
    return generateuuid()

@app.route("/slack/events", methods = ['GET'])
def slack_create():
    text = request.args.get('text')
    channel = request.args.get('channel_name')
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    guid = get_uuid()
    thr = Thread(target=slack_get, args=[text, channel, user_id, user_name, guid])
    thr.start()
    return 'Your event is being created'

def slack_get(text, channel, user_id, user_name, guid):
    try:
        slackwork = slackcreate(text, channel, user_id, user_name, guid)
        newboard = TrelloCreate()._create_event_board(name=text,guid=guid,description=None)
        url = newboard.url
        wfrom = 'slack'
        TrelloCreate()._create_event_card(name=text,guid=guid,url=url,wfrom=wfrom,description=None)
    except Exception,e:
        print str(e)

def trello_from_trello(guid,cardid,actiontype,name,description):
    try:
        card = MyTrelloClient()._get_card(cardid)
        print 'testing if card was created by slack'
        wfrom = [x.name for x in card.labels if x.name=='FromSlack']
        if 'FromSlack' not in wfrom and actiontype == 'createCard':
            print 'creating new board'
            newboard = TrelloCreate()._create_event_board(name=name,guid=guid,description=description)
            url = newboard.url
            print 'updating card with board url'
            TrelloCreate()._update_event_card(url,card)
            print 'creating event in slack'
            slackcreate(name, None, None, None, guid)
        else:
            pass
    except Exception,e:
        print str(e)

@app.route('/trello/events', methods=['POST'])
def trello_new_event():
    guid = get_uuid()
    print 'creating event: ' + str(guid)
    response = request.data
    data = json.loads(response)
    cardid = data['action']['data']['card']['id']
    actiontype = data['action']['type']
    name = data['action']['data']['card']['name']
    try:
        description = data['action']['data']['card']['desc']
    except:
        description = 'Enter description'
    thr = Thread(target=trello_from_trello, args=[guid,cardid,actiontype,name,description])
    thr.start()
    return jsonify({'result': True})

@app.route('/trello/events', methods=['HEAD'])
def head():
    return jsonify({'result': True})

def publish_from_trello(listafter,actiontype,cardid):
    try:
        if actiontype == 'updateCard' and listafter == 'Publishing':
            TrelloPublish()._trigger_publish(cardid)
        else:
            pass
    except Exception,e:
        print str(e)

@app.route('/trello/publish', methods=['POST'])
def trello_publish():
    response = request.data
    data = json.loads(response)
    listafter = data['action']['data']['listAfter']['name']
    actiontype = data['action']['type']
    cardid = data['action']['data']['card']['id']
    thr = Thread(target=publish_from_trello, args=[listafter,actiontype,cardid])
    thr.start()
    return jsonify({'result': True})

@app.route('/trello/publish', methods=['HEAD'])
def pub_head():
    return jsonify({'result': True})

def enrich_card(cardid):
    card = MyTrelloClient()._get_card(cardid)
    name = card.name
    itemid = re.search(r'\b([0-9a-fA-F]{32,32})\b', name).group(1)
    #url = getimage(itemid)
    url = 'http://binaryapi.ap.org/' + itemid + '/preview.jpg?wm=api'
    TrelloCreate()._update_event_card(url,card)

@app.route('/trello/enrich', methods=['POST'])
def trello_enrich():
    response = request.data
    data = json.loads(response)
    cardid = data['action']['data']['card']['id']
    thr = Thread(target=enrich_card, args=[cardid])
    thr.start()
    return jsonify({'result': True})

@app.route('/trello/enrich', methods=['HEAD'])
def enrich_head():
    return jsonify({'result': True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
