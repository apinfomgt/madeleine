from trelloapp import TrelloCreate,MyTrelloClient
import requests

requests.packages.urllib3.disable_warnings()


def _test_from_slack(name,guid,description=None):
    newboard = TrelloCreate()._create_event_board(name=name,guid=guid,description=description)
    url = newboard.url
    TrelloCreate()._create_event_card(name=name,guid=guid,url=url,description=description)

def _test_from_trello(name,guid,cardid,description=None):
    newboard = TrelloCreate()._create_event_board(name=name,guid=guid,description=description)
    url = newboard.url
    card = MyTrelloClient()._get_card(cardid)
    TrelloCreate()._update_event_card(newboard,card)

if __name__ == '__main__':
    _test_from_slack('TestEventFromSlack','49b55117b7e043deb0517e4fdb02336b','Creating an Event from Slack')
    #_test_from_trello('TestEventFromTrello','49b55117b7e043deb0517e4fdb02336b','567316f941cd49b748effac5','')
