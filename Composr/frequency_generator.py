from new_PyLyrics import *
import string
import nltk
from nltk.probability import *
import time

bigram_dict = dict()
total_artists = 0
total_possible_songs = 0
total_songs = 0
output_file = open("output.txt", "w")
input_file = open("artists.txt", "r")

input_read = input_file.readlines()
artist_list = [w.replace('\n', '') for w in input_read] #remove newlines from artist names
artist_list = [w.title() for w in artist_list] #artist names need to be capitalized
start_time = time.time()

counter = 0

for artist in artist_list:
    counter = counter + 1
    
    print("(" + str(counter) + ") " + artist)
    albums = getAlbums(artist)
    if len(albums) == 0:
        continue
    else:
        total_artists += 1

    for album in albums:
        tracks = getTracks(artist, album)
        for track in tracks:
            total_possible_songs += 1
            #print("(" + str(counter) + ") " + track)
            try:
                lyrics = getLyrics(artist, track)
                total_songs += 1
            except (UnicodeEncodeError, ValueError, IndexError):
                continue
    
            lyrics_freq = FreqDist(lyrics)

            bigrams = nltk.bigrams(lyrics)
            bigram_freq = FreqDist(bigrams)


            for k,v in bigram_freq.items():
                if k[0] in bigram_dict:
                    if k[1] in bigram_dict[k[0]]:
                        bigram_dict[k[0]][k[1]] += v
                    else:
                        bigram_dict[k[0]][k[1]] = v
                else:
                    bigram_dict[k[0]] = {}
                    bigram_dict[k[0]][k[1]] = v



for word in bigram_dict:
    try:
        output_file.write(word+"@")
    except (UnicodeEncodeError, ValueError, IndexError):
            continue
    for next_word in bigram_dict[word]:
        try:
            output_file.write(next_word+"@"+str(bigram_dict[word][next_word])+"@")
        except (UnicodeEncodeError, ValueError, IndexError):
            continue
    output_file.write("\n")

print("Total artists: " + str(total_artists) + " out of " + str(len(artist_list)))
print("Total songs: " + str(total_songs) + " out of " + str(total_possible_songs))
print("Total unique words: " + str(len(bigram_dict)))
print("Total time: " + str(time.time() - start_time))

output_file.close()

