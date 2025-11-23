"""
Trigram (Markov Chain) Autocomplete
=====
  The classic trigram model for text prediction, using a sliding window approach to learn patterns from a given dataset.
  This code reads a dataset, processes it to extract trigrams, and allows for text prediction based on learned patterns.
  The dataset used is my own writing since i dont know any public domain datasets.
"""

import time

BLANK = '<Void>'
STOP  = '<EOS>'
MAXGUESS = 10 # number of guesses to show

# the place to store learned patterns (context, result, occurrence count)
class DATA:
  def __init__(self, preliminary, result, occurance):
    self.prelim = preliminary  # Tuple of 3 context words (e.g., ('this', 'is', 'a'))
    self.result = result       # The predicted word (e.g., 'test')
    self.occurance = occurance

# dataset
dataset = """Lorem Ipsum Dolor Sit Amet"""

data = []
data = [BLANK, BLANK] + data # add initial BLANKs for context
oldlib = {} 
library = [] # List to store DATA objects

# tokenizing the dataset into a list of words.
for word_token in dataset.lower().split():
  
  # separate sentences by punctuation
  if ('!' in word_token) or ('?' in word_token) or ('.' in word_token):
    cleaned_word = word_token.replace('!','').replace('?','').replace('.','')
    
    if cleaned_word: # Add the cleaned word if it's not empty
      data.append(cleaned_word)
      
    data.append(STOP) # Mark end of sentence
    data.extend([BLANK, BLANK])
    
  else:
    
    data.append(word_token.replace(',','').replace('"',''))

# sliding window algorithm to count trigrams
for i in range(len(data) - 2):
  
  current_block_tuple = tuple(data[i:i+3]) # window

  # filter out blocks where any of the context words is a STOP token
  if STOP not in list(current_block_tuple[:2]):
    if current_block_tuple not in oldlib:
      oldlib[current_block_tuple] = 1
    else:
      oldlib[current_block_tuple] += 1

# convert the dictionary into a list of DATA objects for easier handling
for block_tuple, occurance_count in oldlib.items():
  
  library.append(DATA(block_tuple[:2], block_tuple[2], occurance_count))
  #                   prelim         , result        , occurance

# start the program
print(f"> Number of trigrams learned: {len(oldlib)}")
print("--------------------------------------------------")
print("> Start typing (type 'help()' for information):")
current_input_words = [BLANK, BLANK]

while True:
  
  display_input = [w for w in current_input_words if w != BLANK]
  print(" ".join(display_input), end=' ')

  user_raw_input = str(input("")).strip().lower()

  if user_raw_input == "exit()":
    print("> Exiting...")
    break
  
  elif user_raw_input == "clear()":
    current_input_words = [BLANK, BLANK]
    print("--------------------------------------------------")
    print("> Start typing (type 'help()' for information):")
    continue
  
  elif user_raw_input == "help()":
    print("""
  > Available commands:
  - 'exit()' to exit the program.
  - 'clear()' to clear the current context.
  - 'help()' to display this help message.
    """)
    print("--------------------------------------------------")
    print("> Start typing (type 'help()' for information):")
    continue

  elif not user_raw_input: # predict based on current context if user returns nothing
    pass
  
  else:
    
    # Process user's new input
    processed_user_words = []
    for w in user_raw_input.split():
      if ('!' in w) or ('?' in w) or ('.' in w):
        
        cleaned_word = w.replace('!','').replace('?','').replace('.','')
        
        if cleaned_word:
          processed_user_words.append(cleaned_word)
          
        # After a sentence ends, reset the context for the next prediction
        processed_user_words.append(STOP)
        current_input_words = [BLANK, BLANK]
        
      else:
        processed_user_words.append(w.replace(',','').replace('"',''))
    
    # Update by adding new words and keeping only the last 3 for context
    current_input_words.extend(processed_user_words)
    current_input_words = current_input_words[-2:]

  prediction_context_tuple = tuple(current_input_words)

  options = [] # reset options
  total_confidence = 0 # reset confidence

  # matching options from the library
  for item in library:
    if item.prelim == prediction_context_tuple:
      options.append(item)

  # sort options by occurrence
  options = sorted(options, key=lambda d: d.occurance, reverse=True)

  # calculate total occurrences for confidence percentage
  for block_option in options:
    total_confidence += block_option.occurance

  # output prediction
  print(f"{ ' '.join([w for w in current_input_words if w != BLANK]) } _____ \n")

  if not options:
    print("No guesses available for this context.")
    print("--------------------------------------------------")
  else:
    print(f"{len(options)} total guesses, showing {MAXGUESS}")
    print("--------------------------------------------------")

    count = 0
    for item in options:
      count += 1
      output_str = f"guess: {item.result:<20}"
      
      percentage = (item.occurance / total_confidence) * 100 if total_confidence > 0 else 0
      print(f"{output_str} | Confidence = {round(percentage, 3)}%")

      if count >= MAXGUESS:
        break
    print("--------------------------------------------------")

  time.sleep(0.5)


