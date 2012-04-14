#!/usr/bin/python

from pyechonest import config
from pyechonest import artist
from pyechonest import song

config.ECHO_NEST_API_KEY="ADPSTO1TYQSNQSBGV"

class EN(object):
	def __init__(self, name):
		results = artist.search(name=name)
		if (results):
			self.artist = results[0]
		else:
			print "Can't find artist %s " %(name,)

	def similarArtists(self):
		print "Artists similar to: %s:" % (self.artist.name,)
		for similar_artist in self.artist.similar:
			print "\t%s" % (similar_artist.name,)

	def spotifySongs(self):
	    print "Songs of %s " % (self.artist.name)
	    for song in self.artist.songs:
	    	print "Songs %s" % (song.title)
		print "ID: " + song.id
		track = song.get_tracks('spotify-WW')
		if len(track) == 0:
		    print "No associated spotify track!"
		else:
		    print "SPOTIFY ID: " + track[0]['foreign_id']
		
	def getMusicBrainzID(self):
	    idString = self.artist.get_foreign_id('musicbrainz').split(":")
	    return idString[2]
					
	def getLastFmUrl(self):
		urls = self.artist.get_urls()
		url = urls.get("lastfm_url")
		return url
	
