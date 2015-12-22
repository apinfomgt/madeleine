import uuid, re

def generateuuid():
    eventid = uuid.uuid4()
    cleanid = re.sub('[-]', '', str(eventid))
    return cleanid

if __name__ == "__main__":
    generateuuid()
