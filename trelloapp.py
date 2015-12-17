import os, re
from trello import TrelloClient

api_key = os.environ['TRELLO_API_KEY']
api_secret = os.environ['TRELLO_API_SECRET']
token = os.environ['TRELLO_TOKEN_KEY']
token_secret = os.environ['TRELLO_TOKEN_SECRET']
pub_board = os.environ['PUBLISH_BOARD']
event_list = os.environ['EVENT_LIST']

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

class TrelloCreate():
    def __init__(self):
        print 'getting pub board'
        print pub_board
        self.publish = MyTrelloClient()._get_board(pub_board)
        self.events = self.publish.get_list(event_list)


    def _create_event_board(self,name,guid,description=None):
        if description == '' or description == None:
            description = 'Enter description'
        else:
            description = description
        newboard = MyTrelloClient()._add_board(name)
        print newboard
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

    def _create_event_card(self,name,guid,url,description=None):
        try:
            newcard = self.events.add_card(name,description)
            newcard.attach(name=name, url=url)
            return newcard
        except Exception as e:
            print(str(e))
            self.fail("Caught Exception adding card")

    def _update_event_card(self,board,card):
        try:
            url = board.url
            name = url
            card.attach(name=name, url=url)
            return card
        except Exception as e:
            print(str(e))
            self.fail("Caught Exception updating card")
