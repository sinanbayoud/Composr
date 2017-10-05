############### Imports ###############

import sys
import nltk
from copy import deepcopy
from collections import namedtuple
from random import randint
import syllables
import word_generator
from nltk.parse.generate import generate
from nltk import CFG
from new_PyLyrics import *


############### Function Defs ###############

def create_structure(artist, song):
    try:
      lyrics = getLyrics(artist, song)
    except ValueError:
      return []
    pos = nltk.pos_tag(lyrics)
    return_value = []
    for v in pos:
        return_value.append(v[1])
    return return_value



