import chess
import chess.uci
import chess.svg

oneList = ['1', 'one', 'on']
twoList = ['2', 'two', 'to', 'too']
threeList = ['3', 'three', 'tree', 'thee', 'free']
fourList = ['4', 'four', 'for', 'fore']
fiveList = ['5', 'five']
sixlist = ['6', 'six', 'sticks', 'stick']
sevenList = ['7', 'seven', 'seen']
eightList = ['8', 'eight', 'ate', 'eighth', 'age']

aList = []
bList = []
cList = []
dList = []
eList = ['e', 'gecko']
fList = []
gList = []
hList = ['h', 'motel']
# These lists were going to be used for common mistranslations of
# NATO alphabet words that ended up starting with different letters
# However there was only 2 words that came up a lot so I just hard 
# coded it.  I may go back and revise these to contain more words
# if more users report errors.  I would have corrected the errors
# in the same way I corrected the number errors  


masterList = [oneList, twoList, threeList, fourList, fiveList, sixlist,
				sevenList, eightList]


def getMove(moveList): 
# By the structure of the code moveList must be a list of length 4 containing strings
	i = 0
	move = ''
	while i < len(moveList):
		# 0th or 2nd index, square designations
		# 1st or 3rd inded, number designations
		if i%2 == 0:
			if moveList[i].lower() == 'motel': # hotel becomes motel sometimes
				move = move + 'h'
				i = i + 1
			elif moveList[i].lower() == 'gecko': # echo becomes gecko sometimes
				move = move + 'e'
				i = i + 1
			else:
				move = move + moveList[i][0].lower()
				i = i + 1
		else:
			# Numbers
			for numList in masterList:
				if ( moveList[i] in numList):
					move = move + numList[0]
			i = i + 1
	return move

# NATO ALPHABET FOR Recognition
# a -> alpha
# b -> beta/bravo
# c -> charlie
# d -> delta
# e -> epsilon/echo
# f -> fox/foxtrot
# h -> hotel/hospital
