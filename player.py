import mplayer
import youtube
from time import sleep
import threading
import sys
import audiourl
import argparse

class Player(threading.Thread):
    """Docstring for Player """

    def __init__(self, playlist=[], paused=False, pulse=False):
        """"""
        self._playlist = []
        for entry in playlist:
            self.append(entry)
        self._pause = paused
        self._archive = []
        if pulse:
            self._p = mplayer.Player(args="-ao pulse")
        else:
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
            self._playlist.reverse() # reverse because stack
            self._archive = []
        if self._playlist == []:
            return youtube.dl_audiostream("https://www.youtube.com/watch?v=oHg5SJYRHA0", path="music")
        current = self._playlist.pop()

        if youtube.validate(current):
            self._archive.append(current)
            return youtube.dl_audiostream(current, path="music")
        elif audiourl.validate(current):
            r = retrieve_url(current)
            if r:
                self._archive.append(current)
                return r

    def append(self, command):
        """append new entry to playlist
        """
        if command == "skip":
            self.play_next()
        elif command == "pause":
            self._pause = not self._pause
            return;
        elif command.split("=")[0] == "volume":
            f = float(command.split("=")[1])
            if f > 100.0:
                f = 100.0
            if f < 0.0:
                f = 0.0
            self._p.volume = f
            return;
        elif youtube.validate(command):
            self._playlist.append(command)
            print "appending %s to playlist" %command
            return;
        elif audiourl.validate(command):
            self._playlist.append(command)
            print "appending %s to playlist" %command

    def play_next(self):
        self._current = self._next
        if not self._current:
            self._current = self._fetch_next()
        print "playing %s" %self._current
        self._p.loadfile(self._current)
        self._pause = False
        if self._p.paused:
            self._p.pause()
        self._next = self._fetch_next()


    def run(self):
        while True:
            if self._p.paused != self._pause:
                self._p.pause()
            if not (self._p.percent_pos >= 0):
                self.play_next()
            sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Webdownloarding music-player')
    parser.add_argument('-p','--playlist' , help='playlist-file', default=None)
    parser.add_argument('--paused' , help="start paused, input pause to start playing", action="store_true")
    parser.add_argument('--pulse' , help="activate the pulseaudio driver", action="store_true")
    args = parser.parse_args()
    l = []
    if args and args.playlist:
        with open(args.playlist) as pl:
            l = [ line.rstrip() for line in pl ]
    p = Player(playlist=l, paused=args.paused, pulse=args.pulse)
    p.start()
    while True:
        s = raw_input()
        p.append(s)

