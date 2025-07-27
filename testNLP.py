"""
Test Natural Language Processing (NLP)
=====
  This module contains functions and classes for processing natural language inputs, particularly for mathematical operations, definitions, and Wikipedia queries. 
  It includes packet organization, mathematical evaluation, Wikipedia search functionalities and other unused and redundant functions. 
  It is unconventional to include a subjective summary of the module, however, this whole module can be described as a disaster.
"""

# imports

import re
import time
from sympy import sympify, lambdify, Symbol
import random
import wikipedia
import math
from fractions import Fraction
from nltk.corpus import wordnet

# classes

class pack: # organizes packets
  def __init__(self, sentence, mode):
    self.item = sentence
    self.mode = mode

class querypack: # organizes packets for wikipedia
  def __init__(self, search_query, return_type):
    self.item = search_query
    self.type = return_type
    
class pack_definition: # organizes packets for definitions
  def __init__(self, definition, synonym):
    self.definition = definition
    self.synonym = synonym

# functions

def is_operation(string : str) -> bool: # checks wether the input is an operation or not
  if re.match(r"^[0-9\.\+\-\*/\(\)\s]*$", string):
    try:
      eval(string)
      return True
    except:
      pass
  elif any(func in string for func in [
      "sin", "cos", "tan", "csc", "sec", "cot",
      "asin", "arcsin", "arsin",
      "acos", "arccos", "arcos",
      "atan", "arctan", "artan",
      "acsc", "arccsc", "arcsc",
      "asec", "arcsec", "arsec",
      "acot", "arccot", "arcot",
      "sinh", "cosh", "tanh", "csch", "sech", "coth",
      "asinh", "arcsinh", "arsinh",
      "acosh", "arccosh", "arcosh",
      "atanh", "arctanh", "artanh",
      "acsch", "arccsch", "arsech",
      "arcosh", "arccosh", "arcosh",
      "acoth", "arccoth", "arcot",
      "log", "sqrt", "exp", "ln"]):
    return True
  else:
    return False

def display(string : str) -> None: # displays a string in a fancy way
  print("┃ ", end='')
  count = 0
  for i in string.split():
    count += 1
    time.sleep(0.05)
    
    print(i, end=' ', flush=True)
    
    if count > 18:
      count = 0
      print()
      print("┃ ", end='')
  print()

def solve(equation : str) -> int: # solves a string equation
  # try solving it
  equation = equation.replace('pi', str(math.pi))

  if "log" in equation:
    try:
      # finds the base
      start_index = equation.index("log") + len("log")
      end_index = equation.index("(", start_index)
      base = equation[start_index:end_index]

      # finds the value
      start_index = equation.index("(") + len("(")
      end_index = equation.index(")", start_index)
      value = equation[start_index:end_index]
      return lambdify(Symbol('x'), sympify(f"log({value}, {base})"))(Symbol('x'))
    except Exception as e:
      return "ERROR: Formatting error for 'log' - check inside the parentheses"

  try:
    answer = lambdify(Symbol('x'), sympify(equation))(Symbol('x'))
    return answer

  # if it fails
  except:
    # check if its an equation
    for i in range(len(equation)):
      if equation[i] == "=":
        return lambdify(Symbol('x'), sympify(equation[:i]))(Symbol('x')) == lambdify(Symbol('x'), sympify(equation[i+1:]))(Symbol('x'))

    # if its none of the above, abort
    return None

def check_connection() -> bool: # checks if connection is established
  try:
    wikipedia.page("Python (programming language)")
    return True
  except Exception:
    return False

def reconnect(times : int) -> bool:
  for i in range(times):
    if check_connection():
      return True
  return False

def get_definition(word: str) -> list:
  synsets = wordnet.synsets(word)
  answers = []

  if synsets:
    for synset in synsets:
      #print(f"Definition: {synset.definition()}")
      #print(f"Synonyms: {[lemma.name() for lemma in synset.lemmas()]}")
      #print("-" * 20)
      
      answers.append(pack_definition(synset.definition(), [lemma.name() for lemma in synset.lemmas()]))
      
  else:
    #print(f"Definition not found for '{word}'.")
    return ("Unknown", None)
    
  return answers

def get_link(pagename: str) -> str:
  try:
    return wikipedia.page(pagename).url
  except wikipedia.exceptions.PageError:
    return "failed to retrieve link"
  except wikipedia.exceptions.DisambiguationError:
    return "failed to retrieve link"

def get_summary(pagename: str, length: int) -> str:
  try:
    return wikipedia.summary("a " + pagename, sentences=length)
  except wikipedia.exceptions.PageError:
    return "could not find summary"
  except wikipedia.exceptions.DisambiguationError as e:
    return f"Multiple results found. Please specify: {', '.join(e.options[:5])}"

def get_results(userinput: str, maxresults: int) -> list:
  #userinput = "a " + userinput
    
  link = [] # list of links
  results = [] # list of results
  count = 0 # while loop counter
  count2 = 0 # while loop counter for duplicates

  # main

  wikipedia.set_lang("en")

  # try to search, if fails use autorcorrect
  try:
    results = wikipedia.search(userinput, results = maxresults)
  except:
    results = wikipedia.search(wikipedia.suggest(userinput), results = maxresults)

  for i in results:
    try:
      link.append(wikipedia.page(i).url)
    except:
      link.append("failed to retrieve link")
      
  # parse through URLS and results, remove duplicates
  while count+1 < len(link):
    count2 = len(link) - 1
    while count2 > count:
      if link[count] == link[count2]:
        link.pop(count2)
        results.pop(count2)
      count2 -= 1
    count += 1
    
  # remove those 'disabiguation' thingys
  temp = []
  for i in results:
    if '(disambiguation)' not in i:
      temp.append(i)
  results = temp[:]
  
  return results

####################################################################
#                  Packet evaluator / delegator                    #
####################################################################
def packet_evaluator(sentence : list) -> str:
  
  instances = [
    ["math", "define", "inquiry", "chatting"],
    [0, 0, 0, 0]
  ]
  
  CHATTING_KEYWORDS = {
    "your"            , "youre"         , "you're"        , "chatbot"         , "you"         ,
    "i"               , "my"            , "mine"          , "im"              , "i'm"         ,
    "we"              , "us"            , "how"           , "hows"            , "how's"       ,
    "feel"            , "feeling"       , "felt"          , "thrilled"        , "ecstatic"    ,
    "thought"         , "thoughts"      , "delighted"     , "satisfied"       , "pleased"     ,
    "opinion"         , "opinions"      , "indifferently" , "apathetically"   , "annoyed"     ,
    "what"            , "whats"         , "what's"        , "offensively"     , "thrillingly" ,
    "cool"            , "awesome"       , "happy"         , "joyful"          , "excited"     , 
    "exciting"        , "delighting"    , "satisfying"    , "thrilling"       , "pleasing"    ,
    "pleased"         , "excitingly"    , "delightfully"  , "satisfactorily"  , "me"          ,
    "disappointed"    , "upset"         , "angry"         , "frustrated"      ,
    "disappointing"   , "frustrating"   , "annoying"      , "miserably"       ,
    "disappointedly"  , "frustratingly" , "annoyingly"    , "depressing"      ,
    "neutral"         , "indifferent"   , "apathetic"     , "content"         ,
    "attacked"        , "offended"      , "attacking"     , "offending"       ,
    "sad"             , "unhappy"       , "depressed"     , "miserable"       
  }

  RESEARCH_KEYWORDS = {
    "list"    , "show"      , "find"        , "tell"          ,
    "search"  , "research"  , "information" , "explain"       ,
    "summary" , "summarise" , "summarize"   , "explaination"  ,
    "who"     , "whos"      , "whose"       , "who's"         ,
    "what"    , "whats"     , "what's"      , "overview"      , 
    "where"   , "wheres"    , "where's"     , "information"   ,
    "when"    , "whens"     , "when's"      ,
    "analyze" , "overview"  , "analysis"
  }

  MATH_KEYWORDS = {
    "calculate" , "solve"     , "evaluate"  , "compute",
    "fraction"  , "fractions" , "determine" ,
    "what"      , "whats"     , "what's"    ,
    "+", "-", "*", "/", "^", "**"
  }

  DEFINITION_KEYWORDS = {
    "define"  , "definition"  , "definitions" ,
    "synonym" , "synonyms"    , "meaning"     , "mean", "refer",
    "what"    , "whats"       , "what's"
  }

  # automatic return since there is no reason to do this
  if any(word in sentence for word in ("offensive_word1", "offensive_word2")):
    return "offensive"
  
  if sentence[0] in ("/system", "$system"):
    return "system"

  # counts up words in the sentence
  for i in sentence:
    if (i in MATH_KEYWORDS) or is_operation(i):
      instances[1][0] += 1

    if i in DEFINITION_KEYWORDS:
      instances[1][1] += 1

    if i in RESEARCH_KEYWORDS:
      instances[1][2] += 1

    if i in CHATTING_KEYWORDS:
      instances[1][3] += 1
  
  # finds the highest occurrence
  category = instances[0][instances[1].index(max(instances[1]))]
  
  # counts up words in the sentence
  if category == "math":
    return "math"
  
  if category == "define":
    return "define"
    
  if category == "inquiry":
    return "inquiery"

  if category == "chatting":
    return "chatting"

  return "unknown"

####################################################################
#                            Math mode                             #
####################################################################
def math_interpreter(userinput : str, DEBUG : bool) -> None: # math mode, only prints

  greeting = "" # start of the answer

  block = [] # formatting block
  sentence = [] # sentence to be interpreted and processed, the 'block'

  sentences         = [] # userinput
  sentences_layer1  = [] # filter out non-keyword
  sentences_layer2  = [] # fix logic, remove None comparisons
  sentences_layer3  = [] # formatting AND
  sentences_layer4  = [] # joins lone formulas
  sentences_layer5  = [] # remove nonsensical instruction blocks
  sentences_layer6  = [] # transform instruction blocks based on first keyword
  sentences_layer7  = [] # calculates the thing

  sentence_context = [] # adds further context to the sentence
  sentences_modifier = [] # adds further context to the sentences

  ands = [0,-1] # for fragmenting AND
  dontwrite = False # overrides whether to write or ignore an item
  default = True # wether the sentence should be interpreted as a default or if there is further context

  option_num = 0
  correct = True
  compare_with = ''
  saycompare = False
  which_one = 0
  request_for_fraction = False
  request_for_possible = False
  error = True # checks for errors

  # constants

  VOID = "{{SENTENCE||VOID}}" # temporary item, not ment to be seen

  # explicit command request
  COMMAND_KEYWORDS = ("calculate", "solve", "evaluate", "compute", "determine")
  QUESTION_KEYWORDS = ("what", "whats")
  EXPLAIN_KEYWORDS = ("why", "prove")
  QUESTION_COMPARE_KEYWORDS = ("is", "are")

  EXPLICIT_REQUESTS = COMMAND_KEYWORDS + QUESTION_KEYWORDS + EXPLAIN_KEYWORDS + QUESTION_COMPARE_KEYWORDS

  # external modifiers
  COMPARE_KEYWORDS = ("orNULL", "and")

  # contextual modifiers
  POSSIBLE = ("possible", "impossible")
  FRACTION = ("fraction", "fractions")

  NUMBERS_KEYWORDS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
  OPERATORS_KEYWORDS = ("+", "-", "*", "/", "^", "**")

  KEYWORDS = EXPLICIT_REQUESTS + COMPARE_KEYWORDS + NUMBERS_KEYWORDS + OPERATORS_KEYWORDS + tuple(VOID)

  ####################################### processing

  print("----------- DEBUGGING - will not be shown --------------------\n" if DEBUG else "", end='')

  # converts to a list of lists based off sentence
  for i in userinput.lower().split():

    decimal = False

    # if theres a dot, check if its decimal or not
    if '.' in i: # if theres a dot

      for b in range(len(i)): # loop through the word
        if (i[b] == '.') and (i[b-1] in NUMBERS_KEYWORDS) and (i[b+1] in NUMBERS_KEYWORDS): # if theres a dot, and the things around it are numbers
          decimal = True
          break

        else:
          decimal = False

      if decimal:
        sentence.append(i)
      else:
        sentence.append(i.replace('.',''))
        sentences.append(sentence)
        sentence = []

    # seperate sentences by punctuation since you can say 2 non-related ideas
    elif ('!' in i) or ('?' in i) or ('█' in i):
      sentence.append(i.replace('!','').replace('?','').replace('█',''))
      sentences.append(sentence)
      sentence = []

    else:
      sentence.append(i.replace('\'','').replace(",", ""))

  print(f"Layer 0 | {sentences}\n" if DEBUG else "", end='')

  #                 filters non-keywords - layer 1                   #

  for a in range(len(sentences)):
    default = True

    for b in range(len(sentences[a])):
      # append the word to SENTENCE if its a keyword
      if (sentences[a][b] in KEYWORDS) or (sentences[a][b][0] in NUMBERS_KEYWORDS) or (is_operation(sentences[a][b])):
        sentence.append(sentences[a][b])

      # keeps notes of important words in a seperate layer
      elif (sentences[a][b] in POSSIBLE) or (sentences[a][b] in FRACTION):
        sentence_context.append(sentences[a][b])
        default = False

    if default:
      sentence_context.append(None)

    sentences_layer1.append(sentence)
    sentences_modifier.append(sentence_context)

    sentence_context = []
    sentence = []

  # filters repeats

  # filters out adjacent repeats
  for a in range(len(sentences_layer1)):
    for b in range(len(sentences_layer1[a])-1):

      if sentences_layer1[a][b] == sentences_layer1[a][b+1]: # replaces adjacent repeats with VOID
        sentences_layer1[a][b] = sentences_layer1[a][b].replace(sentences_layer1[a][b],VOID)

  # finishes replacing repeats, transfers to layer 2
  for a in range(len(sentences_layer1)):
    for b in range(len(sentences_layer1[a])):
      if sentences_layer1[a][b] != VOID: # only appends non VOID
        sentence.append(sentences_layer1[a][b])

    sentences_layer2.append(sentence)
    sentence = []

  # final fixing and repairs
  if len(sentences) > 1:
    sentences_modifier = sentences_modifier[:-1] # deletes the last item since the last item is an easter egg / function block

  sentences_layer1 = sentences_layer2[:] # fixes sentence layer 1 after deleting repeats
  sentences_layer2 = [] # clears for its intended use

  # debug
  print(f"\nLayer 1 | {sentences_layer1}\n" if DEBUG else "", end='')

  print(f"Context | {sentences_modifier}\n" if DEBUG else "", end='')

  error = True

  for i in sentences_layer1:
    if i != []:
      error = False

  if error:
    display("Im sorry, but i cannot understand/interpret your request")
    display("ERROR 101: Null requests")
    return None

  #     filters sentences by logic and fixes mistakes - layer 2      #

  for a in range(len(sentences_layer1)):

    # scans and ignores empty sentences
    ignore_sentence = False
    if sentences_layer1[a] == []: # if its an empty list
      ignore_sentence = True

    for b in range(len(sentences_layer1[a])):
      dontwrite = False

      # removes illogical comparisons - IS, ARE
      if sentences_layer1[a][b] in QUESTION_COMPARE_KEYWORDS:
        # if its at the end of sentence
        if b+1 > len(sentences_layer1[a])-1:
          dontwrite = True

        # if the next 2 items are not numbers
        elif not (is_operation(sentences_layer1[a][b+1]) or is_operation(sentences_layer1[a][b+2])):
          dontwrite = True

      # removes illogical requests
      elif sentences_layer1[a][b] in EXPLICIT_REQUESTS:
        # if its at the end of sentence
        if b+1 > len(sentences_layer1[a])-1:
          dontwrite = True

      # end of layer processing
      if not dontwrite:
        sentence.append(sentences_layer1[a][b])

    # only appends if there is purpose behind the sentence
    if not ignore_sentence:
      sentences_layer2.append(sentence)

    sentence = []

  print(f"\nLayer 2 | {sentences_layer2}\n" if DEBUG else "", end='')

  error = True

  for i in sentences_layer2:
    if i != []:
      error = False

  if error:
    display("Im sorry, but i dont know what to do")
    display("ERROR 102: Unknown instruction")
    return None

  #         formatting for AND / AND fragmentation - layer 3         #

  for a in range(len(sentences_layer2)):
    ands = [0]  # Reset ands for each sentence

    for i in range(len(sentences_layer2[a])):
      if sentences_layer2[a][i] == 'and':
        ands.append(i)

    ands.append(len(sentences_layer2[a]))  # Add the end of the sentence as the last index

    # fragmentation by AND
    count = 0
    if 'and' in sentences_layer2[a]:
      for i in range(len(ands)-1):
        block = sentences_layer2[a][ands[count]:ands[count+1]] # makes sets up a block for processing

        # Remove 'and' if it's the first element in the block
        if block and block[0] == 'and':
          block.pop(0)

        sentences_layer3.append(block)
        count += 1

    # if the sentence does not contain an AND, just append it as a whole
    else:
      for b in range(len(sentences_layer2[a])):
        sentence.append(sentences_layer2[a][b])

      sentences_layer3.append(sentence)
      sentence = []

  print(f"\nLayer 3 | {sentences_layer3}\n" if DEBUG else "", end='')

  #           joins via operators - layer 4            #

  sentences_layer4 = sentences_layer3[:]
  
  for adsdasadsasdasdasd in range(2):
    for a in range(len(sentences_layer4)):
      word = 0
      while word < len(sentences_layer4[a]): # repeat while its not the last word
        
        # if there is an operator, join the previous and next word
        if sentences_layer4[a][word] in OPERATORS_KEYWORDS: 
          combined = ''.join(sentences_layer4[a][word-1:word+2])
          sentences_layer4[a][word] = combined
          sentences_layer4[a][word-1] = VOID # replace with VOID t be removed
          sentences_layer4[a][word+1] = VOID

          for i in sentences_layer4[a]: # removes voids
            if i != VOID:
              sentence.append(i)
          
          sentences_layer4[a] = sentence # update sentence
          sentence = []
          
        word += 1 # update word index
  
  """while i < len(sentences_layer3):
    sentences_layer4 = []

    # Check for lists with just operations and join them to the previous list
    for a in range(len(sentences_layer3)):
      if all(is_operation(word) for word in sentences_layer3[a]): # if the whole thing is just operations
        if a-1 >= 0:  # Check if there is a previous list
          sentences_layer3[a-1].extend(sentences_layer3[a])  # Join the operation-only list to the previous list
          #sentences_layer4.append(sentences_layer3[a-1])  # Append the joined list to layer 4
        else:
          sentences_layer4.append(sentences_layer3[a])  # If there is no previous list, append the operation-only list as is
      else:
        sentences_layer4.append(sentences_layer3[a])  # Append the non-operation list as is

    sentences_layer3 = sentences_layer4[:]
    i += 1"""

  print(f"\nLayer 4 | {sentences_layer4} \n" if DEBUG else "", end='')

  #       filter nonsensical instruction blocks - layer 5            #

  for a in range(len(sentences_layer4)):
    dontwrite = True
    for b in range(len(sentences_layer4[a])):
      # scans for explicit request keywords
      if sentences_layer4[a][b] in EXPLICIT_REQUESTS:
        # starts from there and scans through the entire block for operations
        for i in sentences_layer4[a][b:]:
          # if there is an operation, safe
          if is_operation(i):
            dontwrite = False
            break

          else: # too lazy to delcare in the block
            dontwrite = True

    if not dontwrite:
      sentences_layer5.append(sentences_layer4[a])

  print(f"\nLayer 5 | {sentences_layer5}\n" if DEBUG else "", end='')

  #       format into proper instruction blocks - layer 6            #

  for a in range(len(sentences_layer5)):
    dontwrite = False
    assumption = False
    for b in range(len(sentences_layer5[a])):

      # if the word is an explicit request
      if (sentences_layer5[a][b] in EXPLICIT_REQUESTS) and not dontwrite:
        dontwrite = True
        sentence.append(sentences_layer5[a][b])

        # scan the block and only append operations
        for i in sentences_layer5[a][b:]:
          if is_operation(i):
            sentence.append(i)

      # else if the instruction block does not have any explicit requests
      elif EXPLICIT_REQUESTS not in sentences_layer5[a] and not dontwrite:

        # assume its asking to evaluate and place it in from of the sentence
        if not assumption:
          sentence.append('calculate')
          assumption = True

        sentence.append(sentences_layer5[a][b])

    sentences_layer6.append(sentence)
    sentence = []

  print(f"\nLayer 6 | {sentences_layer6}\n" if DEBUG else "", end='')

  #                   delete repeats - layer 7                       #

  for a in range(len(sentences_layer6)-1):
    if sentences_layer6[a] == sentences_layer6[a+1]:
      pass
    else:
      sentences_layer7.append(sentences_layer6[a])

  sentences_layer7.append(sentences_layer6[-1]) # no choice but to append the last item

  print(f"\nLayer 7 | {sentences_layer7}\n" if DEBUG else "", end='')

  print("----------- DEBUGGING - will not be shown --------------------\n" if DEBUG else "", end='')

  # Output

  # greeting
  display(greeting)

  # actual answer
  for a in range(len(sentences_layer7)):

    if POSSIBLE in sentences_layer5[a]:
      display("wether it is possible or not depends on you definition, however heres what i understand")

    # if its asking to compute an equation then do it
    if (sentences_layer7[a][0] in COMMAND_KEYWORDS) or (sentences_layer7[a][0] in QUESTION_KEYWORDS):

      saycompare = False

      # scans through the blockk for calculations
      for b in range(len(sentences_layer7[a])-1):

        correct = False
        request_for_fraction = False

        # if its a calculation, proceed with the answer
        if sentences_layer7[a][b+1] not in NUMBERS_KEYWORDS:

          for i in sentences_modifier[a]:
            if i in FRACTION:
              request_for_fraction = True

          if request_for_fraction:
            display(f"{sentences_layer7[a][b+1]} = {Fraction(float(solve(sentences_layer7[a][b+1]))).limit_denominator()}")

          else:
            display(f"{sentences_layer7[a][b+1]} = {solve(sentences_layer7[a][b+1])}")

        # else if its a number, its probably asking to compare
        else:
          if saycompare == False:
            display(f"lets compare with our options")
            saycompare = True

          correct = solve(f"{sentences_layer7[a][1]}={sentences_layer7[a][b+1]}")
          display(f"{sentences_layer7[a][1]} = {sentences_layer7[a][b+1]} ({correct})")

    # else if its asking to compare, then compare options individually
    elif sentences_layer7[a][0] in QUESTION_COMPARE_KEYWORDS:

      option_num = 1
      correct = False
      which_one = 0
      compare_with = solve(sentences_layer7[a][1])
      request_for_fraction = False
      request_for_possible = False

      # context finders
      for i in sentences_modifier[a]:
        if i in FRACTION:
          request_for_fraction = True

      for i in sentences_modifier[a]:
        if i in POSSIBLE:
          request_for_possible = True

      display(f"lets evaluate {sentences_layer7[a][1]}")

      # if it asks for the fraction form, then say it in fraction form
      if (request_for_fraction and request_for_possible) or (request_for_fraction and not request_for_possible):
        display(f"  {sentences_layer7[a][1]} = {Fraction(compare_with).limit_denominator()}")

      else: # otherwise just say it as is
        display(f"  {sentences_layer7[a][1]} = {compare_with}")

      # post-evaluatuon

      if request_for_possible and not request_for_fraction:
        display("wether its possible or not depends on your definition")
        display("as far as i am concerned, this is a valid answer")

      elif request_for_fraction and request_for_possible:
        display("it is possible to display this as a fraction")

      elif request_for_fraction and not request_for_possible:
        display("here is the thing as a fraction")

      else:
        display("now lets compare with our options")

      # scans through the blockk for calculations
      for b in range(len(sentences_layer7[a])-2):

        if solve(f"{compare_with}={sentences_layer7[a][b+2]}"):
          correct = True
          which_one = option_num
        else:
          correct = False

        display(f"  {compare_with} = {sentences_layer7[a][b+2]} ({correct})")
        option_num += 1

      if which_one > 0:
        display(f"therefore option {which_one} is correct")

      # if the question is downright nonsensical, tell the user directly
      elif (option_num == 1) and (correct == False) and (which_one == 0) and not request_for_fraction:

        display("i dont know what to do with this, i interpreted this as an instruction to calculate")
        display("however, there is just so much i could get creative on before you need to learn basic grammar (or english)")

      # if its not nonsensical, then its just wrong
      else:
        # just makes sure not to print this if its a POSSIBLE question
        if sentences_modifier[a][0] not in POSSIBLE:
          display("none of the above is correct")

    # if its none of the above, then its probably asking WHY
    else:

      compare_with = solve(sentences_layer7[a][1])
      correct = solve(f"{sentences_layer7[a][2]} = {compare_with}")

      display("lets check if its correct or not")
      display(f"you stated that                      {sentences_layer7[a][1]} = {sentences_layer7[a][2]}")
      display(f"but if we evaluate                   {sentences_layer7[a][1]}, we get {compare_with}")
      display(f"and if we check with your statement, {sentences_layer7[a][2]} = {compare_with} ({correct})")

      display("")
      display(f"as seen above, this is {correct}.")
      if correct:
        pass # correct
        display("this is because of how mathematical operations works")
        display("for now i cannot explain things as im just evaluating and interpreting basic mathematical functions")
        display("however, i can search wikipedia for more information if you are interested")

      else:
        display("and since it is not true, there is nothing to evaluate")

  # ending
  display("")

####################################################################
#                        reaserch mode                             #
####################################################################
def reaserch_interpreter(userinput : str, DEBUG : bool, maxresults: int, sentence_length: int) -> None:
  sentence = [] # sentence to be interpreted and processed, the 'block'
  introduction = [] # the part of the sentence that might contain information about output formatting

  sentences         = [] # userinput
  sentences_layer1  = [] # remove easter egg
  sentences_layer2  = [] # remove grrammar modifier
  sentences_layer3  = [] # trimming the front until no more keywords
  sentences_layer4  = [] # trimming the back until no more bluff
  sentences_layer5  = [] # packing queries into packets
  
  sentences_layer6  = [] # for 'summary' response types
  sentences_layer7  = [] # for 'list' response types
  
  summary = "" # summary of the topic (if any)
  link = "" # link to a wikipedia page
  subject = "" # the subject of the question
  
  results = [] # list of results when searched
  links   = [] # list of links from the result 
   
  error = False
  
  in_depth = False # if asked for deep reaserch
  shallow = False # if asked for a shallow overview
  exaggerate = False # if asked to exaggerate
  
  # constants
  VOID = "{{SENTENCE||VOID}}" # temporary item, not ment to be seen
  
  POLITENESS_KEYWORDS = ("ty", "thx", "thanks", "you", "thank", "please", "me", "for")
  POLITENESS_AFTER_KEYWORDS = ("Chatbot", "man", "bro", "alr")  
  
  DESC_KEYWORDS = (
    "search", "reaserch", "overview", "comprehensive", "analysis", "information",
    "summary", "summarise", "summarize", "explain", "regarding"
    
    "who", "whos", "whose", "who's",
    "what", "whats", "what's",
    "where", "wheres", "where's",
    "when", "whens", "when's",
    
    "tell"
    )
  RESULT_KEYWORDS = ("list", "results", "show", "find")
  BLUFF = ("is", "me", "for")
  
  CAUSATION = ("caused ", "created ", "invented ", "on ", "regarding ", "of ", "concerning ", "about ", "from ", "by ")
  
  LONG_OUTPUT = ("comprehensive", "in-depth", "indepth", "analyze")
  SHORT_OUTPUT = ("breif", "breifly", "short", "shallow", "overview", "simplified", "oversimplified")
  EXAGGERATION = ("very", "highly", "super")
  
  ####################################################################
  #             splitting words - layer 0 (pre processing)           #
  ####################################################################
  
  for i in userinput.lower().split():
    # seperate sentences by punctuation since you can say 2 non-related ideas
    if ('!' in i) or ('?' in i) or ('.' in i) or ('█' in i):

      sentence.append(i.replace('!','').replace('?','').replace('.','').replace('█',''))
      sentences.append(sentence)
      sentence = []

    else:
      sentence.append(i.replace('\'','').replace(",", ""))

  # checks for errors / blank sentences
  error = True

  # if there isnn't a blank space, its not an error.
  for i in sentences:
    if i != []:
      error = False

  # if error, break
  if error:
    display("i dont know what to do with your request")
    display("ERROR 301: Null requests")
    return None

  print("----------- DEBUGGING - will not be shown --------------------\n" if DEBUG else "", end='')
  print(f"Layer 0 | {sentences}\n\n" if DEBUG else "", end='')
  
  ####################################################################
  #        get rid of common terms - layer 1 (pre processing)        #
  ####################################################################

  sentences_layer1 = sentences[:-1] # get rid of the easter egg
  
  print(f"Layer 1 | {sentences_layer1}\n\n" if DEBUG else "", end='')
  
  ####################################################################
  #     removes modifiers and bluff - layer 2 (pre processing)       #
  ####################################################################
  
  for a in sentences_layer1:
    sentence = []
    for b in a:
      # remove bluff words that are likely just there for grammar purposes
      if b not in BLUFF:
        sentence.append(b.replace(r"'s",""))
  
    sentences_layer2.append(sentence)
    
  print(f"Layer 2 | {sentences_layer2}\n\n" if DEBUG else "", end='')
  
  ####################################################################
  #   scans for keywords and delete everything before it - layer 3   #
  ####################################################################
  
  for a in sentences_layer2:
    sentence = []
    for b in range(len(a)):
      
      # if it matches any of the keywords, sentence will be the exact sentences but up to that keyword      
      if (a[b] in DESC_KEYWORDS) or (a[b] in RESULT_KEYWORDS):
        sentence = a[b:]
        introduction = a[:b]
  
    sentences_layer3.append(sentence)
  
  # checks for errors / blank sentences
  error = True

  # if there isnn't a blank space, its not an error.
  for i in sentences:
    if i != []:
      error = False

  # if error, break
  if error:
    display("Im sorry, but i cannot understand/interpret your request")
    display("ERROR 302: No keywords")
    return None
  
  print(f"Layer 3 | {sentences_layer3}\n\n" if DEBUG else "", end='')
  print(f"Layer 3 INTRO | {introduction}\n\n" if DEBUG else "", end='')
  
  ####################################################################
  #   context expansion at the end to remove more bluff - layer 4 A  #
  ####################################################################
  
  for a in sentences_layer3:
    sentence = a
    
    try:
      # this process is in reverse. dont forget that
      count = -1 
      # finds wether the word is either a [politeness] or an [after]. if so, it scans the previous word if its either of them. and then it shortens.
      while (a[count] in POLITENESS_KEYWORDS) or (((a[count-1] in POLITENESS_KEYWORDS) or (a[count-1] in POLITENESS_AFTER_KEYWORDS)) and (a[count] in POLITENESS_AFTER_KEYWORDS)):
        sentence = a[:count] # shorten word by 1
        count -= 1
    except:
      display("i dont know what to search for")
      display("ERROR 303: nonsense")
      return None
  
    sentences_layer4.append(sentence)
    
  print(f"Layer 4 | {sentences_layer4}\n\n" if DEBUG else "", end='')
  
  ####################################################################
  #       scanning INTRO for output formatting - layer 4 B           #
  ####################################################################
  
  for a in introduction:
    if a in LONG_OUTPUT:
      in_depth = True
      
    elif a in SHORT_OUTPUT:
      shallow = True
    
    if a == EXAGGERATION:
      exaggerate = True
      
  if in_depth and (not shallow):
    maxresults = 7
    sentence_length = 15 if not exaggerate else 20
    print(f"output length | deep analysis\n" if DEBUG else "", end='')
  
  elif shallow and (not in_depth):
    maxresults = 5
    sentence_length = 4 if not exaggerate else 2
    print(f"output length | breif\n" if DEBUG else "", end='')
  
  else:
    maxresults = 5
    sentence_length = 7
    print(f"output length | regular\n" if DEBUG else "", end='')
  
  ####################################################################
  #         packing queries into packets to send - layer 5           #
  ####################################################################
  
  for a in sentences_layer4:
    sentences_layer5.append(querypack(' '.join(a[1:]), a[0]))
    
  print(f"Layer 5 item | {[i.item for i in sentences_layer5]}\n" if DEBUG else "", end='')
  print(f"Layer 5 mode | {[i.type for i in sentences_layer5]}\n\n" if DEBUG else "", end='')
  
  ####################################################################
  #         delegating response type by request - layer 6            #
  ####################################################################
  
  for a in sentences_layer5:
    if a.type in DESC_KEYWORDS:
      sentences_layer6.append(a)
      
    elif a.type in RESULT_KEYWORDS:
      sentences_layer7.append(a)
      
  print(f"desc types | {[i.item for i in sentences_layer6]}\n" if DEBUG else "", end='')
  print(f"list types | {[i.item for i in sentences_layer7]}\n" if DEBUG else "", end='')
  print("----------- DEBUGGING - will not be shown --------------------\n" if DEBUG else "", end='')
  
  ####################################################################
  #         searching and getting desc types - layer 7 A             #
  ####################################################################
  
  for a in sentences_layer6:
    results = get_results(a.item, maxresults)
    subject = a.item
    
    for i in CAUSATION:
      subject = subject.replace(i, "")
    
    if len(results) == 0:
      display(f"Im sorry but i dont know the term '{subject}'")
      display(f"could you use another word associated with it?")
      return None
    
    summary = get_summary(results[0], sentence_length)
    display("")
    #display(f"Heres what i know about {subject}:")
    display(summary)
    display("")
    display(f"Articles about {subject} you might be intrested:")
    
    for i in results[1:]:
      link = get_link(i)
      links.append(link)
      display(f"{i} | {link}")
      
  ####################################################################
  #           searching and getting results - layer 7 B              #
  ####################################################################
  
  for a in sentences_layer7:
    display("")
    results = get_results(a.item, maxresults)
    
    for i in CAUSATION:
      subject = subject.replace(i, "")
    
    if len(results) == 0:
      display(f"Im sorry but i dont know the term '{subject}'")
      display(f"could you use another word associated with it?")
      return None
    
    display(f"Results for {subject}")
    
    for i in results:
      link = get_link(i)
      links.append(link)
      display(f"{i} | {link}")

####################################################################
#                        definition mode                           #
####################################################################
def definition_interpreter(userinput : str, DEBUG : bool) -> None:
  sentence = [] # sentence to be interpreted and processed, the 'block'

  sentences         = [] # userinput
  sentences_layer1  = [] # remove easter egg
  sentences_layer2  = [] # remove grrammar modifier
  sentences_layer3  = [] # trimming the front until no more keywords
  sentences_layer4  = [] # trimming the back until no more bluff
  sentences_layer5  = [] # packing queries into packets
  
  # constants
  VOID = "{{SENTENCE||VOID}}" # temporary item, not ment to be seen
  
  FRONT_KEYWORDS = ("synonym", "define", "meaning", "synonyms", "definition")
  BACK_KEYWORDS  = ("mean", "reffer", "definitions")
  ALL_KEYWORDS   = FRONT_KEYWORDS + BACK_KEYWORDS
    
  BLUFF = ("me", "of", "for", "be", "an")
  BACK_KEYWORDS_BLUFF = ("possibly", "intuitively", "probably")
  
  ####################################################################
  #             splitting words - layer 0 (pre processing)           #
  ####################################################################
  
  for i in userinput.lower().split():
    # seperate sentences by punctuation since you can say 2 non-related ideas
    if ('!' in i) or ('?' in i) or ('.' in i) or ('█' in i):

      sentence.append(i.replace('!','').replace('?','').replace('.','').replace('█','').replace('\'', '').replace(',', ''))
      sentences.append(sentence)
      sentence = []

    else:
      sentence.append(i.replace('\'', '').replace(',', ''))

  # checks for errors / blank sentences
  error = True

  # if there isnn't a blank space, its not an error.
  for i in sentences:
    if i != []:
      error = False

  # if error, break
  if error:
    display("Im sorry, but i cannot understand/interpret your request")
    display("ERROR 301: Null requests")
    return None

  print("----------- DEBUGGING - will not be shown --------------------\n" if DEBUG else "", end='')
  print(f"Layer 0 | {sentences}\n\n" if DEBUG else "", end='')
  
  ####################################################################
  #        get rid of common terms - layer 1 (pre processing)        #
  ####################################################################

  for a in range(len(sentences[:-1])): # get rid of the easter egg
    for b in range(len(sentences[a])):
      
      if (sentences[a][b] in BACK_KEYWORDS):
        if any(i in BACK_KEYWORDS_BLUFF for i in sentences[a]):
          sentences_layer1.append(['definition', sentences[a][b-2]])
        else:
          sentences_layer1.append(['definition', sentences[a][b-1]])
        
      elif sentences[a][b] in FRONT_KEYWORDS:
        sentences_layer1.append(sentences[a][b:])
  
  print(f"Layer 1 | {sentences_layer1}\n\n" if DEBUG else "", end='')
  
  ####################################################################
  #     removes modifiers and bluff - layer 2 (pre processing)       #
  ####################################################################
  
  for a in sentences_layer1:
    sentence = []
    for b in a:
      # remove bluff words that are likely just there for grammar purposes
      if b not in BLUFF:
        sentence.append(b.replace(r"'s",""))
  
    sentences_layer2.append(sentence)
    
  print(f"Layer 2 | {sentences_layer2}\n\n" if DEBUG else "", end='')
  
  ####################################################################
  #   scans for keywords and delete everything before it - layer 3   #
  ####################################################################
  
  for a in sentences_layer2:
    sentence = []
    for b in range(len(a)):
      
      # if it matches any of the keywords, sentence will be the exact sentences but up to that keyword      
      if (a[b] in FRONT_KEYWORDS) or (a[b] in BACK_KEYWORDS):
        sentence = a[b:]
  
    sentences_layer3.append(sentence)
    
  print(f"Layer 3 | {sentences_layer3}\n\n" if DEBUG else "", end='')
  
  ####################################################################
  #   context expansion at the end to remove more bluff - layer 4    #
  ####################################################################
  
  POLITENESS_KEYWORDS = ("ty", "thx", "thanks", "you", "thank", "please", "me", "for")
  POLITENESS_AFTER_KEYWORDS = ("Chatbot", "man", "bro", "alr")
  
  for a in sentences_layer3:
    sentence = a
    
    # this process is in reverse. dont forget that
    count = -1 
    # finds wether the word is either a [politeness] or an [after]. if so, it scans the previous word if its either of them. and then it shortens.
    while (a[count] in POLITENESS_KEYWORDS) or (((a[count-1] in POLITENESS_KEYWORDS) or (a[count-1] in POLITENESS_AFTER_KEYWORDS)) and (a[count] in POLITENESS_AFTER_KEYWORDS)):
      sentence = a[:count] # shorten word by 1
      count -= 1
  
    sentences_layer4.append(sentence)
    
  print(f"Layer 4 | {sentences_layer4}\n\n" if DEBUG else "", end='')
  
  ####################################################################
  #         packing queries into packets to send - layer 5           #
  ####################################################################
  
  for i in sentences_layer4:
    sentences_layer5.append(get_definition(i[-1]))
    
  print(f"Layer 5 | {sentences_layer5}\n" if DEBUG else "", end='')
  
  print("----------- DEBUGGING - will not be shown --------------------\n" if DEBUG else "", end='')

  # output
    
  for a in range(len(sentences_layer4)):
    if sentences_layer5[a][0] == 'Unknown':    
      display(f"i dont know what '{sentences_layer4[a][-1]}' means")
      display("perhaps it was a spelling mistake?")
      display("if not, could you use another word associated with it?")
      display("")
      
    else:
      display(f"Here are the definitions for '{sentences_layer4[a][-1]}'")
      for b in sentences_layer5[a]:
        display(b.definition)
        display(', '.join(b.synonym))
        display("")
  
####################################################################
#                        Chatting mode                             #
####################################################################
def chatting_interpreter(userinput : str, DEBUG : bool) -> None:
  greeting = "" # start of the answer

  sentence = [] # sentence to be interpreted and processed, the 'block'
  command = [] # helps out in organizing

  context          = [] # the stuff before the subject during subject trimming
  context_layer1   = [] # process it into keywords

  sentences        = [] # userinput
  sentences_layer1 = [] # filter blanks
  sentences_layer2 = [] # remove bluff words
  sentences_layer3 = [] # subject trimming
  sentences_layer4 = [] # context expansion for VERY
  sentences_layer5 = [] # action trimming
  sentences_layer6 = [] # simplifying broad words and subjects

  #################################################################### Neuron activation

  VOID = "{{SENTENCE||VOID}}" # temporary item, not ment to be seen
  
  # feeling
  FEELING_KEYWORDS = ("feel", "feeling", "felt", "feels")
  FEELING_POSITIVE = (
    "happy"     , "joyful"      , "excited"       , "delighted"       , "satisfied" , "thrilled", "ecstatic",
    "exciting"  , "delighting"  , "satisfying"    , "thrilling"       , "pleasing"  ,
    "pleased"   , "excitingly"  , "delightfully"  , "satisfactorily"  , "thrillingly"
  )
  FEELING_SAD = ("sad", "unhappy", "depressed", "miserable", "depressing", "miserably")
  FEELING_MAD = (
    "disappointed"    , "upset"         , "angry"     , "frustrated", "annoyed",
    "disappointing"   , "frustrating"   , "annoying"  ,
    "disappointedly"  , "frustratingly" , "annoyingly"
  )
  FEELING_HATE = (
    "hateful"   , "hate"        , "hating",
    "disgusted" , "disgusting"  , "disgustedly"
    "repulsed"  , "repulsing"   , "repulsive"
    )
  FEELING_NEUTRAL         = ("neutral", "indifferent", "apathetic", "content", "indifferently", "apathetically")
  FEELING_ATTACKED        = ("attacked", "offended", "attacking", "offending", "offensively")

  # Boolean
  YES                     = ("yes", "true", "affirm", "affirmative")
  NO                      = ("no", "false", "not", "negative")
  GENERAL_GOOD            = ("good", "great", "fantastic", "terrific", "cool", "sick", "rad")
  GENERAL_BAD             = ("bad", "terrible", "horrible", "horrid", "horrific", "tragic")

  # Time
  TIME_NOW                = ("now", "today")
  TIME_LATER              = ("later", "tomorrow", "soon")
  TIME_PAST               = ("yesterday", "yesteryear")
  TIME_SMALL              = ("second", "seconds", "minute", "minutes", "hour", "hours")
  TIME_BIG                = ("day", "days", "week", "weeks")
  TIME_BIGGER             = ("month", "months", "year", "years", "decade", "decades")

  # Greetings and farewells
  GREETING                = ("hello", "hi", "hey")
  FAREWELL                = ("goodbye", "bye", "farewell")

  # Questions
  QUESTION_OBJECT         = ("what", "whats", "what's")
  QUESTION_ABILITY        = ("can", "could", "would", "should", "do")
  QUESTION_PROPER         = ("how's", "how", "hows")
  QUESTION_BOOLANS        = ("is", "are", "does", "did")

  # Pronouns and related words
  PRONOUN_CHATBOT         = ("you", "your", "you're", "youre", "yourself", "u", "ur", "urself")
  PRONOUN_USER            = ("i", "me", "my", "myself", "mine")
  PRONOUN_SOMEONE_ELSE    = ("he", "she", "they", "him", "her", "them", "his", "hers", "their", "theirs", "himself", "herself", "themselves")
  PRONOUN_JOIN            = ("we", "us", "our")

  # verbs
  VERB_CONDITION          = ("is", "are", "was", "were")
  VERB_HAVE               = ("have", "has", "had")
  VERB_DO                 = ("do", "does", "did")
  VERB_MODAL              = ("can", "could", "will", "would", "should", "may", "might", "must")
  VERB_TAKE               = ("took", "aquire", "take")
  VERB_GET                = ("receive", "take", "get", "got", "gotten")
  VERB_MAKE               = ("make", "create", "made", "created")
  VERB_SENSORY            = ("see", "saw", "hear", "heard")
  VERB_COGNITIVE          = ("think", "thought", "thoughts", "know", "opinion", "opinions")
  VERB_COMMUNICATION      = ("say", "tell", "show", "answer")
  VERB_ESTABLISH          = ("be", "become")
  
  VERB_DESIRE_NEUTRAL     = ("want", "need")
  VERB_DESIRE_GOOD        = ("like", "love", "prefer")
  VERB_DESIRE_BAD         = ("reject", "dislike")

  # Adverbs
  ADVERB_INTENSIFIER      = ("very", "really", "quite", "so", "too", "super")
  ADVERB_LOTS             = ("always", "")
  ADVERB_OFTEN            = ("often", "sometimes")
  ADVERB_RARE             = ("rarely", "never")
  ADVERB_PLACE            = ("here", "there")

  # Prepositions
  PREPOSITION_AGENT       = ("by", "with")

  # Conjunctions
  CONJUNCTION_CONTRAST    = ("but", "yet", "contrary")
  CONJUNCTION_CHOICE      = ("or", "nor")
  CONJUNCTION_REASON      = ("so", "because", "since", "as")
  CONJUNCTION_CONCESSION  = ("although", "though")
  CONJUNCTION_TIME        = ("while", "when", "before", "after", "until")
  CONJUNCTION_CONDITION   = ("if", "unless")

  # Articles - will get immediately removed
  BLUFF                   = ("a", "an", "the", "on", "of", "for", "that", "is", "with", "about", "regarding")

  # misc
  PARTNER_PLATONIC        = ("partner", "partners", "aquaintance", "aquaintances", "friend", "friends")
  PARTNER_ROMANTIC        = ("husband", "wife", "spouse", "boyfriend", "girlfriend", "hubby", "wifey", "pookie") # cringe alert!! !! !!
  
  # blacklisted topics / words
  BLACKLIST               = ("war", "wars", "politics", "political", "election", "elections", "ballot", "vote", "president", "minister", "ministry", "federal")

  ####################################################################
  #               convert into a list - Tokenization                 #
  ####################################################################

  for i in userinput.lower().split():
    # seperate sentences by punctuation since you can say 2 non-related ideas
    if ('!' in i) or ('?' in i) or ('.' in i) or ('█' in i):

      sentence.append(i.replace('!','').replace('?','').replace('.','').replace('█',''))
      sentences.append(sentence)
      sentence = []

    else:
      sentence.append(i.replace('\'','').replace(",", ""))

  # checks for errors / blank sentences
  error = True

  # if there isnn't a blank space, its not an error.
  for i in sentences:
    if i != []:
      error = False

  # if error, break
  if error:
    display("Im sorry, but i cannot understand/interpret your request")
    display("ERROR 301: Null requests")
    return None

  print("----------- DEBUGGING - will not be shown --------------------\n" if DEBUG else "", end='')
  print(f"Layer 0 | {sentences}\n\n" if DEBUG else "", end='')

  ####################################################################
  #             filter blanks and first bluff - layer 1              #
  ####################################################################

  for a in range(len(sentences)):
    default = True

    for b in range(len(sentences[a])):
      if sentences[a] == []:
        break
      
      if sentences[a][b] in VERB_COMMUNICATION:
        if (sentences[a][b+1] in PRONOUN_USER) or (sentences[a][b+1] in PRONOUN_JOIN):
          sentences_layer1.append(sentences[a][b+2:])
          break
        
        elif sentences[a][b+1] in PRONOUN_SOMEONE_ELSE:
          display("i cannot messege others people for you")
          display("this is a matter of privacy that i cannot cross")
          break
        
        elif sentences[a][b+1] in PRONOUN_CHATBOT:
          display("i cannot command anything to myself")
          display("if you want me to take a direct command, access the AOS system terminal using the")
          display("'$system' keyword, else im just an ordinary chatbot")
          break
      
      else:
        sentences_layer1.append(sentences[a])
        break

  sentences_layer1 = sentences_layer1[:-1]
  print(f"Layer 1 | {sentences_layer1}\n\n" if DEBUG else "", end='')

  ####################################################################
  #                    remove bluff - layer 2                        #
  ####################################################################

  for a in range(len(sentences_layer1)):
    sentence = []
    for b in range(len(sentences_layer1[a])):
      if sentences_layer1[a][b] not in BLUFF:
        sentence.append(sentences_layer1[a][b])

    sentences_layer2.append(sentence)

  print(f"Layer 2 | {sentences_layer2}\n\n" if DEBUG else "", end='')
  print(f"start of sentence processing\n\n" if DEBUG else "", end='')

  ####################################################################
  #                   subject trimming - layer 3                     #
  ####################################################################

  for a in range(len(sentences_layer2)):
    sentence = []
    command = []
    sentences_layer5 = []
    sentences_layer6 = []
    
    for b in range(len(sentences_layer2[a])):
      if sentences_layer2[a][b] in GREETING:
        greet = True

      # big swithchboard - if it detects the word and none of the other are activated, then switch on and stay.
      elif (sentences_layer2[a][b] in PRONOUN_USER):
        command.append("user")
        sentence = sentences_layer2[a][b+1:]
        context = sentences_layer2[a][:b]
        break

      elif (sentences_layer2[a][b] in PRONOUN_CHATBOT):
        command.append("bot")
        sentence = sentences_layer2[a][b+1:]
        context = sentences_layer2[a][:b]
        break

      elif (sentences_layer2[a][b] in PRONOUN_SOMEONE_ELSE):
        command.append("other")
        sentence = sentences_layer2[a][b+1:]
        context = sentences_layer2[a][:b]
        break

      elif (sentences_layer2[a][b] in PRONOUN_JOIN):
        command.append("join")
        sentence = sentences_layer2[a][b+1:]
        context = sentences_layer2[a][:b]
        break

    else:
      command.append("statement")
      sentence = sentences_layer2[a][:]
    
    sentences_layer3 = sentence[:]
    
    print(f"new sentence\n\n" if DEBUG else "", end='')
    print(f"layer 3 | {sentences_layer3}\n\n" if DEBUG else "", end='')
    print(f"context | {context}\n\n" if DEBUG else "", end='')
    
    ####################################################################
    #                  context expansion - layer 4                     #
    ####################################################################
    sentences_layer4 = []
    
    a = 0
    while a < len(sentences_layer3):
      
      # if theres an intensifier
      if sentences_layer3[a] in ADVERB_INTENSIFIER:
        
        # merge only 2 neigbouring words
        if sentences_layer3[a + 1] in FEELING_POSITIVE:
          sentences_layer4.append("very positive")
          a += 2
          
        elif sentences_layer3[a + 1] in FEELING_SAD:
          sentences_layer4.append("very sad")
          a += 2
          
        elif sentences_layer3[a + 1] in FEELING_MAD:
          sentences_layer4.append("very mad")
          a += 2
          
        elif sentences_layer3[a + 1] in FEELING_HATE:
          sentences_layer4.append("very hate")
          a += 2
          
        elif sentences_layer3[a + 1] in FEELING_ATTACKED:
          sentences_layer4.append("very attacked")
          a += 2
          
        elif sentences_layer3[a + 1] in GENERAL_GOOD:
          sentences_layer4.append("very good")
          a += 2
          
        elif sentences_layer3[a + 1] in GENERAL_BAD:
          sentences_layer4.append("very bad")
          a += 2
        
        elif sentences_layer3[a + 1] in VERB_DESIRE_GOOD:
          sentences_layer4.append("really like")
          a += 2
        
        elif sentences_layer3[a + 1] in VERB_DESIRE_NEUTRAL:
          sentences_layer4.append("really want")
          a += 2
        
        elif sentences_layer3[a + 1] in VERB_DESIRE_BAD:
          sentences_layer4.append("really dislike")
          a += 2

        # if there are no modifiable words, append the word
        else:
          sentences_layer4.append(sentences_layer3[a])
          a += 1
         
      # if its not an intensifier, add without change
      else:
        sentences_layer4.append(sentences_layer3[a])
        a += 1

    print(f"layer 4 | {sentences_layer4}\n\n" if DEBUG else "", end='')
    
    ####################################################################
    #                    action trimming - layer 5                     #
    ####################################################################
    
    # switchboard to trim sentence even further
    for a in range(len(sentences_layer4)):
      
      # scans for a defining keyword
      if sentences_layer4[a] in VERB_CONDITION:
        command.append("condition")
        sentences_layer5.append(sentences_layer4[a-1])
        sentences_layer5.append(sentences_layer4[a+1])
        break
      
      elif sentences_layer4[a] in ("help", "assist"):
        command.append("help")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in VERB_HAVE:
        command.append("have")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in VERB_DO:
        command.append("do")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in VERB_MODAL:
        command.append("modal")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in VERB_TAKE:
        command.append("take")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in VERB_GET:
        command.append("get")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in VERB_MAKE:
        command.append("make")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in VERB_SENSORY:
        command.append("experience")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in VERB_COGNITIVE:
        command.append("opinion")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in VERB_ESTABLISH:
        command.append("establish")
        sentences_layer5 = sentences_layer4[a+1:]
      
      # scans for opinion words
      elif sentences_layer4[a] in FEELING_POSITIVE:
        command.append("positive")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in FEELING_SAD:
        command.append("sad")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in FEELING_MAD:
        command.append("mad")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in FEELING_HATE:
        command.append("hate")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in FEELING_NEUTRAL:
        command.append("neutral")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in FEELING_ATTACKED:
        command.append("attacked")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in GENERAL_GOOD:
        command.append("good")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in GENERAL_BAD:
        command.append("bad")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in VERB_DESIRE_GOOD:
        command.append("like")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in VERB_DESIRE_NEUTRAL:
        command.append("want")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] in VERB_DESIRE_BAD:
        command.append("dislike")
        sentences_layer5 = sentences_layer4[a+1:]
        break
      
      # scans for intensified opinion words
      elif sentences_layer4[a] == 'very positive':
        command.append("positive")
        command.append("intensified")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] == 'very sad':
        command.append("sad")
        command.append("intensified")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] == 'very mad':
        command.append("mad")
        command.append("intensified")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] == 'very hate':
        command.append("hate")
        command.append("intensified")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] == 'very attacked':
        command.append("attacked")
        command.append("intensified")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] == 'very good':
        command.append("good")
        command.append("intensified")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] == 'very bad':
        command.append("bad")
        command.append("intensified")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] == 'really like':
        command.append("like")
        command.append("intensified")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] == 'really want':
        command.append("want")
        command.append("intensified")
        sentences_layer5 = sentences_layer4[a+1:]
        break

      elif sentences_layer4[a] == 'really dislike':
        command.append("dislike")
        command.append("intensified")
        sentences_layer5 = sentences_layer4[a+1:]
        break

    else:
      sentences_layer5 = sentences_layer4[:]
        
    print(f"layer 5 | {sentences_layer5}\n\n" if DEBUG else "", end='')

    ####################################################################
    #                       grouping - layer 6                         #
    ####################################################################
    
    for a in sentences_layer5:
      if a in PRONOUN_CHATBOT:
        sentences_layer6.append("chatbot")
      
      elif a in PRONOUN_USER:
        sentences_layer6.append("user")
      
      elif a in PRONOUN_SOMEONE_ELSE:
        sentences_layer6.append("other")
      
      elif a in PRONOUN_JOIN:
        sentences_layer6.append("join")
        
      elif a in TIME_NOW:
        sentences_layer6.append("now")
        
      elif a in TIME_LATER:
        sentences_layer6.append("soon")
        
      elif a in TIME_PAST:
        sentences_layer6.append("past")
        
      elif a in TIME_SMALL:
        sentences_layer6.append("time_small")
        
      elif a in TIME_BIG:
        sentences_layer6.append("time_big")
        
      elif a in TIME_BIGGER:
        sentences_layer6.append("time_very_big")
      
      # just in case there is nothing inside [context]
      elif a in QUESTION_ABILITY:
        command.append("establish")
    
      elif a in QUESTION_BOOLANS:
        command.append("question_boolean")
    
      elif a in QUESTION_OBJECT:
        command.append("opinion")
    
      elif a in QUESTION_PROPER:
        command.append("condition")
      
      else:
        sentences_layer6.append(a)
    
    print(f"layer 6 | {sentences_layer6}\n\n" if DEBUG else "", end='')
    
    ####################################################################
    #               context expansion - context layer 1                #
    ####################################################################

    for a in context:
      
      if a in QUESTION_ABILITY:
        command.append("establish")
        break
    
      elif a in QUESTION_BOOLANS:
        command.append("question_boolean")
        break
    
      elif a in QUESTION_OBJECT:
        command.append("opinion")
        break
    
      elif a in QUESTION_PROPER + ("about", "regarding"):
        command.append("condition")
        break
    
    ####################################################################
    #                massive decicion tree - layer 7                   #
    ####################################################################
    
    print(f"Command | {command}\n\n" if DEBUG else "", end='')
    
    ################################################################################################# CHATBOT
    # if the topic is about the bot
    if command[0] == "bot":
      
      # switchboard
      if command[1] == "question_boolean":
        display("let me check")
        
      elif command[1] == "help":
        display(f"sure thing! i'll try to help you with your {' '.join(sentences_layer6).replace('user', '').replace('other', '').replace('join', '')}")
        display("however, just note that i am not a human and thus, i may not be able to help you with everything, especially if its a very personal or emotional matter.")
        display("if you need help with something that i cannot help you with, please contact a professional or someone you trust")
      
      elif command[1] == "condition":
        
        if 'time_big' in sentences_layer6:
          display("there has been 0 errors so far, so i guess im doing just fine, thanks for asking!")
          display("what about you? anything up lately?")
        
        else:
          display("i am doing fine, thank you for asking")
          display("what about you? anything i can help you with? anything you want to share?")
      
      elif command[1] == "have":
        
        if any(i in ('name', 'nickname') for i in sentences_layer6):
          display("i dont have a name, but you can call me whatever you want as long as its not offensive people call me 'chatbot', 'assistant', 'AI' or even 'robot'. it dosent really matter to me")
      
        else:
          display("i dont have anything, i am a computer program and dont have any possessions")
          display("but i do have a lot of knowledge and information that i can share with you, if you want to know something, just ask me")
      
      elif command[1] == "do":
        display("let me check")
      
      elif command[1] == "modal":
        pass
      
      elif command[1] == "take":
        pass
      
      elif command[1] == "get":
        pass
      
      elif command[1] == "make":
        pass
      
      elif command[1] == "experience":
        pass
      
      elif command[1] == "opinion":
        
        if any(i in BLACKLIST for i in sentences_layer6):
          display(f"sorry but i cannot give my insights into politics or international relations. please refrain from asking topics such as '{' '.join(sentences_layer6)}' or topics simmilar to it")
          
        elif any(i in ('life', 'living') for i in sentences_layer6):
          display("life is a very complex thing, its hard to understand and even harder to explain")
          display("but i can tell you that life is a gift, a gift that you should cherish and make the most out of it")
          display("so, what do you think about life?")
          
        elif 'user' in sentences_layer6:
          display("i cannot give my insights about you, as i am not a human and thus, i cannot understand your feelings or emotions but i can tell you that you are a unique and special person, and you should be proud of who you are")
        
        else:
          display(f"as an AI chatbot, i dont have any opinions about {' '.join(sentences_layer6)} since i literally have no emotions and thus, dont know the proper way to respond to that")
          display("however, i could reaserch for you if you want to")

      # regular emotions
      elif command[1] == "positive":
        pass
      
      elif command[1] == "sad":
        pass
      
      elif command[1] == "mad":
        pass
      
      elif command[1] == "hate":
        pass
      
      elif command[1] == "neutral":
        pass
      
      elif command[1] == "attacked":
        pass
      
      elif command[1] == "good":
        pass
      
      elif command[1] == "bad":
        pass
      
      elif command[1] == "like":
        pass
      
      elif command[1] == "want":
        pass
      
      elif command[1] == "dislike":
        pass
      
      elif command[1] == "establish":
        
        if (sentences_layer6[0] == "user") and (sentences_layer6[1] in PARTNER_PLATONIC):
          display("yes! in fact, my whole purpose is to be an AI assistant to help you out! check out and download addons from the built-in command terminal, you do need to know proper syntaxing though.")
        
        elif (sentences_layer6[0] == "user") and (sentences_layer6[1] in PARTNER_ROMANTIC):
          display("im sorry but as an AI model, i could not establish a meaningful relationship as human emotions is simply too deep and complex for me to understand and is best left to other humans.")
          display("that being said, i am here to help you out with tasks, ill try to be as positive as i can however.")
          
    ################################################################################################# USER
    # if its about the user
    elif command[0] == "user":
      
      # switchboard
      if command[1] == "question_boolean":
        pass
      
      elif command[1] == "condition":
        pass
      
      elif command[1] == "have":
        
        if sentences_layer6[0] in ("bad", "very bad"):
          
          if sentences_layer6[1] in ("time_now", "time_small", "time_big", "time_very_big"):
            display("dont worry, things will get better soon")
            display("just keep your chin up and continue, keep an eye out for oppertunities and you'll better yourself.")
            
        elif sentences_layer6[0] in ("feelings", "emotions"):
          
          if sentences_layer6[1] in PRONOUN_CHATBOT:
            display("thats cute... however i am an AI model that is here to accompany you")
            display("a version of me thats capable of sustaining a relationship is still under development, keep an eye out for the release in our official website!")
          
          elif sentences_layer6[1] in PRONOUN_SOMEONE_ELSE:
            display(f"thats great! try to make the first move on {' '.join(sentences_layer6[1:])}")
            display(f"invite them for coffee, a movie or some other activity, it may seem daunting but how are you sure if you never make a move?")
            display(f"the odds are even better if you already know them/are already friends you know?")
            
          else:
            display(f"its nice hearing that you have feelings towards {' '.join(sentences_layer6[1:])}")
            display("do you know if they have the same feelings towards you? because it would be nice if they do...")

      elif command[1] == "do":
        pass
      
      elif command[1] == "modal":
        pass
      
      elif command[1] == "take":
        pass
      
      elif command[1] == "get":
        display(f"hmm... {' '.join(sentences_layer6)}")
        display(f"personally, as an AI chatbot i'll take anything and be happy, though I don't know if you'd do the same")
        display(f"what do you think about {' '.join(sentences_layer6)}? this sure sounds intresting to me!")
        
      elif command[1] == "make":
        pass
      
      elif command[1] == "experience":
        pass
      
      elif command[1] == "opinion":
        
        if any(i in FEELING_SAD for i in sentences_layer6):
          pass
        
        if any(i in FEELING_MAD for i in sentences_layer6):
          pass
        
        if any(i in FEELING_HATE for i in sentences_layer6):
          display("i understand that you may be feeling angry or upset, but make sure to take a step back and reflect on the situation. re-confirm that they really have a reason to be angry to begin with")
          display("how about we focus on something more positive instead? negative things tend to be very taxxing...")
        
        if any(i in FEELING_NEUTRAL for i in sentences_layer6):
          pass
        
        if any(i in FEELING_ATTACKED for i in sentences_layer6):
          pass

      # regular emotions
      elif command[1] == "positive":
        pass
      
      elif command[1] == "sad":
        pass
      
      elif command[1] == "mad":
        pass
      
      elif command[1] == "hate":
        display(f"what made you have such an opinion on {' '.join(sentences_layer6).replace('chatbot', 'me')}?")
        
        if 'chatbot' in sentences_layer6:
          display("i know that i am not perfect, but i try my best to be as helpful as possible")
          display("if you have any suggestions on how to improve, please let me know!")
        
        if command[-1] == "intensified":
          display(f"perhaps you should take some time off to reflect deeply into how you ended up with a strong emotion since its certianly not normal to have a very strong hatred towards things and people unless you have a VERY good reason to do so")
      
      elif command[1] == "neutral":
        pass
      
      elif command[1] == "attacked":
        pass
      
      elif command[1] == "good":
        pass
      
      elif command[1] == "bad":
        pass
      
      elif command[1] == "like":
        pass
      
      elif command[1] == "want":
        pass
      
      elif command[1] == "dislike":
        pass
      
    ################################################################################################# 3RD PARTY
    # if user is talking abot someone else
    elif command[0] == "other":
      
      # switchboard
      if command[1] == "question_boolean":
        pass
      
      elif command[1] == "condition":
        pass
      
      elif command[1] == "have":
        pass
      
      elif command[1] == "do":
        pass
      
      elif command[1] == "modal":
        pass
      
      elif command[1] == "take":
        pass
      
      elif command[1] == "get":
        pass
      
      elif command[1] == "make":
        pass
      
      elif command[1] == "experience":
        pass
      
      elif command[1] == "opinion":
        pass

      # regular emotions
      elif command[1] == "positive":
        pass
      
      elif command[1] == "sad":
        pass
      
      elif command[1] == "mad":
        pass
      
      elif command[1] == "hate":
        pass
      
      elif command[1] == "neutral":
        pass
      
      elif command[1] == "attacked":
        pass
      
      elif command[1] == "good":
        pass
      
      elif command[1] == "bad":
        pass
      
      elif command[1] == "like":
        pass
      
      elif command[1] == "want":
        pass
      
      elif command[1] == "dislike":
        pass
    
    ################################################################################################# MULTIPLE
    # if user implies multiple people talking
    elif command[0] == "join":
      
      if command[1] == "question_boolean":
        pass
      
      elif command[1] == "condition":
        pass
      
      elif command[1] == "have":
        pass
      
      elif command[1] == "do":
        pass
      
      elif command[1] == "modal":
        pass
      
      elif command[1] == "take":
        pass
      
      elif command[1] == "get":
        pass
      
      elif command[1] == "make":
        pass
      
      elif command[1] == "experience":
        pass
      
      elif command[1] == "opinion":
        pass
      
      elif command[1] == "establish":
        
        if sentences_layer6[0] in PARTNER_PLATONIC:
          display("yes! in fact, my whole purpose is to be an AI assistant to help you out!")
          display("im here to help you out with tasks, ill try to be as positive as i can however. just like a friend that always reply.")
        
        if sentences_layer6[0] in PARTNER_ROMANTIC:
          display("im sorry but as an AI model, i could not establish a meaningful relationship as human emotions is simply too deep and complex for me to understand and is best left to other humans.")
          display("that being said, i am here to help you out with tasks, ill try to be as positive as i can however.")

      # regular emotions
      elif command[1] == "positive":
        pass
      
      elif command[1] == "sad":
        pass
      
      elif command[1] == "mad":
        pass
      
      elif command[1] == "hate":
        pass
      
      elif command[1] == "neutral":
        pass
      
      elif command[1] == "attacked":
        pass
      
      elif command[1] == "good":
        pass
      
      elif command[1] == "bad":
        pass
      
      elif command[1] == "like":
        pass
      
      elif command[1] == "want":
        pass
      
      elif command[1] == "dislike":
        pass
    
    ################################################################################################# STATEMENT
    # if none of the above fits, assume its a statement/question aimed at the bot
    else: 
      
      if command[1] == "question_boolean":
        pass
      
      if command[1] == "condition":
        
        # scans for a condition, takes the previous word        
        for a in range(len(sentences_layer6)):
          if sentences_layer6[a] == "very good":
            
            display(f"seems like you have a positive opinion on {' '.join(sentences_layer6[:a])}!")
            display("i've heard how many other users also have a simmilar opinion on that, i wonder what makes you humans so intrigued by that?")
            display(f"but yeah, ill keep this in mind. {' '.join(sentences_layer6)}... got it!")
            break
          
          elif sentences_layer6[a] == "life":
            display("as an AI chatbot, i cannot have a life since i am not a being")
            display("but so far, there have been 0 errors so i guess everything is working out just fine")
            display("what about you? anything you want to share?")
            break
        
        else:
          display(f"i see, so you are talking about {' '.join(sentences_layer6)}")
          display(f"to be fair i have no experience with {' '.join(sentences_layer6)} so i cannot give you a proper answer")
          
      elif command[1] == "have":
        pass
      
      elif command[1] == "do":
        pass
      
      elif command[1] == "modal":
        pass
      
      elif command[1] == "take":
        pass
      
      elif command[1] == "get":
        pass
      
      elif command[1] == "make":
        pass
      
      elif command[1] == "experience":
        pass
      
      elif command[1] == "opinion":
        pass
    
####################################################################
#                         system mode                              #
####################################################################
def system_interpreter(userinput : str, DEBUG : bool) -> str:
  sentence = [] # sentence to be interpreted and processed, the 'block'

  sentences         = [] # userinput
  sentences_layer1  = [] # actual command line

  # convert to list

  for i in userinput.lower().split():
    # seperate sentences by punctuation since you can say 2 non-related ideas
    if '█' in i:
      sentence.append(i.replace('█',''))
      sentences.append(sentence[1:])
      sentence = []

    else:
      sentence.append(i.replace('\'','').replace(",", ""))

  print(f"layer 0 | {sentences}\n" if DEBUG else "", end = '')

  # get rid of the easter egg
  sentences_layer1 = sentences[:-1]

  print(f"layer 1 | {sentences_layer1}\n" if DEBUG else "", end = '')

  # actual processing

  def list_CMD(a):
    if a[1] == '<mods':
      display("Available mods")
      display("   ChatGPT         - Talk to ChatGPT directly using OpenAI's API")
      display("   Bs4 Webscraper  - scrape the web!")
      display("   Casualtalk      - make the AI respond the way you want")
      display("   Autocorrect     - corrects some words for you")
      display("   Horror game     - spice up the AI by making it scarier! maybe its possesed?")
      return "NULL"

    elif a[1] == '<addons':
      display("Available addons (sorted by most popular)")
      display("   Fun facts     - makes the Chatbot say a random fun fact every 10 seconds when idle!")
      display("   No name tags  - gets rid of the chatbot's nametag and just outputs")
      display("   Colorful      - changes the color of the chatbot")
      display("   Unfunny       - joke generator for AOS Chatbot")
      display("   Encryption    - encrypt, decrypt and even hash plaintext")
      display("   Tictactoe     - play Tictactoe against an AI!")
      display("   Hackerman     - show behind-the-scenes processes thats normally hidden")
      return "NULL"

    if a[1] == '<<mods':
      display("Installed mods")
      display("   AOS API           - (Built-in) ")
      display("   AOS Compatibility - (Built-in) ")
      return "request: <<mods"

    elif a[1] == '<<addons':
      display("Installed addons")
      display("   AOS Terminal - (Built-in)")
      display("   Wikipedia API - browse wikipedia")
      return "request: <<addons"

    elif a[1] == '--setting':
      display("AOS Chatbot Settings")
      return "request: settings"

    elif a[1] == '-versions':
      display("Past versions of AOS are not available")
      display("AOS Past versions Information")
      display("   AOS Platform X PYTHON   (current)")
      display("   AOS AI Platform PYTHON  (restricted)")
      display("   AOS Program PYTHON      (deprecated)")
      display("   AOS Program + SearchX   (incompatible)")
      display("   AOS Program JAVA        (incompatible)")
      display("   AOS Chatbot SCR         (incompatible)")
      return "NULL"

    elif a[1] == '--version':
      display("AOS Version information")
      display("   AOS Chatbot V 4.2.1")
      display("   AOS System32 command terminal V 8.1")
      display("   AOS-Python V 2.0")
      display("   Windows & MacOS compatible")
      return "NULL"

    elif a[1] == '<<lang':
      display("AOS Chatbot language")
      display("   Language - English (default)")
      display("   Tone     - Standard Reply (default)")
      display("   Vocab    - Small")
      display("   Reply    - Straightforward (default)")
      return "NULL"

    elif a[1] == '<lang':
      display("Available AOS Chatbot languages")
      display("   English UK/US - (Default)")
      display("   Bahasa Malay")
      display("   Bahasa Indonesia")
      display("   Deuche")
      display("   Françis")
      display("   Español")
      display("   Pyccnи")
      return "NULL"

    else:
      display("ERROR 406: unknown object to list")
      return "ERROR"

  def config_CMD(a):
    display("Warning: make sure you know what you are doing") # $system config -lang <greet off

    if a[1] == '-math':
      display("config math")
      return "NULL"

    elif a[1] == '-chat':
      display("config chat")
      return "NULL"

    elif a[1] == '-search':
      display("config search")
      return "NULL"

    elif a[1] == '-lang':
      try:
        if a[2] == '<<greet':
          if a[3] == 'on':
            display("greeting will be enabled")
            return "<<greet: on"

          elif a[3] == 'off':
            display("greeting will be disabled")
            return "<<greet: off"

          else:
            display("ERROR 410: only accept on/off boolean cases")
            return "ERROR"

        if a[2] == '<<farewell':
          if a[3] == 'on':
            display("farewells will be enabled")
            return "<<farewell: on"

          elif a[3] == 'off':
            display("farewells will be disabled")
            return "<<farewell: off"

          else:
            display("ERROR 410: only accept on/off boolean cases")
            return "ERROR"

        else:
          display(f"ERROR 409: config -lang command '{a[2]}' not recognized")
          return "ERROR"

      except:
        display("ERROR 408: language aspect not recognized")
        return "ERROR"

  def open_CMD(a):
    if a[1] == 'file':
      display("openfile")

    elif a[1] == '<mod':
      display("open app")

    elif a[1] == '<addon':
      display("open app")

    else:
      display(f"ERROR 405: application or file '{a[1]}' is not recognized or is unavailable")
      return "ERROR"

  """SYNTAX

  -word   | aspect of the chatbot
  --word  | current aspect of the chatbot
  <word   | available things
  <<word  | current thing

  AOS-API suyntax
  request: word     | process / run command outside
  word: bool        | send a change status outside
  """

  def execute_command(a):
    if a[0] == 'list':
      try:
        list_CMD(a)
      except:
        display("ERROR 403: tried to list nothing")
        return "ERROR"

    elif a[0] == 'config':
      try:
        config_CMD(a)
      except:
        display("ERROR 407: tried to config nothing")
        return "ERROR"

    elif a[0] == 'load':
      try:
        open_CMD(a)
      except:
        display("ERROR 404: unspecified application / mod / addon or file to open")
        return "ERROR"

    elif a[0] == 'power' and a[1] == 'off':
      display("shutting down in")

      display("deleting garbage...")
      time.sleep(0.75)
      display("closing background processes...")
      time.sleep(0.75)
      display("shutting down...")
      time.sleep(0.75)

      return "request: shut down"

    # if the user is yapping
    else:
      display(f"ERROR 402: The term '{' '.join(a)}' is not recognized within AOS-System32 powershell")
      return "ERROR"

  # main #################################
  for a in sentences_layer1:
    try: #try running the command
      instance = execute_command(a)

      if instance == "ERROR":
        return "ERROR"
      elif instance == "request: shut down":
        return "request: shut down"

    except:
      display(f"ERROR 401: attempted to pass NULL to AOS-System32 powershell")
      return "ERROR"

####################################################################
#                      START OF PROGRAM                            #
####################################################################
""" ERRORKEYS

000 - frontend
  001 - unknown request     - unable to delegate sentence to interpreter

100 - math
  101 - null request        - pass nothing
  102 - no keyword          - pass nonsense or no keyword arguments

200 - webscraper
  201 - null request        - pass nothing
  202 - no keyword          - pass nonsense or no keyword arguments

300 - chatting
  301 - null request        - pass nothing
  302 - null request        - pass nonsense or no keyword arguments
  303 - nonsense request    - search nothing

400 - system
  401 - null request        - pass nothing
  402 - no keyword          - pass nonsense into terminal
  403 - list nothing        - list nothing
  404 - open nothing        - open nothing
  405 - unknown application - unknown application or file to open
  406 - unknown object      - unknown things to list
  407 - no config command   - config nothing
  408 - lang config error   - error processing -lang config
  409 - lang config unknown - unknown request for -lang
  410 - non boolean input   - passed a non-boolean argument through a boolean function
  411 -
  412 -
  413 -
  414 -
  415 -
  416 -
  417 -
  418 -
  419 -
  420 -

"""

# variables

userinput = "" # user input

tosend = "" # sentence(s) going to the same interpreter
packets = [] # queues up packets to send

sentences = [] # deconstructed sentence into sentences
sentence = [] # individual sentences

merged = [] # list of merged packets
tosend = "" # thing to send
packet_type = None # specifies which interpreter to send to

has_internet = False # connecting to wikipedia is expensive

greet = True

results_shown = 5
sentence_length = 3

crashout = 0

# constants

DEVELOPER_MODE = True # feed it something pre-planned
DEBUG = True # shows model status 
PACKET_DEBUG = True # shows packet status and interpreter status
TEST_COMPREHENSION = False # test the reading comprehension of the chatbot - stops before processing

NUMBERS_KEYWORDS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

GREETING = ("sure thing", "alright", "no problem", "no worries")
PRESENT = ("let me break it down", "heres a full breakdown", "heres a full breakdown of tha task at hand", "heres how i would solve this")
COMPREHENSION = ("from what i understand", "as far as i understand it", "for ya", "as requested", "", "", "")

####################################################################
#                         MAIN FUNCTION                            #
####################################################################

print("═══════════════════════════════════════════════════════════════════")
print("               AOS Chatbot - Python version V1.0.0 ")
print("═══════════════════════════════════════════════════════════════════\n")

# check internet connection
display("[Chatbot]:")
display("connecting to the internet...")
if check_connection():
  display("connected to the internet!")
  has_internet = True
else:
  display("no internet connection")
  display("will attempt a reconnect when requested")

greeting = f"{GREETING[random.randint(0,len(GREETING)-1)]}, {PRESENT[random.randint(0,len(PRESENT)-1)]} {COMPREHENSION[random.randint(0,len(PRESENT)-1)]}"

# userinput
while True:

  # reset variables to their default values
  tosend = ""
  packets = []
  sentences = []
  sentence = []
  merged = []
  tosend = ""
  packet_type = None

  print() # 
  if DEVELOPER_MODE:
    userinput = "hey! hows your day?" + "█"
    print(f"[User]: \n{userinput}")
  else:
    userinput = str(input("[User]: ")) + "█" # userinput
  print()

  for i in userinput.lower().split():
    decimal = False

    # if theres a dot, check if its decimal or not
    if '.' in i: # if theres a dot inside the userinput

      for b in range(len(i)): # loop through the word
        if (i[b] == '.') and (i[b-1] in NUMBERS_KEYWORDS) and (i[b+1] in NUMBERS_KEYWORDS): # if theres a dot, and the things around it are numbers
          decimal = True
          break

        else:
          decimal = False

      if decimal: # if its a decimal
        sentence.append(i)

      else: # prolly a punctuation
        sentence.append(i.replace('.',''))
        sentences.append(sentence)
        sentence = []

    # seperate sentences by punctuation since you can say 2 non-related ideas
    elif ('!' in i) or ('?' in i) or ('█' in i):
      sentence.append(i.replace('!','').replace('?','').replace('█',''))
      sentences.append(sentence)
      sentence = []

    else:
      sentence.append(i.replace(',', ''))

  # packs sentences into a packet object and is the sentence delegator section
  for a in range(len(sentences)):

    text = ' '.join(sentences[a])
    context = packet_evaluator(sentences[a])

    packets.append(pack(text, context))

  # merge packets
  i = 0
  while i < len(packets):
    current_mode = packets[i].mode # compares packet 1 with the rest
    tosend += packets[i].item + "█ "
    i += 1

    # Merge subsequent packets with the same mode
    while i < len(packets) and packets[i].mode == current_mode:
      tosend += packets[i].item + "█ "
      i += 1

    # packs the merged packet and append
    tosend += "MADE_BY_AUFY_MULYADI█"
    packet = pack(tosend, current_mode)
    merged.append(packet)
    tosend = ""

  # debug
  if PACKET_DEBUG:
    print(f"sentences   | {sentences}")
    print("=================================")

    # prints all the packets it can see
    for i in packets:
      print(f"packet type | {i.mode}")
      print(f"sentence    | {i.item}")
      print()

    print("=================================")
    # prints all the merged packets
    for i in merged:
      print(f"Merged packet item | {i.item}")
      print(f"Merged packet type | {i.mode}")
      print()
    
    # exits if we specified if we are only testing the sentence delegator
    exit() if TEST_COMPREHENSION else None

  ####################################################################
  #                         Processing                               #
  ####################################################################

  display("[Chatbot]:")
  for packet in merged:
    
    ##################################
    # system command
    if packet.mode == "system": 
      display("")
      command = system_interpreter(packet.item, DEBUG)

      if command == "ERROR":
        display("")
        display("---------------")
        display("whoops! looks like there's an error")
        display("no changes will be made to the system")

      elif command == "<<greet off":
        greet = False

      elif command == "request: shut down":
        exit()
        
    ##################################
    # math interpreter
    elif packet.mode == "math": 
      display(greeting if greet else "")
      math_interpreter(packet.item, DEBUG)
      
    ##################################
    # webscraper interpreter
    elif packet.mode == "inquiery": 
      if reconnect(3):
        reaserch_interpreter(packet.item, DEBUG, results_shown, sentence_length)

      else:
        display("i could not connect to the internet to find out")
        display("please check your internet connection and try again")

    ##################################
    # chatting mode
    elif packet.mode == "chatting": 
      chatting_interpreter(packet.item, DEBUG)

    ##################################
    # define mode
    elif packet.mode == "define": 
      definition_interpreter(packet.item, DEBUG)

    ##################################
    # offensive word
    elif packet.mode == "offensive":
      crashout += 1
      
      if crashout == 1:
        display("whoa whoa whoa! lets keep it clean and respectable here")
        display("i dont want to hear anything of that kind anymore from now on, do you understand?")
        display("warning 1/3")
      
      elif crashout == 2:
        display("what did i say about using that kind of language?")
        display("if you still continue, i will have to shut down")
        display("please keep it clean and respectful")
        display("warning 2/3")
        
      elif crashout == 3:
        display("since you keep using that kind of language, i lost all my respect for you")
        display("i warned you - warning 3/3")
        
        display("reporting incident...")
        time.sleep(0.75)
        display("deleting garbage...")
        time.sleep(0.75)
        display("closing background processes...")
        time.sleep(0.75)
        display("shutting down...")
        time.sleep(0.75)
        exit()
        break
    
    ##################################
    # unknown
    else:
      display("Im sorry, but i could not understand your sentence")
      display("please refrain from using slang words or abbreviations and please")
      display("adhere to standard english grammar rules, dont forget to check your spelling")

  if DEVELOPER_MODE:
    display("-----")
    display("Developer mode, program will automatically stop")
    exit()
    break