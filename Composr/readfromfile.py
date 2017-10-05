import json


#build the dict, takes in the file name as param
def buildDict(s):
  fp = open(s, "r")
  dictionary = {}
  linesInFile = []
  for line in fp:
    newLine = line.split('@')
    linesInFile.append(newLine)

  length = len(linesInFile)
  for i in range(0,length):
    #new innerDict for using the insidedict 
    innerDict = {}
    x = 1 
    y = 2
    lenOfLine = len(linesInFile[i])-1
    while( y < lenOfLine):
      #create a dict out of a new word
      innerDict.update({linesInFile[i][x]: linesInFile[i][y]})
      x = x + 2
      y = y + 2
    #add the new dict to the overall dict
    dictionary.update({linesInFile[i][0]: innerDict}) 

  return dictionary



# uncomment this to print the dict nicely
'''
  print ( json.dumps(dictionary, indent=2))
  
'''
