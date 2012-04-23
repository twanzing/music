#!/usr/bin/python

from optparse import OptionParser
from EN import EN
from googlemaps import GoogleMaps
import re, urllib, json
import pprint

SONGKICKAPIKEY = 'UirC1LAZA5NmBKbn'
SONGKICKUSERNAME = 'wan-yih'

def getNearByShows(location, distance, mbid):	
    events = getArtistShows(mbid)
    nearByShows = []    
    gmaps = GoogleMaps()
    for event in events:
	venueLocation = event['location']['city']
	isUS = re.compile("US$")
	if not isUS.search(venueLocation):
	    print "not in US"
	    continue
#	print "directions between " + location + " and " + venueLocation
        direction = gmaps.directions(location, venueLocation)
#	print direction['Directions']['Distance']['meters']
	if direction['Directions']['Distance']['meters'] < distance:
	    print("Found near by show! %s" % venueLocation)
	    nearByShows.append(event) 
    return nearByShows

def getArtistShows(musicBrainzId):
    url = 'http://api.songkick.com/api/3.0/artists/mbid:' + musicBrainzId + '/calendar.json?apikey=' + SONGKICKAPIKEY
    event_json = urllib.urlopen(url).read()

    eventRef = json.loads(event_json)
    
    if 'event' in eventRef['resultsPage']['results']:
        return eventRef['resultsPage']['results']['event']
    else:
	return []

def getCommittedShows():
    url = 'http://api.songkick.com/api/3.0/users/' + SONGKICKUSERNAME + '/events.json?apikey=' + SONGKICKAPIKEY 
    event_json = urllib.urlopen(url).read()

    eventRef = json.loads(event_json)
    if 'event' in eventRef['resultsPage']['results']:
        return eventRef['resultsPage']['results']['event']
    else:
	return []
 
def generatePlayList(show, artist):
    # get a list of songs fron echoNest then get the spotify ID for those songs
    playList = artist.spotifySongs(results=10)
    # ok, now do it for the openers
    for performers in show['performance']:
        if performers['billing'] == 'support':
            opener = EN(performers['displayName'])
            playList = playList + opener.spotifySongs(results=3)
    return playList

def getHeadliner(show):
    # get the performances
    for perf in show['performance']:
        if perf['billingIndex'] == 1:
	    #headliner!
	    return perf['artist']['displayName']

def committedShowsPlaylist():
    parser = OptionParser()
    parser.add_option("-a", "--artists", dest="thisArtist", help="query on this artist")
    parser.add_option("-l", "--location", dest="location", default="318 Highland Ave., Somerville, MA", help="your current location(city)")
    parser.add_option("-d", "--distance", dest="distance", default=10000)
    (options, args) = parser.parse_args()

    # store off the artists i like that I bought tickets for
    artists = []
    committedShows = getCommittedShows()	
    committedShowsPlaylist = []
    for show in committedShows:
	headliner = getHeadliner(show)
	artist = EN(name=headliner)
	artists.append(artist)
    	committedShowsPlaylist = committedShowsPlaylist + generatePlayList(show, artist)

    for i in range(0, len(committedShowsPlaylist)):
	elements = committedShowsPlaylist[i].split(":")
	committedShowsPlaylist[i] = elements[2]

    # now lets see if there are similar artists of the ones I like
#    similar = []
#    for artist in artists:
	# just get 2 for now
#        similar = similar + artist.similarArtists(results=2)
    
#    for simArtist in similar:
#	print "Similar artists: " + simArtist.name
#	simArtist = EN(simArtist)	
#  	mbid = simArtist.getMusicBrainzID()
#  	print getNearByShows(options.location, options.distance, mbid)
    
    return ", ".join(committedShowsPlaylist)
