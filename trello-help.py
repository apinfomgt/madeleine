import os, re
from trello import TrelloClient
import requests

requests.packages.urllib3.disable_warnings

api_key = os.environ['TRELLO_API_KEY']
api_secret = os.environ['TRELLO_API_SECRET']
token = os.environ['TRELLO_TOKEN_KEY']
token_secret = os.environ['TRELLO_TOKEN_SECRET']
pub_board = os.environ['PUBLISH_BOARD']
event_list = os.environ['EVENT_LIST']

#api_key='d5ce3f1198288ff5de75d0f8c13ecd0c'
#api_secret='59546674a99f6287cbc49259beac752ef3d0481425f1f0b2fca8c1b3a46843a7'
#token='a765d04f047650757ed7ccac107a72bbd5562d50a320c9605228eed698f2b35d'
#token_secret='5c9415d771eb90137b939ac77fa394cb'
#pub_board='5633d93ffc0721b51330a0e1'
#event_list='5633d94a2460148854315431'

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

if __name__ == '__main__':
    print api_key
    print api_secret
    print token
    print token_secret
    print pub_board
    print event_list
	
    boards = MyTrelloClient()._list_boards()
    for b in boards:
        print b.name
