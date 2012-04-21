#!/usr/bin/python

from pyechonest import config
from pyechonest import artist
from pyechonest import song

config.ECHO_NEST_API_KEY="ADPSTO1TYQSNQSBGV"

class EN(object):
	def __init__(self, name=nil, artistObj=nil):
	    if artistObj:
		self.artist = artistObj
		return

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
	    for song in self.artist.get_songs(results=results):
	    	print "Songs %s" % (song.title)
		track = song.get_tracks('spotify-WW')
		if len(track) == 0:
		    print "No associated spotify track!"
		else:
		    print "SPOTIFY ID: " + track[0]['foreign_id']
		    spotifySongs.append(track[0]['foreign_id'])
	    return spotifySongs

	def getMusicBrainzID(self):
	    idString = self.artist.get_foreign_id('musicbrainz').split(":")
	    return idString[2]
					
	def getLastFmUrl(self):
		urls = self.artist.get_urls()
		url = urls.get("lastfm_url")
		return url
	
