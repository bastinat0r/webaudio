import urllib
import re

def retrieve_url(url, path='./'):
    try:
        urllib.urlretrieve( url, "path/%s"%(url.split('/')[-1]) )
        return "path/%s"%(url.split('/')[-1])
    except Exception, e:
        print e
        return None
def validate(url):
    if re.compile("^(http://|https://|ftp://).+\\..+(mp3|m4a|ogg|acc)$").match(url):
        return True
    return False
