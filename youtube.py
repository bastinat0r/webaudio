import pafy
import os.path

def dl_audiostream(url, path=''):
    """download audiostream from youtube

    :url: the youtube url
    :returns: filename of the downloaded file

    """
    video = pafy.new(url)
    audio = video.getbestaudio()
    if path != '':
        path = "%s/%s" %(path, audio.filename)
    if os.path.isfile(path):
        return path
    name = audio.download(filepath=path, quiet=True)
    print "downloaded file %s" %name
    return name

def validate(url):
    try:
        v = pafy.new(url)
        if len(v.audiostreams) > 0:
            return True
    except Exception, e:
        print e
        return False
    return False # should not happen
