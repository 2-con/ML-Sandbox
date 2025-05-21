"""DOCSTRING
made in 20/1/2025 (d/m/y)

To-do:

 - 

Notes:

not reccomended to train AI in google collab bc its slow.

ik its tedious (and annoying) to upgrade both the training model and the game model but sometimes they are imcompatible with
each other

definitions
  "attacking" - blocking an opponent's movement

"""

# imports =====================================================================================

import random
import matplotlib.pyplot as plt

# classes =====================================================================================

class block:# organize steps
  def __init__(self,preliminary,result):
    self.prelim = preliminary
    self.result = result

class path:# organize paths (rounds)
  def __init__(self,path,result,length):
    self.path = path
    self.result = result
    self.length = length

class blacklist:# organize blacklists
  def __init__(self,preliminary,blacklistspot):
    self.prelim = preliminary
    self.coords = blacklistspot

class debug:# organize debugging
  def __init__(self,win,lose,tie):
    self.win = win
    self.lose = lose
    self.tie = tie

  def debug_win(self):
    for a in range(len(win)):
      for b in range(len(win[a].path)):
        print(win[a].path[b].prelim)
        print(win[a].path[b].result)
        print()
      print(f"WINNER = {win[a].result}")
      print(f"LENGTH = {win[a].length}")
      print("END OF ROUND\n")

  def debug_lose(self):
    for c in lose:
      print(c[0].prelim)
      print(c[0].coords)

  def debug_tie(self):
    for a in range(len(tie)):
      for b in range(len(tie[a].path)):
        print(tie[a].path[b].prelim)
        print(tie[a].path[b].result)
        print()
      print(f"WINNER = {tie[a].result}")
      print(f"LENGTH = {tie[a].length}")
      print("END OF ROUND\n")

class graphing: # organize data for graphing
  def __init__(self, round_number, number_of_wins, number_of_losses, number_of_ties, WINaccuracy, ALLaccuracy):
    self.round = round_number
    self.win = number_of_wins
    self.lose = number_of_losses
    self.tie = number_of_ties
    self.Waccuracy = WINaccuracy
    self.Aaccuracy = ALLaccuracy

# functions =====================================================================================

def check(board):# checks for a winner and returns 'X' or 'O' or None or TIE respectively
  win = []
  blanks = 0

  # rows (-)
  for row in board:
    if all(x == row[0] for x in row) and row[0] != ' ':
      return row[0]

  # columns (|)
  for i in range(BOARDSIZE):
    column = [row[i] for row in board]

    if all(x == column[0] for x in column) and column[0] != ' ':
      return column[0]

  # diagonal (\)
  diag1 = [board[i][i] for i in range(BOARDSIZE)]

  if all(x == diag1[0] for x in diag1) and diag1[0] != ' ':
      return diag1[0]

  # diagonal (/)
  diag2 = [board[i][(BOARDSIZE-1)-i] for i in range(BOARDSIZE)]

  if all(x == diag2[0] for x in diag2) and diag2[0] != ' ':
      return diag2[0]

  # scans through all options and count blanks
  for a in board:
    for b in a:
      if b == ' ':
        blanks += 1

  # if there are no blanks, its a tie
  if blanks == 0:
    return 'TIE'

  # no win
  return None

def display(board):# display the board nicely (purely asthetic)
  step = 0
  top = "         "
  row = ""
  COLUMN = "column"

  # adjusts the "column" sign to the middle
  while len(COLUMN) <= len(board)*2:
    COLUMN = "  " + COLUMN

  print(f"        " + COLUMN)

  # adjusts the colunms according to the size of the board
  for i in range(len(board)):
    top += (str(i+1)+"   ")

  print(top)

  # adnjusts the rows according to the size of the board
  for a in range(len(board)):
    for b in range(len(board[a])):
      row += f" {board[a][b]} |"

    print(f" row {a+1} |" + row)
    row = ""

def training_stats(AI):
  print("\n================================ Debugging ================================ \n")
  print("------------ Wins ----------------------------- \n")
  AI.debug_win()
  print("------------ Ties ----------------------------- \n")
  AI.debug_tie()
  print("------------ Blacklists ----------------------- \n")
  AI.debug_lose()

def pad(input,length):
  answer = str(input)

  while len(str(answer)) < length:
    answer = answer + " "

  return answer

def display_stat(count,win_score,lose_score,tie_score,board):
  if lose_score >= 1:
    print(f"Game {pad(count+1,6)} | {pad(win_score,6)} Wins | {pad(lose_score,6)} Losses | {pad(tie_score,6)} ties | Game result { (check(board)+'  ' if check(board) != 'TIE' else check(board)) if check(board) != None else 0} | Ratio {pad(round(((win_score+tie_score)/lose_score),3),6)} | Win% {pad(round(100*(win_score/(count+1)),3),6)} % | All% {pad(round(100*((win_score+tie_score)/(count+1)),3),6)} %")
  else:
    # makes sure there is no division by 0
    print(f"Game {pad(count+1,6)} | {pad(win_score,6)} Wins | {pad(lose_score,6)} Losses | {pad(tie_score,6)} ties | INSUFFICIENT DATA")

  pass

# variables =====================================================================================

count = 0 # counts how many training sessions the AI did
step = 0 # keeps track of who is going to play in the actual game

win_score = 0 # keeps track of wins
lose_score = 0 # keeps track of losses
tie_score = 0 # keeps track of ties

randomA = [] # saves available options after blacklists are processed. stands for 'random ALL'
randomX = 0 # saves random number to check under row
randomY = 0 # saves random number to check under column

found = False # checks weather to move on after finding a preliminary and the result
available = [] # checks for available optionss as a list of tuples that specifies position

graph_game = [] # stores values for graphing

round_  = [] # one round of preliminaries and results
temporary = [] # temporary list for blacklists, the reason its a list is because i can modify the scope

preliminary = [] # what the AI sees
result = [] # what the AI should do

win = [] # places to place given prelim, these are for the AI
tie = [] # if there are no more moves that leads to win
lose = [] # places to avoid placing given prelim

V3row_counter = 0 # converts row list into row position in V3
V4continue = False # checks if its no longer the 1st move

# game initialization
BOARDSIZE = 3 # the size of the board, default = 3x3
board = [[' ' for i in range(BOARDSIZE)] for i in range(BOARDSIZE)]

# aesthetics
LINE = "------------------------------" # visually seperate stuff
SHOWGAMEHISTORY = False # wether to display the COMPLETE game history during training or not
PLAY = True # False = developer mode | True = player mode
GRAPH = True # weather to graph the training

# hyperparameters
BLACKLIST_SCOPE = 2 # how far the AI should learn from its mistakes / the weight of the punishment
SESSIONS        = 20000 # how much sessions is the AI trained on
VERSION         = 1 # switches which AI model is playing

"""list of available AI models:
This is NOT a ranking!
----------------------

1 | 1st and most rudementary version
2 | learning method overhaul
3 | prioritizes neutralizing enemies
5 | more balanced strategy, bassically No.4 but compatible with all board sizes

4 | spesifically made for the 3x3 classic board

"""

# main function =====================================================================================

if VERSION == 1:
  while count < SESSIONS:

    display_stat(count,win_score,lose_score,tie_score,board)
    graph_game.append(graphing(count,win_score,lose_score,tie_score,round(100*(win_score/count),5) if count > 1 else 0,round(100*((win_score+tie_score)/count),5) if count > 1 else 0))

    count += 1

    board = [[' ' for i in range(BOARDSIZE)] for i in range(BOARDSIZE)]

    round_ = []
    temporary = []

    preliminary = []
    result = []

    while check(board) == None:

      # trainer's input
      while board[randomX][randomY] != ' ':
        randomX = random.randint(0,BOARDSIZE-1)
        randomY = random.randint(0,BOARDSIZE-1)
      board[randomX][randomY] = 'O'

      # breaks out of the loop in case it wins
      if check(board) != None:
        break
      preliminary = [i[:] for i in board] # makes a copy for prelim

      # AI's input
      while board[randomX][randomY] != ' ':
        randomX = random.randint(0,BOARDSIZE-1)
        randomY = random.randint(0,BOARDSIZE-1)
      board[randomX][randomY] = 'X'

      temporary.append(blacklist(preliminary,(randomX,randomY))) # stores prelim and (result as coords) for blacklist in case it lost
      result = [i[:] for i in board] # makes a copy for result

      round_.append(block(preliminary, result))

    # post-game processing ----------------------------------

    # sort the main libraries
    win = sorted(win, key=lambda block: block.length)
    tie = sorted(tie, key=lambda block: block.length)

    # proccesing end condition
    if check(board) == 'X':# if the AI wins
      win.append(path(round_,'X',len(round_)))
      win_score += 1

    elif check(board) == 'O':# if the AI loses
      lose.append(temporary[-1:])
      lose_score += 1

    else:# if tie
      tie.append(path(round_,'TIE',len(round_)))
      tie_score += 1

elif VERSION in [2,3,4,5]:
  while count < SESSIONS:

    display_stat(count,win_score,lose_score,tie_score,board)
    graph_game.append(graphing(count,win_score,lose_score,tie_score,round(100*(win_score/count),5) if count > 1 else 0,round(100*((win_score+tie_score)/count),5) if count > 1 else 0))

    count += 1

    board = [[' ' for i in range(BOARDSIZE)] for i in range(BOARDSIZE)]

    round_ = []
    temporary = []

    preliminary = []
    result = []

    while check(board) == None:
      found = False

      # trainer's input
      while board[randomX][randomY] != ' ':
        randomX = random.randint(0,BOARDSIZE-1)
        randomY = random.randint(0,BOARDSIZE-1)
      board[randomX][randomY] = 'O'

      # breaks out of the loop in case it wins
      if check(board) != None:
        break
      preliminary = [i[:] for i in board] # makes a copy for prelim

      # AI's input
      if VERSION < 3:
        # checks inside [win] for answer
        for a in range(len(win)):
          for b in range(len(win[a].path)):
            if board == win[a].path[b].prelim: # if the board matches with any preliminaries inside win>path
              board = [i[:] for i in win[a].path[b].result]

              found = True
              break # breaks from the inner loop

          if found:
            break # breaks from the outer loop

      elif VERSION == 2:
        # if there is none in [win], try:
        if found == False:
          # check for blacklisted preliminaries
          for i in lose:
            if board == i[0].prelim: # if the board matches with any blacklisted preliminaries inside loses

              # scans for available spots / empty slots and append them to [available]
              for a in range(BOARDSIZE):
                for b in range(len(board[a])):
                  if board[a][b] == ' ':
                    available.append((a,b))

              # removes blacklisted spots
              for x in available:
                if x == i[0].coords:
                  available.remove(x)

              # pick a random spot form the avilable slots
              randomA = available[random.randint(0,len(available)-1)]
              randomX = randomA[0]
              randomY = randomA[1]

              # picks a random spot that is not blacklisted and is available
              board[randomX][randomY] = 'X'

              found = True
              break

      elif VERSION == 3:

        # checks inside [win] for answer
        if found == False:
          for a in range(len(win)):
            for b in range(len(win[a].path)):
              if board == win[a].path[b].prelim: # if the board matches with any preliminaries inside win>path
                board = [i[:] for i in win[a].path[b].result]

                found = True
                break # breaks from the inner loop

            if found:
              break # breaks from the outer loop

        # check for [OO ]
        if found == False:
          # rows (-)
          if found == False:
            V3row_counter = 0
            for i in board:
              if (i.count('O') == BOARDSIZE-1) and (i.count(' ') == 1):
                board[V3row_counter][i.index(' ')] = 'X'
                found = True

              V3row_counter += 1

          # columns (|)
          if found == False:
            for i in range(BOARDSIZE):
              if ([row[i] for row in board].count('O') == BOARDSIZE-1) and ([row[i] for row in board].count(' ') == 1):
                board[[row[i] for row in board].index(' ')][i] = 'X'
                found = True

          # diagonal (\)
          if found == False:
            if ([board[i][i] for i in range(BOARDSIZE)].count('O') == BOARDSIZE-1) and ([board[i][i] for i in range(BOARDSIZE)].count(' ') == 1):
              for i in range(BOARDSIZE):
                if board[i][i] == ' ':
                  board[i][i] = 'X'
                  found = True

          # diagonal (/)
          if found == False:
            if ([board[i][2-i] for i in range(BOARDSIZE)].count('O') == BOARDSIZE-1) and ([board[i][2-i] for i in range(BOARDSIZE)].count(' ') == 1):
              for i in range(BOARDSIZE):
                if board[i][2-i] == ' ':
                  board[i][2-i] = 'X'
                  found = True

        if found == False:
          # check for blacklisted preliminaries
          for i in lose:
            if board == i[0].prelim: # if the board matches with any blacklisted preliminaries inside loses
              # scans for available spots / empty slots and append them to [available]
              for a in range(BOARDSIZE):
                for b in range(len(board[a])):
                  if board[a][b] == ' ':
                    available.append((a,b))

              # removes blacklisted spots
              for x in available:
                if x == i[0].coords:
                  available.remove(x)

              # pick a random spot form the avilable slots
              randomA = available[random.randint(0,len(available)-1)]
              randomX = randomA[0]
              randomY = randomA[1]

              # picks a random spot that is not blacklisted and is available
              board[randomX][randomY] = 'X'

              found = True
              break

      elif VERSION == 4:
        # dont seperate these two, it makes it easier to troubleshoot
        if V4continue == False:
          # checks if theres one O in the corner
          if found == False:
            if (board[0][0] == 'O') or (board[0][2] == 'O') or (board[2][0] == 'O') or (board[2][2] == 'O'):
              board[1][1] = 'X'
              found = True
              V4continue = True

          # checks if theres one O in the edge
          if found == False:
            if (board[0][1] == 'O') or (board[1][0] == 'O') or (board[1][2] == 'O') or (board[2][1] == 'O'):
              board[1][1] = 'X'
              found = True
              V4continue = True

          # checks if theres one O in the middle
          if found == False:
            if board[1][1] == 'O':
              if random.randint(0,1) == 1:
                if random.randint(0,1):
                  board[0][0] = 'X'
                  found = True
                  V4continue = True
                else:
                  board[0][2] = 'X'
                  found = True
                  V4continue = True
              else:
                if random.randint(0,1):
                  board[2][0] = 'X'
                  found = True
                  V4continue = True
                else:
                  board[2][2] = 'X'
                  found = True
                  V4continue = True

        V4continue = True

        # scans board for [X X]
        if found == False:
          # rows (-)
          if found == False:
            V3row_counter = 0
            for i in board:
              if (i.count('X') == 2) and (i.count(' ') == 1):
                board[V3row_counter][i.index(' ')] = 'X'
                found = True
              V3row_counter += 1

          # columns (|)
          if found == False:
            for i in range(BOARDSIZE):
              if ([row[i] for row in board].count('X') == 2) and ([row[i] for row in board].count(' ') == 1):
                board[[row[i] for row in board].index(' ')][i] = 'X'
                found = True

          # diagonal (\)
          if found == False:
            if ([board[i][i] for i in range(BOARDSIZE)].count('X') == 2) and ([board[i][i] for i in range(BOARDSIZE)].count(' ') == 1):
              for i in range(BOARDSIZE):
                if board[i][i] == ' ':
                  board[i][i] = 'X'
                  found = True

          # diagonal (/)
          if found == False:
            if ([board[i][2-i] for i in range(BOARDSIZE)].count('X') == 2) and ([board[i][2-i] for i in range(BOARDSIZE)].count(' ') == 1):
              for i in range(BOARDSIZE):
                if board[i][2-i] == ' ':
                  board[i][2-i] = 'X'
                  found = True

        # scans board for [OO ]
        if found == False:
          # rows (-)
          if found == False:
            V3row_counter = 0
            for i in board:
              if (i.count('O') == 2) and (i.count(' ') == 1):
                board[V3row_counter][i.index(' ')] = 'X'
                found = True
              V3row_counter += 1

          # columns (|)
          if found == False:
            for i in range(BOARDSIZE):
              if ([row[i] for row in board].count('O') == 2) and ([row[i] for row in board].count(' ') == 1):
                board[[row[i] for row in board].index(' ')][i] = 'X'
                found = True

          # diagonal (\)
          if found == False:
            if ([board[i][i] for i in range(BOARDSIZE)].count('O') == 2) and ([board[i][i] for i in range(BOARDSIZE)].count(' ') == 1):
              for i in range(BOARDSIZE):
                if board[i][i] == ' ':
                  board[i][i] = 'X'
                  found = True

          # diagonal (/)
          if found == False:
            if ([board[i][2-i] for i in range(BOARDSIZE)].count('O') == 2) and ([board[i][2-i] for i in range(BOARDSIZE)].count(' ') == 1):
              for i in range(BOARDSIZE):
                if board[i][2-i] == ' ':
                  board[i][2-i] = 'X'
                  found = True

         # scans for [ X ]
        if found == False:
          # rows (-)
          if found == False:
            V3row_counter = 0
            for i in board:
              if (i.count('X') == 1) and (i.count(' ') == 2):
                board[V3row_counter][i.index(' ')] = 'X'
                found = True
              V3row_counter += 1

          # columns (|)
          if found == False:
            for i in range(BOARDSIZE):
              if ([row[i] for row in board].count('X') == 1) and ([row[i] for row in board].count(' ') == 2):
                board[[row[i] for row in board].index(' ')][i] = 'X'
                found = True

          # diagonal (\)
          if found == False:
            if ([board[i][i] for i in range(BOARDSIZE)].count('X') == 1) and ([board[i][i] for i in range(BOARDSIZE)].count(' ') == 2):
              for i in range(BOARDSIZE):
                if board[i][i] == ' ':
                  board[i][i] = 'X'
                  found = True

          # diagonal (/)
          if found == False:
            if ([board[i][2-i] for i in range(BOARDSIZE)].count('X') == 1) and ([board[i][2-i] for i in range(BOARDSIZE)].count(' ') == 2):
              for i in range(BOARDSIZE):
                if board[i][2-i] == ' ':
                  board[i][2-i] = 'X'
                  found = True
      
      elif VERSION == 5:

        # checks inside [win] for answer
        if found == False:
          for a in range(len(win)):
            for b in range(len(win[a].path)):
              if board == win[a].path[b].prelim: # if the board matches with any preliminaries inside win>path
                board = [i[:] for i in win[a].path[b].result]

                found = True
                break # breaks from the inner loop

            if found:
              break # breaks from the outer loop
            
        # scans board for [X X]
        if found == False:
          # rows (-)
          if found == False:
            V3row_counter = 0
            for i in board:
              if (i.count('X') == BOARDSIZE-1) and (i.count(' ') == 1):
                board[V3row_counter][i.index(' ')] = 'X'
                found = True
              V3row_counter += 1

          # columns (|)
          if found == False:
            for i in range(BOARDSIZE):
              if ([row[i] for row in board].count('X') == BOARDSIZE-1) and ([row[i] for row in board].count(' ') == 1):
                board[[row[i] for row in board].index(' ')][i] = 'X'
                found = True

          # diagonal (\)
          if found == False:
            if ([board[i][i] for i in range(BOARDSIZE)].count('X') == BOARDSIZE-1) and ([board[i][i] for i in range(BOARDSIZE)].count(' ') == 1):
              for i in range(BOARDSIZE):
                if board[i][i] == ' ':
                  board[i][i] = 'X'
                  found = True

          # diagonal (/)
          if found == False:
            if ([board[i][2-i] for i in range(BOARDSIZE)].count('X') == BOARDSIZE-1) and ([board[i][2-i] for i in range(BOARDSIZE)].count(' ') == 1):
              for i in range(BOARDSIZE):
                if board[i][2-i] == ' ':
                  board[i][2-i] = 'X'
                  found = True

        # check for [OO ]
        if found == False:
          # rows (-)
          if found == False:
            V3row_counter = 0
            for i in board:
              if (i.count('O') == BOARDSIZE-1) and (i.count(' ') == 1):
                board[V3row_counter][i.index(' ')] = 'X'
                found = True

              V3row_counter += 1

          # columns (|)
          if found == False:
            for i in range(BOARDSIZE):
              if ([row[i] for row in board].count('O') == BOARDSIZE-1) and ([row[i] for row in board].count(' ') == 1):
                board[[row[i] for row in board].index(' ')][i] = 'X'
                found = True

          # diagonal (\)
          if found == False:
            if ([board[i][i] for i in range(BOARDSIZE)].count('O') == BOARDSIZE-1) and ([board[i][i] for i in range(BOARDSIZE)].count(' ') == 1):
              for i in range(BOARDSIZE):
                if board[i][i] == ' ':
                  board[i][i] = 'X'
                  found = True

          # diagonal (/)
          if found == False:
            if ([board[i][2-i] for i in range(BOARDSIZE)].count('O') == BOARDSIZE-1) and ([board[i][2-i] for i in range(BOARDSIZE)].count(' ') == 1):
              for i in range(BOARDSIZE):
                if board[i][2-i] == ' ':
                  board[i][2-i] = 'X'
                  found = True

        if found == False:
          # check for blacklisted preliminaries
          for i in lose:
            if board == i[0].prelim: # if the board matches with any blacklisted preliminaries inside loses
              # scans for available spots / empty slots and append them to [available]
              for a in range(BOARDSIZE):
                for b in range(len(board[a])):
                  if board[a][b] == ' ':
                    available.append((a,b))

              # removes blacklisted spots
              for x in available:
                if x == i[0].coords:
                  available.remove(x)

              # pick a random spot form the avilable slots
              randomA = available[random.randint(0,len(available)-1)]
              randomX = randomA[0]
              randomY = randomA[1]

              # picks a random spot that is not blacklisted and is available
              board[randomX][randomY] = 'X'

              found = True
              break
      
      # if all fails, roll a dice and hope for the best
      if found == False:
        # inputs randomly
        while board[randomX][randomY] != ' ':
          randomX = random.randint(0,BOARDSIZE-1)
          randomY = random.randint(0,BOARDSIZE-1)
        board[randomX][randomY] = 'X'

      temporary.append(blacklist(preliminary,(randomX,randomY))) # stores prelim and (result as coords) for blacklist in case it lost
      result = [i[:] for i in board] # makes a copy for result

      round_.append(block(preliminary, result))

    # post-game processing ----------------------------------

    # sort the main libraries
    win = sorted(win, key=lambda block: block.length)
    tie = sorted(tie, key=lambda block: block.length)

    # proccesing end condition
    if check(board) == 'X':# if the AI wins
      win.append(path(round_,'X',len(round_)))
      win_score += 1

    elif check(board) == 'O':# if the AI loses
      lose.append(temporary[-BLACKLIST_SCOPE:])
      lose_score += 1

    else:# if tie
      tie.append(path(round_,'TIE',len(round_)))
      tie_score += 1

else:
  print(LINE)
  print("\nInvalid AI model!")
  print(f"There is no AI V{VERSION} as of now\n")
  print(LINE)
  exit()

# post-training processing --------------------------------

# sort the main libraries
win = sorted(win, key=lambda block: block.length)
tie = sorted(tie, key=lambda block: block.length)

# debugging

if SHOWGAMEHISTORY:
  training_stats(debug(win,lose,tie))

if GRAPH:
  plt.subplot(2,1,2)
  plt.plot([i.round for i in graph_game],[i.win for i in graph_game], c = '#03fc03')
  plt.plot([i.round for i in graph_game],[i.tie for i in graph_game], c = '#f78605')
  plt.plot([i.round for i in graph_game],[i.lose for i in graph_game], c = '#f70d05')

  plt.subplot(2,1,1)
  plt.plot([i.round for i in graph_game],[i.Waccuracy for i in graph_game], c = '#2505f7')
  plt.plot([i.round for i in graph_game],[i.Aaccuracy for i in graph_game], c = '#059ef7')
  plt.plot([i.round for i in graph_game],[(100-i.Aaccuracy) for i in graph_game], c = '#ab1a7f')

  plt.title(f"AI Model {VERSION} | {BOARDSIZE}x{BOARDSIZE} Board", loc='center', fontsize = '13', y =1.09)
  plt.title("Wins = green | Ties = orange | Losses = red | Win% = blue | All% = cyan | Lose% = purple", loc='left', fontsize = '8', y=1.0)

  plt.show()

# Actual game =======================================================================================

# universal settings

V4continue = False

if PLAY: # normal game settings
  print("\n================================ Game ================================ \n")
  print(f"Tictactoe AI V{VERSION}")

  board = [[' ' for i in range(BOARDSIZE)] for i in range(BOARDSIZE)]

  print(f"START GAME")
  display(board)
  print()
  print(LINE)

if PLAY == False: # Developer mode settings
  temporary = [blacklist([['O', ' ', 'X'], ['X', ' ', 'O'], ['O', 'X', 'O']],(0, 1))]
  lose.append(temporary)

  board = [
    ['O', 'O', ' '],
    [' ', ' ', ' '],
    ['X', ' ', ' ']
    ]

  V4continue = True

  print("\n================================ TEST CASE ================================ \n")
  print(f"Tictactoe AI Model {VERSION}")
  print("PRELIMINARY" + LINE)
  display(board)

while check(board) == None:

  found = False
  step += 1
  row = 0
  column = 0

  if (step % 2 == 1) and (PLAY): # player input
    print("\n        Your turn")

    row = int(input("ROW = "))-1
    column = int(input("COLUMN = "))-1
    board[row][column] = 'O'

    display(board)
    print()

  else: # AI input
    if VERSION < 3:
      # checks inside [win] for answer
      for a in range(len(win)):
        for b in range(len(win[a].path)):
          if board == win[a].path[b].prelim: # if the board matches with any preliminaries inside win>path
            board = [i[:] for i in win[a].path[b].result]

            found = True
            break # breaks from the inner loop

        if found:
          break # breaks from the outer loop

    elif VERSION == 2:
      # if there is none in [win], try:
      if found == False:
        # check for blacklisted preliminaries
        for i in lose:
          if board == i[0].prelim: # if the board matches with any blacklisted preliminaries inside loses

            # scans for available spots / empty slots and append them to [available]
            for a in range(BOARDSIZE):
              for b in range(len(board[a])):
                if board[a][b] == ' ':
                  available.append((a,b))

            # removes blacklisted spots
            for x in available:
              if x == i[0].coords:
                available.remove(x)

            # pick a random spot form the avilable slots
            randomA = available[random.randint(0,len(available)-1)]
            randomX = randomA[0]
            randomY = randomA[1]

            # picks a random spot that is not blacklisted and is available
            board[randomX][randomY] = 'X'

            found = True
            break

    elif VERSION == 3:
      # checks inside [win] for answer
      if found == False:
        for a in range(len(win)):
          for b in range(len(win[a].path)):
            if board == win[a].path[b].prelim: # if the board matches with any preliminaries inside win>path
              board = [i[:] for i in win[a].path[b].result]

              found = True
              break # breaks from the inner loop

          if found:
            break # breaks from the outer loop

      # scans for [OO ]
      if found == False:
        # rows (-)
        if found == False:
          V3row_counter = 0
          for i in board:
            if (i.count('O') == BOARDSIZE-1) and (i.count(' ') == 1):
              board[V3row_counter][i.index(' ')] = 'X'
              found = True

            V3row_counter += 1

        # columns (|)
        if found == False:
          for i in range(BOARDSIZE):
            if ([row[i] for row in board].count('O') == BOARDSIZE-1) and ([row[i] for row in board].count(' ') == 1):
              board[[row[i] for row in board].index(' ')][i] = 'X'
              found = True

        # diagonal (\)
        if found == False:
          if ([board[i][i] for i in range(BOARDSIZE)].count('O') == BOARDSIZE-1) and ([board[i][i] for i in range(BOARDSIZE)].count(' ') == 1):
            for i in range(BOARDSIZE):
              if board[i][i] == ' ':
                board[i][i] = 'X'
                found = True

        # diagonal (/)
        if found == False:
          if ([board[i][2-i] for i in range(BOARDSIZE)].count('O') == BOARDSIZE-1) and ([board[i][2-i] for i in range(BOARDSIZE)].count(' ') == 1):
            for i in range(BOARDSIZE):
              if board[i][2-i] == ' ':
                board[i][2-i] = 'X'
                found = True

      if found == False:
        # check for blacklisted preliminaries
        for i in lose:
          if board == i[0].prelim: # if the board matches with any blacklisted preliminaries inside loses
            # scans for available spots / empty slots and append them to [available]
            for a in range(BOARDSIZE):
              for b in range(len(board[a])):
                if board[a][b] == ' ':
                  available.append((a,b))

            # removes blacklisted spots
            for x in available:
              if x == i[0].coords:
                available.remove(x)

            # pick a random spot form the avilable slots
            randomA = available[random.randint(0,len(available)-1)]
            randomX = randomA[0]
            randomY = randomA[1]

            # picks a random spot that is not blacklisted and is available
            board[randomX][randomY] = 'X'

            found = True
            break

    elif VERSION == 4:
      # dont seperate these two, it makes it easier to troubleshoot
      if V4continue == False:
        # checks if theres one O in the corner
        if found == False:
          if (board[0][0] == 'O') or (board[0][2] == 'O') or (board[2][0] == 'O') or (board[2][2] == 'O'):
            board[1][1] = 'X'
            found = True
            V4continue = True

        # checks if theres one O in the edge
        if found == False:
          if (board[0][1] == 'O') or (board[1][0] == 'O') or (board[1][2] == 'O') or (board[2][1] == 'O'):
            board[1][1] = 'X'
            found = True
            V4continue = True

        # checks if theres one O in the middle
          if found == False:
            if board[1][1] == 'O':
              if random.randint(0,1) == 1:
                if random.randint(0,1):
                  board[0][0] = 'X'
                  found = True
                  V4continue = True
                else:
                  board[0][2] = 'X'
                  found = True
                  V4continue = True
              else:
                if random.randint(0,1):
                  board[2][0] = 'X'
                  found = True
                  V4continue = True
                else:
                  board[2][2] = 'X'
                  found = True
                  V4continue = True

      V4continue = True

      # scans board for [X X]
      if found == False:
        # rows (-)
        if found == False:
          V3row_counter = 0
          for i in board:
            if (i.count('X') == 2) and (i.count(' ') == 1):
              board[V3row_counter][i.index(' ')] = 'X'
              found = True
            V3row_counter += 1

        # columns (|)
        if found == False:
          for i in range(BOARDSIZE):
            if ([row[i] for row in board].count('X') == 2) and ([row[i] for row in board].count(' ') == 1):
              board[[row[i] for row in board].index(' ')][i] = 'X'
              found = True

        # diagonal (\)
        if found == False:
          if ([board[i][i] for i in range(BOARDSIZE)].count('X') == 2) and ([board[i][i] for i in range(BOARDSIZE)].count(' ') == 1):
            for i in range(BOARDSIZE):
              if board[i][i] == ' ':
                board[i][i] = 'X'
                found = True

        # diagonal (/)
        if found == False:
          if ([board[i][2-i] for i in range(BOARDSIZE)].count('X') == 2) and ([board[i][2-i] for i in range(BOARDSIZE)].count(' ') == 1):
            for i in range(BOARDSIZE):
              if board[i][2-i] == ' ':
                board[i][2-i] = 'X'
                found = True

      # scans board for [OO ]
      if found == False:
        # rows (-)
        if found == False:
          V3row_counter = 0
          for i in board:
            if (i.count('O') == 2) and (i.count(' ') == 1):
              board[V3row_counter][i.index(' ')] = 'X'
              found = True
            V3row_counter += 1

        # columns (|)
        if found == False:
          for i in range(BOARDSIZE):
            if ([row[i] for row in board].count('O') == 2) and ([row[i] for row in board].count(' ') == 1):
              board[[row[i] for row in board].index(' ')][i] = 'X'
              found = True

        # diagonal (\)
        if found == False:
          if ([board[i][i] for i in range(BOARDSIZE)].count('O') == 2) and ([board[i][i] for i in range(BOARDSIZE)].count(' ') == 1):
            for i in range(BOARDSIZE):
              if board[i][i] == ' ':
                board[i][i] = 'X'
                found = True

        # diagonal (/)
        if found == False:
          if ([board[i][2-i] for i in range(BOARDSIZE)].count('O') == 2) and ([board[i][2-i] for i in range(BOARDSIZE)].count(' ') == 1):
            for i in range(BOARDSIZE):
              if board[i][2-i] == ' ':
                board[i][2-i] = 'X'
                found = True

      # scans for [ X ]
      if found == False:
        # rows (-)
        if found == False:
          V3row_counter = 0
          for i in board:
            if (i.count('X') == 1) and (i.count(' ') == 2):
              board[V3row_counter][i.index(' ')] = 'X'
              found = True
            V3row_counter += 1

        # columns (|)
        if found == False:
          for i in range(BOARDSIZE):
            if ([row[i] for row in board].count('X') == 1) and ([row[i] for row in board].count(' ') == 2):
              board[[row[i] for row in board].index(' ')][i] = 'X'
              found = True

        # diagonal (\)
        if found == False:
          if ([board[i][i] for i in range(BOARDSIZE)].count('X') == 1) and ([board[i][i] for i in range(BOARDSIZE)].count(' ') == 2):
            for i in range(BOARDSIZE):
              if board[i][i] == ' ':
                board[i][i] = 'X'
                found = True

        # diagonal (/)
        if found == False:
          if ([board[i][2-i] for i in range(BOARDSIZE)].count('X') == 1) and ([board[i][2-i] for i in range(BOARDSIZE)].count(' ') == 2):
            for i in range(BOARDSIZE):
              if board[i][2-i] == ' ':
                board[i][2-i] = 'X'
                found = True
    
    elif VERSION == 5:

      # checks inside [win] for answer
      if found == False:
        for a in range(len(win)):
          for b in range(len(win[a].path)):
            if board == win[a].path[b].prelim: # if the board matches with any preliminaries inside win>path
              board = [i[:] for i in win[a].path[b].result]

              found = True
              break # breaks from the inner loop

          if found:
            break # breaks from the outer loop
          
      # scans board for [X X]
      if found == False:
        # rows (-)
        if found == False:
          V3row_counter = 0
          for i in board:
            if (i.count('X') == BOARDSIZE-1) and (i.count(' ') == 1):
              board[V3row_counter][i.index(' ')] = 'X'
              found = True
            V3row_counter += 1

        # columns (|)
        if found == False:
          for i in range(BOARDSIZE):
            if ([row[i] for row in board].count('X') == BOARDSIZE-1) and ([row[i] for row in board].count(' ') == 1):
              board[[row[i] for row in board].index(' ')][i] = 'X'
              found = True

        # diagonal (\)
        if found == False:
          if ([board[i][i] for i in range(BOARDSIZE)].count('X') == BOARDSIZE-1) and ([board[i][i] for i in range(BOARDSIZE)].count(' ') == 1):
            for i in range(BOARDSIZE):
              if board[i][i] == ' ':
                board[i][i] = 'X'
                found = True

        # diagonal (/)
        if found == False:
          if ([board[i][2-i] for i in range(BOARDSIZE)].count('X') == BOARDSIZE-1) and ([board[i][2-i] for i in range(BOARDSIZE)].count(' ') == 1):
            for i in range(BOARDSIZE):
              if board[i][2-i] == ' ':
                board[i][2-i] = 'X'
                found = True

      # check for [OO ]
      if found == False:
        # rows (-)
        if found == False:
          V3row_counter = 0
          for i in board:
            if (i.count('O') == BOARDSIZE-1) and (i.count(' ') == 1):
              board[V3row_counter][i.index(' ')] = 'X'
              found = True

            V3row_counter += 1

        # columns (|)
        if found == False:
          for i in range(BOARDSIZE):
            if ([row[i] for row in board].count('O') == BOARDSIZE-1) and ([row[i] for row in board].count(' ') == 1):
              board[[row[i] for row in board].index(' ')][i] = 'X'
              found = True

        # diagonal (\)
        if found == False:
          if ([board[i][i] for i in range(BOARDSIZE)].count('O') == BOARDSIZE-1) and ([board[i][i] for i in range(BOARDSIZE)].count(' ') == 1):
            for i in range(BOARDSIZE):
              if board[i][i] == ' ':
                board[i][i] = 'X'
                found = True

        # diagonal (/)
        if found == False:
          if ([board[i][2-i] for i in range(BOARDSIZE)].count('O') == BOARDSIZE-1) and ([board[i][2-i] for i in range(BOARDSIZE)].count(' ') == 1):
            for i in range(BOARDSIZE):
              if board[i][2-i] == ' ':
                board[i][2-i] = 'X'
                found = True

      if found == False:
        # check for blacklisted preliminaries
        for i in lose:
          if board == i[0].prelim: # if the board matches with any blacklisted preliminaries inside loses
            # scans for available spots / empty slots and append them to [available]
            for a in range(BOARDSIZE):
              for b in range(len(board[a])):
                if board[a][b] == ' ':
                  available.append((a,b))

            # removes blacklisted spots
            for x in available:
              if x == i[0].coords:
                available.remove(x)

            # pick a random spot form the avilable slots
            randomA = available[random.randint(0,len(available)-1)]
            randomX = randomA[0]
            randomY = randomA[1]

            # picks a random spot that is not blacklisted and is available
            board[randomX][randomY] = 'X'

            found = True
            break
                
    # if all fails, roll a dice and hope for the best
    if found == False:
      # inputs randomly
      while board[randomX][randomY] != ' ':
        randomX = random.randint(0,BOARDSIZE-1)
        randomY = random.randint(0,BOARDSIZE-1)
      board[randomX][randomY] = 'X'

    if PLAY:
      print(f"\n        AI's guess")
      display(board)
      print("\n" + LINE)
    else:
      print(f"\nRESULT" + LINE)
      display(board)
      exit()

# endscreen

print(f"\nwinner = {check(board)}")
print("\nGame over================================================= \n")
