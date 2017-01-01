# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags

import requests
from bs4 import BeautifulSoup


def makePuzzles():
	page = requests.get('https://www.sparkchess.com/chess-puzzles.html')

# page.content contains the HTML with the FENS in there somewhere

	soup = BeautifulSoup(page.content, 'html.parser')
	finalPuzzles = []
	formattedPuzzles = []
	puzzles = []
	links = []
	for link in soup.find_all('a'):
		links.append(link.get('href'))

	for key in links:
		if key[0:2] == '/?':
			puzzles.append(key[6:])

	# http://stackoverflow.com/questions/10037742/replace-part-of-a-string-in-python
	for key in puzzles:
		puz = key.replace('%2F', '/')
		formattedPuzzles.append(puz)

	# http://stackoverflow.com/questions/1178335/in-python-2-4-how-can-i-strip-out-characters-after
	for key in formattedPuzzles:
		puz = key.split("&")[0]
		puz2 = puz.replace('+', ' ')
		finalPuzzles.append(puz2)

	return finalPuzzles

