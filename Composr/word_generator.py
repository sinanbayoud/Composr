import readfromfile
import nltk
from random import randint
from nltk import *

genres = {}

def next_words(word, pos, genre, mode='probability'):
  if genre not in genres:
    genres[genre] = readfromfile.buildDict(genre+"_bigram_output.txt")
    
  dictionary = genres[genre]
  following = dictionary[word]
  
  #start of Andrew stuff
  following_limited = following
  if (len(pos) != 0):
    following_limited = dict()
    possible_pos = pos.split("@")
    for next_word in following:
      text = word_tokenize(next_word)
      tag_pair = nltk.pos_tag(text)
      word_pos = tag_pair[0][1]
      if (word_pos in possible_pos):
        following_limited[next_word] = following[next_word]

  if (len(following_limited) > 0):  
    following = following_limited

  if mode == 'probability':
    try:
      
      tot = sum([int(s) for s in following.values()])
      selection = randint(0, tot)

      curr = 0
      for key in following.keys():
        curr = curr + int(following[key])

        if selection < curr:
          return key
    except ValueError:
      if (len(following) > 0):
        return following[0]
    return ","
  else:
    print ("Not supported yet")
  
