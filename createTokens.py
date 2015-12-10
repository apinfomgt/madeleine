import os
from trello import TrelloClient
from trello.util import create_oauth_token

api_key = os.environ['TRELLO_API_KEY']
api_secret = os.environ['TRELLO_API_SECRET']

create_oauth_token(key=api_key, secret=api_secret, scope='read,write', expiration='never',name='Madeleine')
