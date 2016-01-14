import requests
from lxml import etree, objectify

def getimage(itemid):
    url="http://catalogapi.ap.org/AP.MessageRepository.APIHost/services/MessageRepository.svc/documents/"+itemid
    r = requests.get(url)
    data = r.content
    tree = etree.fromstring(data)
    mediatype = tree.xpath('//appl:MediaType/text()', namespaces={'appl': 'http://ap.org/schemas/03/2005/appl'})
    if mediatype[0] == 'Text':
        imageids = tree.xpath('//appl:AssociatedWith/text()', namespaces={'appl': 'http://ap.org/schemas/03/2005/appl'})
        bapiurl = 'http://binaryapi.ap.org/' + imageids[0] + '/preview.jpg?wm=api'
        #return bapiurl
    else:
        bapiurl = 'http://binaryapi.ap.org/' + itemid + '/preview.jpg'
    return bapiurl

if __name__ == "__main__":
    getimage("102e6db1436c2637c62a28c234b7e536")
