#!/usr/bin/python

import re, urllib
import pylast

username = "twanzing"
password_hash = pylast.md5("ricebowl8")
API_KEY = "fe5b0d7722d3a386276aa9aaef4a53f4" 
API_SECRET = "6f8a7ca6a4b6ba74b88e28b06e08e451"


class lastFm(object):
	def __init__(self, name):
		self.network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)
		self.artist = self.network.get_artist(name)

	def getShows(self):
		events = self.artist.get_upcoming_events()
		for event in events:
	    	    print ("event id: %s" % event.get_id())
		    venueInfo = self.get_venue_name(event)
		    print venueInfo

	def get_venue_name(self, event):
            event_id = str(event.get_id())
            url = 'http://ws.audioscrobbler.com/2.0/?method=event.getinfo&event='
	    url += event_id
	    url += '&api_key='
	    url += API_KEY
	    event_xml = urllib.urlopen(url).read()

	    pre, post = '<name>', '</name>'
	    regex = re.compile(pre + '.*' + post)
	    match = regex.search(event_xml).group()
	    name = match[len(pre) : 0 - len(post)]

	    pre, post = '<city>', '</city>'
	    regex = re.compile(pre + '.*' + post)
	    match = regex.search(event_xml).group()
	    city = match[len(pre) : 0 - len(post)]

	    pre, post = '<country>', '</country>'
	    regex = re.compile(pre + '.*' + post)
	    match = regex.search(event_xml).group()
	    country = match[len(pre) : 0 - len(post)]

	    return ', '.join([name, city, country]) 
