#!/usr/bin/python

from optparse import OptionParser
from EN import EN
from googlemaps import GoogleMaps
import re, urllib, json
import pprint

SONGKICKAPIKEY = 'UirC1LAZA5NmBKbn'

def getNearByShows(location, distance, mbid):	
    events = getShows(mbid)
    nearByShows = []    
    gmaps = GoogleMaps()
    for event in events:
	venueLocation = event['location']['city']
	isUS = re.compile("US$")
	if not isUS.search(venueLocation):
	    print "not in US"
	    continue
	print "directions between " + location + " and " + venueLocation
        direction = gmaps.directions(location, venueLocation)
	print direction['Directions']['Distance']['meters']
	if direction['Directions']['Distance']['meters'] < distance:
	    print("Found near by show! %s" % venueLocation)
	    nearByShows.append(event) 
    return nearByShows

def getShows(musicBrainzId):
    url = 'http://api.songkick.com/api/3.0/artists/mbid:' + musicBrainzId + '/calendar.json?apikey=' + SONGKICKAPIKEY
    event_json = urllib.urlopen(url).read()

    eventRef = json.loads(event_json)
    
    if 'event' in eventRef['resultsPage']['results']:
        return eventRef['resultsPage']['results']['event']
    else:
	return []
 
def generatePlayList(shows, artist):
    # get songs from each artist for each show
    for show in shows:
 	# get a list of songs fron echoNest then get the spotify ID for those songs
	artist.spotifySongs()
	# ok, now do it for the openers
	for performers in show['performance']:
	    if performers['billing'] == 'support':
	        opener = EN(performers['displayName'])
		opener.spotifySongs()


    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-a", "--artists", dest="thisArtist", help="query on this artist")
    parser.add_option("-l", "--location", dest="location", default="318 Highland Ave., Somerville, MA", help="your current location(city)")
    parser.add_option("-d", "--distance", dest="distance", default=10000)
    (options, args) = parser.parse_args()
    if (options.thisArtist == None):
	parser.error("Please specify an artist!")
	
    artist1 = EN(options.thisArtist)
    artist1.similarArtists()	
    mbid = artist1.getMusicBrainzID()
    shows = getNearByShows(options.location, options.distance, mbid)
    playList = generatePlayList(shows, artist1)
