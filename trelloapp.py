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
    """
    def _get_list(self,id):
        list = self._trello.get_list(id)
        return list

    def _add_card(self,name,description=None):
        card = self._trello.add_card(name,description)
        return card
    """


class TrelloCreate():
    def __init__(self):
        self.publish = MyTrelloClient()._get_board(pub_board)
        self.events = self.publish.get_list(event_list)


    def _create_event_board(self,name,guid,description=None):
        newboard = MyTrelloClient()._add_board(name)
        #close all default lists before creating new ones
        try:
            defaultlists = newboard.get_lists('open')
            for defaultlist in defaultlists:
                defaultlist.close()
        except:
            pass

        #create labels for metadata list
        addeventidlabel = [newboard.add_label('EventId','green')]
        addnamelabel = [newboard.add_label('EventName','blue')]
        adddescriptionlabel = [newboard.add_label('EventDescription','red')]
        #create lists
        publish = newboard.add_list('To publish')
        progress = newboard.add_list('In progress')
        metadata = newboard.add_list('Metadata')
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
        url = board.url
        name = url
        card.attach(name=name, url=url)
        return card

if __name__ == '__main__':
    #newboard = TrelloCreate()._create_event_board('I fell off a cliff','5ef2522ea7a04aa0b7309dccd264c4c1','It hurt.')
    #url = newboard.url
    #TrelloCreate()._create_event_card('I fell off a cliff','5ef2522ea7a04aa0b7309dccd264c4c1',url,'It hurt.')

    cardid = '56718c4619502914d5a83311'
    boardid = '5633d9b38de295a9453a1eef'

    board = MyTrelloClient()._get_board(boardid)
    card = MyTrelloClient()._get_card(cardid)

    TrelloCreate()._update_event_card(board,card)


    #board = MyTrelloClient()._add_board('test')
    #mylabels = []
    #addmylabel = mylabels.append(board.add_label('EventId','green'))
    #metadata = board.add_list('Metadata')
    #card = metadata.add_card(name='1234',labels=mylabels)
    #TrelloCreate()._create_event('Test')

    """
    for l in publish.all_lists():
        print l.id
        print l.name

    boards = MyTrelloClient()._list_boards()
    for b in boards:
        print b.id
        print b.open_lists()
    """
    """
    newboard = MyTrelloClient()._get_board('5671a136c5d0bfd5246c1013')

    try:
        defaultlists = newboard.get_lists('open')
        for defaultlist in defaultlists:
            defaultlist.close()
    except:
        pass

    addeventidlabel = [newboard.add_label('EventId','green')]
    addnamelabel = [newboard.add_label('EventName','blue')]
    adddescriptionlabel = [newboard.add_label('EventDescription','red')]
    publish = newboard.add_list('To publish')
    progress = newboard.add_list('In progress')
    metadata = newboard.add_list('Metadata')
    card1 = metadata.add_card(name='1234',labels=addeventidlabel)
    card2 = metadata.add_card(name='TestName',labels=addnamelabel)
    card3 = metadata.add_card(name='TestDescription',labels=adddescriptionlabel)
    #print testlist._set_remote_attribute('name','testy')
    """
