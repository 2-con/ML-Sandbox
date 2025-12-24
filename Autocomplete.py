"""
Autocomplete
=====
  A trigram model for autocompleting text input. its similar to the trigram model made,
  just an earlier version of the code, but with a few changes.
"""

print("start typing")
word = ""
while True:
  print(word,end='')
  word = word + str(input("")) + " " # Input
  dataset = "lorem ipsum dolor sit amet" + word
  data = []       # dataset turned into a list of words

  oldlib = {}     # dictionary of blocks along with occurances for analysis
  block = []      # chunks of words to be analysed
  library = []    # oldlib but stores objects instead

  options = []    # options but stores objects
  confidence = 0  # how 'confident' the guess is

  padding = ""    # padding the confidence to look nicer
  output = ""     # AI's guess as an f-string

  # constants
  BLANK = '<VOID>'
  STOP  = '<EOS>'
  MAXGUESS = 10

  # initiating classes
  class DATA:
    def __init__(self,preliminary,result,occurance):
      self.prelim = preliminary
      self.result = result
      self.occurance = occurance

  # initiating functions
  def exist(list,word):
    for i in list:
      if i == word:
        return True
    return False

  # grabs all the words and turns them into a list of words
  for i in dataset.lower().split():
    # seperate sentences by punctuation since you can say 2 non-related ideas
    if ('!' in i) or ('?' in i) or ('.' in i):
      data.append(i.replace('!','').replace('?','').replace('.',''))
      data.append(STOP)
      data.append(BLANK)
    else:
      data.append(i.replace(',','').replace('"',''))

  data = [STOP,BLANK] + data
  # scans the dataset (and input) and seperate them into blocks
  for i in range(len(data)-2):
    block = data[i:i+3]

    # filters out blocks with STOP in the last or 2nd place
    if exist(block[1:],STOP): #block[-1] == STOP or block[-2] == STOP:
      pass
    else:
      # check if there's an identical block, if not add a new entry, if so update occurance
      if tuple(block) not in oldlib:
        oldlib[tuple(block)] = 1
      else:
        oldlib[tuple(block)] += 1

  # converting dictionary into a list of objects
  for i in oldlib:
    library.append(DATA(i[:2],i[-1],oldlib[i]))

  # scans the object list for options
  for item in library:
    if item.prelim == tuple(block[1:]):
      options.append(item)

  # sort out options based on occurances
  options = list(sorted(options, key=lambda DATA: DATA.occurance, reverse=True))

  # calculating confidence
  for block in options:
    confidence += block.occurance

  # output
  print(f"{word} _____ \n")
  print(f"{len(options)} guess" if len(options) == 1 else f"{len(options)} total guesses, showing 10")
  print("------------------")

  count = 0

  # show potential guesses
  for item in options:
    count+=1

    # padding the output to look nicer
    padding = ""
    output = f"guess: {item.result}" + padding
    while len(output) < 25: # pads the output
      padding = padding + " "
      output = f"guess: {item.result}" + padding

    if count == 10:
      break

    print(output + f"| Confidence = {round((item.occurance/confidence)*100,3)}%")