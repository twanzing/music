#!/usr/bin/python

from optparse import OptionParser
from EN import EN
from lastFm import lastFm

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-a", "--artists", dest="thisArtist",
			 help="query on this artist")
	(options, args) = parser.parse_args()
	if (options.thisArtist == None):
		parser.error("Please specify an artist!")
	
	artist1 = EN(options.thisArtist)
	artist1.similarArtists()	
	artist1.printSongs()	
	artist1_last = lastFm(options.thisArtist)
	artist1_last.getShows()
