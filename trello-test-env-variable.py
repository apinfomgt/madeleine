import os, re, json
from trello import TrelloClient
import requests

requests.packages.urllib3.disable_warnings

#api_key = os.environ['TRELLO_API_KEY']
#token = os.environ['TRELLO_TOKEN_KEY']
#boardid = os.environ['PUBLISH_BOARD']

api_key='d5ce3f1198288ff5de75d0f8c13ecd0c'
token='a765d04f047650757ed7ccac107a72bbd5562d50a320c9605228eed698f2b35d'
boardid='5633d93ffc0721b51330a0e1'


if __name__ == '__main__':



    print api_key
    print token
    print boardid

    mytrello = TrelloClient(api_key=api_key,token=token)
    print mytrello
    try:
        board = mytrello.get_board(boardid)
        print board.name
    except:
        print 'failed via py-trello'

    try:
        url =  'https://trello.com/1/boards/%s?key=%s&token=%s' % (boardid,api_key,token)
        print url
        r = requests.get(url)
        print json.loads(r.text)['name']
    except:
        print 'failed via requests'
