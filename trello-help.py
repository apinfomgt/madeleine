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

if __name__ == '__main__':
    boards = MyTrelloClient()._list_boards
    print boards
