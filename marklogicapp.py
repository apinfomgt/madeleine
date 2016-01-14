import os, re, json, requests
from requests.auth import HTTPDigestAuth


marklogic_snippets = os.environ['MARKLOGIC_SNIPPETS']
ml_user = os.environ['ML_USER']
ml_pass = os.environ['ML_PASS']

def snippet(eventid,eventname):
    event = {"eventid":eventid,"eventname":eventname}
    headers = {'content-type': 'application/json'}
    r = requests.post(marklogic_snippets, auth=HTTPDigestAuth(ml_user,ml_pass), data=json.dumps(event), headers=headers)
    return r.status_code

if __name__ == "__main__":
    snippet('http://cv.ap.org/id/a2bc8bbed18a4ed0a985b1079e51d507','Space oddity')
