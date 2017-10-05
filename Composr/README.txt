-------------README.txt-------------

This file outlines what the purpose of each file in our repo is.


-------------artists.txt-------------

This file contains 565 country artists which is fed into frequency_generator.py in order to get the bigram frequencies of all the words appearing in the songs of those artists.


-------------composr.py (THIS FILE IS USED TO RUN OUR PROGRAM)-------------

This is where the lyrics are constructed. This is the file you must run in order to create a song. It is run be typing in the following at the command prompt: "python composr.py". When prompted for a word the user must enter a word that has appeared at least once in the over 30,000 songs we sampled from (essentially no made up words). 


-------------country_bigram_output.txt-------------

This is the output from frequency_generator.py that contains every word that appears in the lyrics and every following word with a frequency of how many times it follows. This file is then fed into readfromfile.py so that the bigram frequencies can be used in composr.py.


-------------frequency_generator.py-------------

This file reads in a list of artists and outputs a file containing the bigram frequencies of all the songs of all the artists.


-------------new_PyLyrics.py-------------

This file is an updated version of PyLyrics that can successfully get the lyrics to a song using the artist name and song name. It can also get all the albums of an artist and all the songs on an album.


-------------readfromfile.py-------------

This python file is used to read in the bigram frequencies file and reconstruct the data structure that contains all the words and their following words to be used in composr.py.


-------------song_pos.py AND syllables.py-------------

These two files were used to get all the POS tags from a song and get the syllables in a line respectively. They were no eventually used in our final product.


-------------word_generator.py-------------

This python file contains a function that allows you to input the previous word and the current POS tag and get a word that is that POS and is likely to come after the previous word.

