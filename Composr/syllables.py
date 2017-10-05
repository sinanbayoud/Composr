from nltk.corpus import cmudict

dic = cmudict.dict()

'''
This function takes in an English word and returns the number of syllables.

If the word is not valid, -1 is returned instead

Examples: num_syllables("bonanza") = 3
          num_syllables("merry-go-round") = 4
          num_syllables("blarg") = -1
'''
def num_syllables(word):
  global dic

  try:
    sounds = dic[word.lower()][0]
  except KeyError:
    return -1

  count = 0
  for i in range(0, len(sounds)):
    if sounds[i][-1].isdigit():
      count = count + 1
  return count

