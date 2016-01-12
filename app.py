import json, os, requests
from slackclient import SlackClient
from flask import Flask, request, jsonify
from slackapp import slackcreate
from generate_uuid import generateuuid
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
    thr = Thread(target=slack_get, args=[text, channel, user_id, user_name])
    return thr.start()

def slack_get(text, channel, user_id, user_name):
    guid = get_uuid()
    slackwork = slackcreate(text, channel, user_id, user_name, guid)
    # TEMPORARY WHILE TESTING THREADING
    # newboard = TrelloCreate()._create_event_board(name=text,guid=guid,description=None)
    # url = newboard.url
    # print url
    # wfrom = 'slack'
    # print wfrom
    # try:
    #     print 'creating event card'
    #     return TrelloCreate()._create_event_card(name=text,guid=guid,url=url,wfrom=wfrom,description=None)
    # except Exception,e:
    #     print str(e)

    # TO REMAIN COMMENTED, NOT PART OF THE TEMPORARY SET
    # try:
    #     return slackcreate(text, channel, user_id, user_name, guid)
    # except Exception,e:
    #     print str(e)

@app.route('/trello/events', methods=['POST'])
def trello_new_event():
    try:
        response = request.data
        data = json.loads(response)
        print data
        cardid = data['action']['data']['card']['id']
        actiontype = data['action']['type']
        card = MyTrelloClient()._get_card(cardid)
        print card
        #test if card was created by slack
        wfrom = [x.name for x in card.labels if x.name=='FromSlack']

        if 'FromSlack' not in wfrom and actiontype == 'createCard':
            name = data['action']['data']['card']['name']
            try:
                description = data['action']['data']['card']['desc']
            except:
                description = 'Enter description'
            guid = get_uuid()
            print 'creating new board'
            newboard = TrelloCreate()._create_event_board(name=name,guid=guid,description=description)
            print newboard
            url = newboard.url
            print url
            TrelloCreate()._update_event_card(newboard,card)
            # create event in Slack
            slackcreate(name, None, None, None, guid)
            return jsonify({'result': True})
        else:
            return jsonify({'result': 'No event created'})
    except Exception as e:
        print(str(e))
        return jsonify({'result': 'Error'})

    return jsonify({'result': True})

@app.route('/trello/events', methods=['HEAD'])
def head():
    return jsonify({'result': True})

@app.route('/trello/publish', methods=['POST'])
def trello_publish():
    try:
        response = request.data
        data = json.loads(response)
        print data
        listafter = data['action']['data']['listAfter']['name']
        actiontype = data['action']['type']
        cardid = data['action']['data']['card']['id']
        print listafter + ':' + actiontype + ':' + cardid
        if actiontype == 'updateCard' and listafter == 'Publishing':
            TrelloPublish()._trigger_publish(cardid)
        else:
            return jsonify({'result': True})
    except Exception as e:
        print(str(e))
        return jsonify({'result': 'Error'})

@app.route('/trello/publish', methods=['HEAD'])
def pub_head():
    return jsonify({'result': True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
