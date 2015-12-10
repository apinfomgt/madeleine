import os
from trello import TrelloClient
from trello.util import create_oauth_token

api_key = os.environ['TRELLO_API_KEY']
api_secret = os.environ['TRELLO_API_SECRET']

#api_key = 'd5ce3f1198288ff5de75d0f8c13ecd0c'
#api_secret = '7fcbf4de7e31d9478dc06d9c7e1a2ac9258d058da27faa9df72773006cb800a8'



create_oauth_token(key=api_key, secret=api_secret, scope='read,write', expiration='never',name='Madeleine')
