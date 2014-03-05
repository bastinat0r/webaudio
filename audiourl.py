import urllib

def retrieve_url(url, path='./'):
    try:
        urllib.urlretrieve( url, "path/%s"%(url.split('/')[-1]) )
        return "path/%s"%(url.split('/')[-1])
    except Exception, e:
        print e
        return None
def validate(url):
    if url.match("^(http://|https://|ftp://).+\\..+(mp3|m4a|ogg|acc)$"):
        return True
    return False
