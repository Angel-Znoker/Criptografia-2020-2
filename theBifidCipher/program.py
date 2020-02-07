"""
	Author: Luis Angel Hernandez Garcia
	Date: Febrary 6, 2020

	This program implements the Bifid cipher
"""

import fileinput

"""
	This function gets the indices of every character 
	of the phrase
"""
def getIndices(tableau, phrase):
	indices = []
	for c in phrase:
		for i in range(5):
			for j in range(5):
				if c == tableau[i][j]:
					indices.append(i)
					indices.append(j)

	return indices

"""
	This function returns the new message with the help of the
	tableau and the indices list.
"""
def newMessage(tableau, indices):
	new = ""

	# to get the characters, the indices pairs are taken from the list
	for i in range(0, len(indices), 2):
		new += tableau[indices[i]][indices[i + 1]]

	return new

def encrypt(tableau, phrase):
	indices = getIndices(tableau, phrase)

	# the i's indices are placed at the beginning of a new list
	indices2 = [indices[i] for i in range(0, len(indices), 2)]
	# then the j's indices are placed
	indices2 += [indices[i] for i in range(1, len(indices), 2)]

	new = newMessage(tableau, indices2)

	return new

def decrypt(tableau, phrase):
	indices = getIndices(tableau, phrase)
	indices2 = []
	# the division of the list is simulated
	# indices are taken "column by column"
	# and added to a new list
	for i in range(len(indices) // 2):
		indices2.append(indices[i])
		indices2.append(indices[i + len(phrase)])

	return newMessage(tableau, indices2)

def main():
	tableau = [['E', 'N', 'C', 'R', 'Y'], ['P', 'T', 'A', 'B', 'D'], ['F', 'G', 'H', 'I', 'K'], ['L', 'M', 'O', 'Q', 'S'], ['U', 'V', 'W', 'X', 'Z']]

	lines = []
	for line in fileinput.input():
		lines.append(line.replace('\n','').replace(' ',''))


	if lines[0] == "ENCRYPT":
		print(encrypt(tableau, lines[1]))
	else:
		print(decrypt(tableau, lines[1]))

main()