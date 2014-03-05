import mplayer
import youtube
from time import sleep
import threading
import sys
import audiourl

class Player(threading.Thread):
    """Docstring for Player """

    def __init__(self, playlist):
        """"""
        self._playlist = playlist
        self._archive = []
        self._p = mplayer.Player()
        threading.Thread.__init__(self)
        self.daemon = True
        self._current = None
        self._next = None

    def _fetch_next(self):
        """get next item from playlist
        :returns: path to audio-file

        """
        if self._playlist == []:
            self._playlist = self._archive
            self._archive = []
        current = self._playlist.pop(0)
        if youtube.validate(current):
            self._archive.append(current)
            return youtube.dl_audiostream(current, path="music")
        elif audiourl.validate(current):
            r = retrieve_url(current)
            if r:
                self._archive.append(current)
                return r;

    def append(self, command):
        """append new entry to playlist
        """
        if command == "skip":
            self.play_next()
        elif youtube.validate(command):
            self._playlist.append(command)
            print "appending %s to playlist" %command
        elif audiourl.validate(command):
            self._playlist.append(command)
            print "appending %s to playlist" %command

    def play_next(self):
        if self._current:
            self._current = self._next
        else:
            self._current = self._fetch_next()
        print "playing %s" %self._current
        self._p.loadfile(self._current)
        self._p.pause()
        self._next = self._fetch_next()


    def run(self):
        while True:
            if self._p.percent_pos < 1:
                self.play_next()
            sleep(1)

if __name__ == '__main__':
    p = Player(["https://www.youtube.com/watch?v=P9spezXhJuU", "https://www.youtube.com/watch?v=i4BYMvVvMg0", "https://www.youtube.com/watch?v=-1z6M4sZmQ0"])
    p.start()
    while True:
        s = raw_input()
        p.append(s)
