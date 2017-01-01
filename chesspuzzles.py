# -m pip install python-chess==0.15.4 to get correct version of chess
# http://python-chess.readthedocs.io/en/v0.16.1/core.html documentation of chess package
# pip install selenium used to refresh the webpages we use to display the board
# http://stackoverflow.com/questions/16399355/refresh-a-local-web-page-using-python
# Can feed FEN string as param to board as string
# pip install nltk
import chess
import chess.uci
import chess.svg
import nltk
from selenium import webdriver
import time
import urllib
import urllib2
import chessaudio
import chessmove
import getpuzzles


chromedriver_path = 'C:/Users/Raghu/Downloads/chromedriver_win32_secondcopy/chromedriver'
# https://chromedriver.storage.googleapis.com/index.html download chromedriver 2.24 from
# this link and specify the file path as chromedriver_path.  I couldn't get chromedriver
# 2.25 (the most updated one) to work so I used an earlier version (2.24).

fileName = 'C:\Projects\ChessProject\curFile.html'
# Path to the file we will be writing to and displaying

use_voice = False

board = chess.Board()
start_board = chess.svg.board(board)
f = open(fileName, 'w')
f.write(start_board)
f.close()
# generating the board and writing it to the file

driver = webdriver.Chrome(chromedriver_path)
driver.get(fileName)
# Opening the page

engine = chess.uci.popen_engine("C:\Users\Raghu\Downloads\stockfish-7-win\stockfish-7-win\Windows\stockfish")
engine.uci()
print engine.name
print engine.author
# Setting up the engine which will evaluate user answers to the puzzles
# The parameter in chess.uci.popen_engine is the path to the engine executable.
# A powerful, free engine can be downloaded from stockfishchess.org
# I happen to be using this engine, but any engine should work.

masterFEN = ['4Rnk1/pr3ppp/1p3q2/5NQ1/2p5/8/P4PPP/6K1 w - - 1 0',
'4k2r/1R3R2/p3p1pp/4b3/1BnNr3/8/P1P5/5K2 w - - 1 0',
'7r/p3ppk1/3p4/2p1P1Kp/2Pb4/3P1QPq/PP5P/R6R b - - 0 1']

# masterFEN = getpuzzles.makePuzzles()
# This line when uncommented scrapes the puzzles from the website. 

numPuz = len(masterFEN)
numHint = 0.0 # Keeps track of number of hints used
timeList = []
master_time = time.time()
for key in masterFEN:
	start_time = time.time()
	board = chess.Board(key)
	# Generating the position from the FEN string
	toFlip = not board.turn 
	# If it is black to move, we want the board flipped so the 
	# user is looking at the position from black's perspective
	# board.turn returns true if white is to move and false if black is to move 

	input_board = chess.svg.board(board, flipped = toFlip) 
	# Creating the Board display
	engineMove = False
	f = open(fileName, 'w')
	f.write(input_board)
	f.close()
	# Overwriting the old version of the display file with the new version

	driver.refresh() # Now that the file has been overwritten, we want to reload the page
	while board.is_game_over() != True:
		if engineMove == True:
			engine.position(board) 
			# Getting the engine thinking about the position
			bestmove, ponder = engine.go(movetime = 3000)
			# Creating a tuple holding the best move in the position
			board.push(bestmove)
			# Updating our board 
			curBoard = chess.svg.board(board, flipped = toFlip)
			f = open(fileName, 'w')
			f.write(curBoard)
			f.close()
			driver.refresh()
			engineMove = False
		else:
			special_move = False
			# used to differentiate commands (like hint and voice) from moves
			engine.position(board)
			bestmove, ponder = engine.go(movetime = 3000)
			if use_voice == True:
				start_move_time = time.time()
				userMove = chessaudio.getVoice()
				if userMove.lower() == 'voice':
					print "voice has been toggled off"
 					special_move = not special_move
 					use_voice = False
				elif userMove.lower() == "invalid input":
					use_voice = use_voice
					special_move = not special_move
				elif userMove.lower() == "hint":
					numHint = numHint + 1
					print bestmove
					special_move = not special_move
				else:
					# now we want to take our move apart
					tokens = nltk.word_tokenize(userMove)
					if len(tokens) != 4:
						print "Sorry, your move couldn't be understoond.  Try using the 'voice' command to switch to text."
						special_move = not special_move
					else:
						userMove = chessmove.getMove(tokens)
				move_time = time.time() - start_move_time
			else:
				start_move_time = time.time()
				userMove = str(raw_input())
				if userMove == 'hint':
					numHint = numHint + 1
					print bestmove
					special_move = not special_move
				elif userMove == 'voice':
					special_move = not special_move
					if use_voice == False:
						use_voice = not use_voice
						print 'voice has been toggled on'
					else:
						use_voice = use_voice
				move_time = time.time() - start_move_time
			if not special_move:
				elapsed_time = time.time() - start_time - move_time
				if chess.Move.from_uci(userMove) == bestmove: # Checking if user move is correct
					board.push(bestmove) # updating board
					if board.is_game_over():
						timeList.append(elapsed_time)
					engineMove = True # informing engine to make next move
					curBoard = chess.svg.board(board, flipped = toFlip)
					f = open(fileName, 'w')
					f.write(curBoard)
					f.close()
					driver.refresh
				else:
					print "Sorry, that's wrong.  Please try again!  Don't forget to ask for a hint if you get stuck."

print "Congrats, you finished all the puzzles!  You used " + str(numHint/numPuz) + ' hints per puzzle.'
print "You spent the most time on puzzle number " + str(timeList.index(max(timeList)) + 1)
print "The FEN string for this puzzle is " + masterFEN[timeList.index(max(timeList))]
print "Overall, you used " + str(sum(timeList)) + " seconds to complete all the puzzles, which is an average of " + str(sum(timeList) / numPuz) + " seconds per puzzle"