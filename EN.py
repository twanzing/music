#!/usr/bin/python

from pyechonest import config
from pyechonest import artist
from pyechonest import song
import urllib, json, re

config.ECHO_NEST_API_KEY="ADPSTO1TYQSNQSBGV"

class EN(object):
    def __init__(self, name):
        results = artist.search(name=name)
	if (results):
            self.artist = results[0]
	else:
            print "Can't find artist %s " %(name,)

    def similarArtists(self, results=10):
	print "Artists similar to: %s:" % (self.artist.name,)
	return self.artist.get_similar(results=results, min_hotttnesss=0.5)

    def spotifySongs(self, results=10):
	print "Songs of %s " % (self.artist.name)
	spotifySongs = []
	holder = song.search(artist_id=self.artist.id, results=30, sort="song_hotttnesss-desc")
	songs = []
	
	# let's get rid of dups
	for currSong in holder:
	    if not currSong.title in songs:
		songs.append(currSong.title)
	    	if len(songs) == results: break
	
	for song1 in songs:
	    print "Songs %s" % (song1)
	    spotifyID = self.searchSpotify(song1, self.artist.name)
	    if spotifyID != "":
	        spotifySongs.append(spotifyID)
	
	return spotifySongs

    def getMusicBrainzID(self):
	idString = self.artist.get_foreign_id('musicbrainz').split(":")
	return idString[2]

    def isSongAvailable(self, track=None, location="US"):
	territory = track['album']['availability']['territories']
	pattern = location
	if re.search(pattern, territory) != None:
	    return True
	return False
	
    def searchSpotify(self, title, artist):
	# get rid of invalid characters
	title = title.replace('&', '')
    	url = 'http://ws.spotify.com/search/1/track.json?q=' + title
        track_json = urllib.urlopen(url).read()
	trackRef = json.loads(track_json)
	tracks = trackRef['tracks']
	for track in tracks:
	    if track['artists'][0]['name'] == artist:
		if self.isSongAvailable(track=track):
	            print "FOUND!: " + track['href']
		    return track['href']
	return ""
	
					
