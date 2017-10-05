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
from song_pos import *

############### Type Defs ###############

#each field of stanza is a list of length 2 where
Stanza = namedtuple("Stanza", "num_lines, num_words, num_syllables")

#Intro, Chorus, Verse, and Outro are Stanzas
#Outline is a list, where each element is a string in
# {"Intro", "Verse", "Chorus", "Outro"}
Song = namedtuple("Song", "Intro Chorus Verse Outro Outline")

#these structures hold the lines for each stanza type so that different stanzas can be saved
Intro = namedtuple("Intro", "lines")
Verse = namedtuple("Verse", "lines")
Chorus = namedtuple("Chorus", "lines")
Outro = namedtuple("Outro", "lines")

############### Function Defs ###############

'''
This function takes in a genre, and produces a Song struct with the format of a song
in the genre.
'''
def read_template(genre):
  
  filename = "template_" + genre.lower() + ".txt"
  fp = open(filename)

  outline = []

  for line in fp:
    #skip comment lines and empty lines
    if line[0] == "#" or len(line) == 1:
      continue

    new_stanza = Stanza([0,0],[0,0],[0,0])

    #strip the newline and separate into [Stanza type, constraints]
    line = line[0:-1]
    line = line.split(':')

    #for the outline, keep a list of strings containing the format to follow
    if line[0] == "Outline":
      for stanza in line[1].split(' '):
        outline.append(stanza)

    else:
      #save the type of stanza
      stanza_type = line[0]

      #process the format of the line
      line = line[1].split(' ')
      for i in range(0, len(line)):
        line[i] = line[i].split('-')

      #set each field in the new stanza
      new_stanza.num_lines[0] = int(line[0][0])
      new_stanza.num_lines[1] = int(line[0][1])

      new_stanza.num_words[0] = int(line[1][0])
      new_stanza.num_words[1] = int(line[1][1])

      new_stanza.num_syllables[0] = int(line[2][0])
      new_stanza.num_syllables[1] = int(line[2][1])


      #set the stanza in the song
      if stanza_type == "Intro":
        intro = new_stanza
      elif stanza_type == "Chorus":
        chorus = new_stanza
      elif stanza_type == "Verse":
        verse = new_stanza
      elif stanza_type == "Outro":
        outro = new_stanza
      else:
        print ("Something bad happened")

  fp.close()

  #build and return the Song
  song = Song(intro, chorus, verse, outro, outline)
  return song


'''
Returns a line and the next word
'''
def write_line(song_structure, starting_word, num_words_min, num_words_max):
  word = starting_word

  num_words = randint(num_words_min, num_words_max)

  line = ""
  syllables_used = 0
  words_used = 0
  structure = []

  if (len(song_structure) == 0):
  
    grammar = create_cfg()
    
  
    for sentence in generate(grammar, depth=num_words):
      if (len(sentence) == num_words):
        structure = sentence[1:]

  else:
    structure = song_structure

  i = 0
  line = starting_word + " "
  while i < len(structure):
    pos = structure[i]
    next_word = word_generator.next_words(word, pos, "country", 'probability')
    try:
      print(word + " ( " + str(i) + " / " + str(len(structure)) + " ) ")
    except UnicodeEncodeError:
      print("error")

    if "'" in next_word or next_word in [",", ".", "?", "!"]:
      line = line[0:-1]
      line = line + next_word + " "
      next_word = word_generator.next_words(next_word, "", "country", 'probability')
      
    line = line + next_word + " "
    word = next_word
    i = i + 1

  try:
    print(word)
  except UnicodeEncodeError:
    print("error")
    
  word = word_generator.next_words(word, "", "country", 'probability')
  
  
  print(structure)
  try:
    print(line)
  except UnicodeEncodeError:
    print("error")
  return line, word

'''
This function takes in a genre of a song to write, generates a song,
and writes the output to the file specified by filename

Supported genres:
  "country"
'''
def compose_song(genre, filename):
  song_format = read_template(genre)
  
  #initialize each stanza as "null"
  intro = Intro([])
  chorus = Chorus([])
  verse = Verse([])
  outro = Outro([])

  word = input("Input the starting word of the hook: ")
  #write the hook and the Word After Hook
  hook, w_a_h = write_line([], word, song_format.Chorus.num_words[0], song_format.Chorus.num_words[1])
                          #song_format.Chorus.num_syllables[0], song_format.Chorus.num_syllables[1])

  #no constraints on what an Intro should look like
  if "Intro" in song_format.Outline:
    #get the starting word of the stanza
    word = input("Input the starting word of the Intro stanza: ")

    #determine the number of lines in the stanza
    num_lines = randint(song_format.Intro.num_lines[0], song_format.Intro.num_lines[1])
    for i in range(0, num_lines):
      line, word = write_line([], word, song_format.Intro.num_words[0], song_format.Intro.num_words[1])
                   #song_format.Intro.num_syllables[0], song_format.Intro.num_syllables[1])

      intro.lines.append(line)

  #Chorus
  if "Chorus" in song_format.Outline:

    #determine the number of lines in the stanza
    num_lines = randint(song_format.Chorus.num_lines[0], song_format.Chorus.num_lines[1])

    for i in range(0, num_lines):
      #insert the hook every two lines, and get the Word After Hook to continue
      if i%2 == 0:
        chorus.lines.append(hook)
        word = w_a_h
      #write a line normally
      else:
        line, word = write_line([], word, song_format.Chorus.num_words[0], song_format.Chorus.num_words[1])
                            #song_format.Chorus.num_syllables[0], song_format.Chorus.num_syllables[1])
        chorus.lines.append(line)

  #Verse
  if "Verse" in song_format.Outline:
    #get the starting word of the verse
    word = input("Input the starting word of the Verse stanza: ")

    #determine the number of lines in the stanza
    num_lines = randint(song_format.Verse.num_lines[0], song_format.Verse.num_lines[1])
    for i in range(0, num_lines):
      line, word = write_line([], word, song_format.Verse.num_words[0], song_format.Verse.num_words[1])
                   #song_format.Verse.num_syllables[0], song_format.Verse.num_syllables[1])

      verse.lines.append(line)

  #Outro
  if "Outro" in song_format.Outline:
    #get the starting word of the last line
    word = input("Input the starting word of the last line of the Outro stanza: ")
    
    #determine the number of lines in the stanza
    num_lines = randint(song_format.Outro.num_lines[0], song_format.Outro.num_lines[1])

    for i in range(0, num_lines - 1):
      outro.lines.append(hook)
    line, word = write_line([], word, song_format.Outro.num_words[0], song_format.Outro.num_words[1])
                        #song_format.Outro.num_syllables[0], song_format.Outro.num_syllables[1])
    outro.lines.append(line)
      
        
  song = []
  for stanza in song_format.Outline:
    if stanza == "Intro":
      for line in intro.lines:
        song.append(line)
      song.append("")
    elif stanza == "Chorus":
      for line in chorus.lines:
        song.append(line)
      song.append("")
    elif stanza == "Verse":
      for line in verse.lines:
        song.append(line)
      song.append("")
    elif stanza == "Outro":
      for line in outro.lines:
        song.append(line)
      song.append("")

  if (filename != ""):
    file_write = open(filename, "w")
    for line in song:
      file_write.write(line)
      file_write.write("\n")
    file_write.close()

  return song

def create_cfg():
  grammar = nltk.CFG.fromstring("""
    S -> NP VP
    PP -> P NP
    NP -> Det N | Det N PP | JJ N | JJ N PP | Det JJ N | Det JJ N PP
    VP -> V NP | VP PP
    Det -> 'DT'
    N -> 'NN@NNS@NNP@NNPS@PRP@PRP$'
    V -> 'VB@VBD'
    P -> 'IN'
    JJ -> 'JJ@JJR@JJS'
    """);
  return grammar


#####MAIN - TODO: delete this for final purposes - It's only for testing #####

song = compose_song("country","generic_output.txt")
for line in song:
  try:
    print (line)
  except UnicodeEncodeError:
    continue
#song = read_template("country")
#print song
