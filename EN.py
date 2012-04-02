#!/usr/bin/python

from pyechonest import config
from pyechonest import artist

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

	def printSongs(self):
		print "Songs of %s " % (self.artist.name,)
		for song in self.artist.songs:
			print "\t%s" % (song.title,)
					
	def getLastFmUrl(self):
		urls = self.artist.get_urls()
		url = urls.get("lastfm_url")
		return url
	
