import json, os
from slackclient import SlackClient

# def slackcreate(text, channel, user_id, user_name):
def slackcreate(text):
    sc = SlackClient(os.environ['slack_token'])
    # join_channel = sc.api_call('channels.join', name=text)
    testing = sc.api_call("api.test")
    return
    # read_response = json.loads(join_channel)
    # channel_id = read_response['channel']['id']
    # invite_to_channel = sc.api_call('channels.invite', channel=channel_id, user=user_id)
    # post_text = 'A new event channel called: ' + text + ' has been created. Join to contribute.'
    # return 'Test - You just created a story called ' + text + ' your new slack channel is: #' + text + ' You have been invited to this channel.'

if __name__ == "__main__":
    slackcreate()
