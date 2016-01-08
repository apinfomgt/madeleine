import os, re, json, requests, urllib
from trello import TrelloClient,Label
from requests.auth import HTTPDigestAuth

api_key = os.environ['TRELLO_API_KEY'].strip()
api_secret = os.environ['TRELLO_API_SECRET'].strip()
token = os.environ['TRELLO_TOKEN_KEY'].strip()
token_secret = os.environ['TRELLO_TOKEN_SECRET'].strip()
pub_board = os.environ['PUBLISH_BOARD'].strip()
event_list = os.environ['EVENT_LIST'].strip()
from_slack = os.environ['FROM_SLACK'].strip()
from_trello = os.environ['FROM_TRELLO'].strip()
marklogic = os.environ['MARKLOGIC'].strip()
ml_user = os.environ['ML_USER'].strip()
ml_pass = os.environ['ML_PASS'].strip()

_trello_client = None

def get_trello_client(api_key, api_secret, token, token_secret):
    global _trello_client
    if _trello_client == None:
        _trello_client = TrelloClient(api_key=api_key,
                api_secret=api_secret,
                token=token,
                token_secret=token_secret)
    return _trello_client

class MyTrelloClient(object):
    def __init__(self):
        self._trello = get_trello_client(api_key=api_key,
                api_secret=api_secret,
                token=token,
                token_secret=token_secret)

    def _list_boards(self):
        boards = self._trello.list_boards()
        return boards

    def _get_board(self,id):
        board = self._trello.get_board(id)
        return board

    def _add_board(self,name):
        board = self._trello.add_board(name)
        return board

    def _get_card(self,id):
        card = self._trello.get_card(id)
        return card

class TrelloPublish():
    def __init__(self):
        self.publish = MyTrelloClient()._get_board(pub_board)
        self.events = self.publish.get_list(event_list)

    def _trigger_publish(self,cardid):
        card = MyTrelloClient()._get_card(cardid)
        attachments = card.client.fetch_json('/cards/' + card.id + '/attachments')
        for attachment in attachments:
            print 'attachment:' + attachment['url']
            if re.match(r'^http.*//.*/b/.*', attachment['url']) is not None:
                boardshortid = attachment['url'].split('/')[4]
                print 'publishing boardshortid:' + boardshortid
                self._publish_from_trello(boardshortid)

    def _publish_from_trello(self,boardid):
        model = {}
        model['itemids'] = []
        print 'getting board'
        myboard = MyTrelloClient()._get_board(boardid)
        print 'getting lists'
        mylists = myboard.client.fetch_json('/boards/' + boardid + '/lists')
        for l in myboard.open_lists():
            if l.name == 'Metadata':
                print 'found metadata list'
                for c in l.list_cards():
                    for label in c.labels:
                        if label.name=='EventId':
                            print 'found eventid: ' + c.name
                            model['eventid'] = c.name
            elif l.name == 'To publish':
                print 'found to publish list'
                names = [c.name for c in l.list_cards()]
                for name in names:
                    itemid = re.search(r'\b([0-9a-fA-F]{32,32})\b', name).group(1)
                    model['itemids'].append(itemid)
            else:
                pass
        print 'sending publish package to marklogic'
        print  model
        headers = {'content-type': 'application/json'}
        r = requests.post(marklogic, auth=HTTPDigestAuth(ml_user,ml_pass), data=json.dumps(model), headers=headers)

class TrelloCreate():
    def __init__(self):
        self.publish = MyTrelloClient()._get_board(pub_board)
        self.events = self.publish.get_list(event_list)


    def _create_event_board(self,name,guid,description=None):
        if description == '' or description == None:
            description = 'Enter description'
        else:
            description = description
        newboard = MyTrelloClient()._add_board(name)
        #close all default lists before creating new ones
        print 'delete default lists'
        try:
            defaultlists = newboard.get_lists('open')
            for defaultlist in defaultlists:
                defaultlist.close()
        except:
            pass
        print 'adding labels'
        #create labels for metadata list
        addeventidlabel = [newboard.add_label('EventId','green')]
        addnamelabel = [newboard.add_label('EventName','blue')]
        adddescriptionlabel = [newboard.add_label('EventDescription','red')]
        print 'creating lists'
        #create lists
        publish = newboard.add_list('To publish')
        progress = newboard.add_list('In progress')
        metadata = newboard.add_list('Metadata')
        print 'adding metadata cards'
        card1 = metadata.add_card(name=guid,labels=addeventidlabel)
        card2 = metadata.add_card(name=name,labels=addnamelabel)
        card3 = metadata.add_card(name=description,labels=adddescriptionlabel)
        return newboard

    def _create_event_card(self,name,guid,url,wfrom,description=None):
        print wfrom
    	print from_slack
    	print from_trello
    	try:
                if wfrom == 'slack':
                    label = self.publish.client.fetch_json('/boards/' + pub_board + '/labels/' + from_slack )
                    labels = [Label.from_json(self.publish,label)]
                elif wfrom == 'trello':
                    label = self.publish.client.fetch_json('/boards/' + pub_board + '/labels/' + from_trello )
                    labels = [Label.from_json(self.publish,label)]
                else:
                    labels = []
                print labels

                newcard = self.events.add_card(name,description,labels=labels)
                newcard.attach(name=name, url=url)
                return newcard
        except Exception as e:
            print(str(e))

        def _update_event_card(self,board,card):
            try:
                url = board.url
                name = url
                card.attach(name=name, url=url)
                return card
            except Exception as e:
                print(str(e))
