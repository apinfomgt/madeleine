import os, re, json
from trello import TrelloClient
import requests

requests.packages.urllib3.disable_warnings

api_key = str(os.environ['TRELLO_API_KEY'])
token = str(os.environ['TRELLO_TOKEN_KEY'])
boardid = str(os.environ['PUBLISH_BOARD'])


if __name__ == '__main__':
    print api_key
    print token
    print boardid

    _trello = TrelloClient(api_key=api_key,token=token)
    try:
        board = _trello.get_board(boardid)
        print board.name
    except:
        print 'failed via py-trello'

    try:
        url = 'https://trello.com/1/boards/' + boardid + '?key=' + api_key + '&token=' + token
        print url
	r = requests.get(url)
	print r
        print json.loads(r.text)['name']
    except:
        print 'failed via requests'
