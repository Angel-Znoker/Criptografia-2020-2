def encrypt(tableau, phrase):
	phrase = phrase.replace(' ', '')

	x = ""
	y = ""

	for e in phrase:
		for i in range(5):
			for j in range(5):
				if e == tableau[i][j]:
					x += str(i)
					y += str(j)

	x += y

	new = ""

	for i in range(0, len(x), 2):
		new += tableau[int(x[i])][int(x[i + 1])]
	
	return new

def decrypt(tableau, phrase):
	x = ""
	for e in phrase:
		for i in range(5):
			for j in range(5):
				if e == tableau[i][j]:
					x += str(i) + str(j)

	y = x[len(x) // 2:]
	x = x[:len(x) // 2]

	new = ""

	for i in range(len(x)):
		new += tableau[int(x[i])][int(y[i])]

	return new


def main():
	tableau = [['E', 'N', 'C', 'R', 'Y'], ['P', 'T', 'A', 'B', 'D'], ['F', 'G', 'H', 'I', 'K'], ['L', 'M', 'O', 'Q', 'S'], ['U', 'V', 'W', 'X', 'Z']]

	phrase = input()

	#print(encrypt(tableau, phrase))

	print(decrypt(tableau, phrase))

main()