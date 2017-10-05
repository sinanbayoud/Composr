import requests
import re
from bs4 import BeautifulSoup, Comment, NavigableString
from nltk.tokenize import word_tokenize

'''
Given an artist name, return a list of that artist's album titles.
Artist names should have the first letter of every word capitalized (even in the
case of lowercase artist names (e.g. mc chris)), and punctuation
included (e.g. the band "Fun.")

Format is "Album_Title_(Release Year)"
'''
def getAlbums(singer):
  singer = singer.replace(' ', '_')

  s = BeautifulSoup(requests.get('http://lyrics.wikia.com/{0}'.format(singer)).text, "html5lib")

  albums = []
  for link in s.find_all('a'):
    href = str(link.get('href'))
    if ("/wiki/" + singer + ":") in href and re.match(".*\([12][0-9][0-9][0-9]\).*", href):
      albums.append(href.split(':')[1])

  return albums

'''
Given a singer and an album title, return a list of the tracks in the album.

Output format is "Track_Name"

The same constraints to the singer name applies as in getAlbums(), and the album
name format should be the same as the output of getAlbums()
'''
def getTracks(singer, album):
  singer = singer.replace(' ', '_')
  s = BeautifulSoup(requests.get('http://lyrics.wikia.com/{0}'.format(singer+":" + album)).text, "html5lib")

  tracks = []
  for link in s.find_all('a'):
    href = str(link.get('href'))
    if ("/wiki/" + singer + ":") in href and not re.match(".*\([12][0-9][0-9][0-9]\).*", href):
      tracks.append(href.split(':')[1])

  return tracks

'''
Given a singer and a track, returns a word-tokenized list of the words in the track.

The same constraints to the singer name applies as in getAlbums, and the track
name format should be the same as the output of getAlbums()
'''
def getLyrics(singer, track):

  singer = singer.replace(' ', '_')
  s = BeautifulSoup(requests.get('http://lyrics.wikia.com/{0}'.format(singer+":" + track)).text, "html5lib")

  lyrics = s.find("div", {'class':'lyricbox'})
  if lyrics is None:
    raise ValueError("Song or Singer does not exist or the API does not have Lyrics")
    return None

  
  capitalized = ' '.join([(s[0].capitalize() + s[1:]) for s in lyrics.text.split(' ')]) 
  words = re.findall('[A-Z][^A-Z ]*', capitalized)
  cleaned = ' '.join(words)
  word_list = word_tokenize(cleaned)

  return word_list

'''
#Example usage:

singer = "The Beatles"
albums = getAlbums(singer)
tracks = getTracks(singer, albums[0])
lyrics = getLyrics(singer, tracks[0])
print lyrics

'''
