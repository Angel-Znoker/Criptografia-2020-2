"""
	Author: Luis Angel Hernandez Garcia
	Date: February 23, 2020

	This program implements simplified DES
"""
import fileinput

# subkeys of each round (10 to 8 bits)
def getSubkeys(key):
	k1 = key[0] + key[6] + key[8] + key[3] + key[7] + key[2] + key[9] + key[5]
	k2 = key[7] + key[2] + key[5] + key[4] + key[9] + key[1] + key[8] + key[0]
	
	return k1, k2

# permutation of plaintext bits, b0 b1 b2 b3 b4 b5 b6 b7 -> b1 b5 b2 b0 b3 b7 b4 b6
def initialPermutation(plaintext):
	return plaintext[1] + plaintext[5] + plaintext[2] + plaintext[0] + plaintext[3] + plaintext[7] + plaintext[4] + plaintext[6]

# inverse permutation of plaintext bits, b0 b1 b2 b3 b4 b5 b6 b7 -> b3 b0 b2 b4 b6 b1 b7 b5
def inversePermutacion(plaintext):
	return plaintext[3] + plaintext[0] + plaintext[2] + plaintext[4] + plaintext[6] + plaintext[1] + plaintext[7] + plaintext[5]

def mixingFunction(k, r):
	# S-boxes
	S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
	S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

	# block expansion, 4 bits to 8 bits
	r = r[3] + r[0] + r[1] + r[2] + r[1] + r[2] + r[3] + r[0]

	r = ''.join([str(int(a) ^ int(b)) for a, b in zip(r,k)]) # subkey XOR expansion
	
	# S-boxes values
	vS = ''
	vS += '{0:02b}'.format(S0[int(r[0] + r[3], 2)][int(r[1] + r[2], 2)]) # S-box S0 value
	vS += '{0:02b}'.format(S1[int(r[4] + r[7], 2)][int(r[5] + r[6], 2)]) # S-box S1 value
	
	# permutation, x0 x1 x2 x3 -> x1 x3 x2 x0
	vS = vS[1] + vS[3] + vS[2] + vS[0]

	return vS
		

def feistelFunction(k, m):
	# left and right halves
	lH = m[:len(m)//2]
	rH = m[len(m)//2:]

	mV = mixingFunction(k, rH) # mixes key and right half

	# left half XOR mix value
	lH = ''.join([str(int(a) ^ int(b)) for a, b in zip(mV, lH)])

	return lH + rH # contenates left an right halves

def encryptionDecryption(ED, key, plaintext):
	if ED == 'E': # if need encryption
		k1, k2 = getSubkeys(key)
	else: # if need decryption
		k2, k1 = getSubkeys(key)

	plaintext = initialPermutation(plaintext)
	plaintext = feistelFunction(k1, plaintext) # round 1

	# switch left and right halves
	plaintext = plaintext[len(plaintext)//2:] + plaintext[:len(plaintext)//2]

	plaintext = feistelFunction(k2, plaintext) #round 2
	plaintext = inversePermutacion(plaintext)

	return plaintext


def main():
	lines = []
	
	for line in fileinput.input():
		lines.append(line.replace('\n',''))
	
	print(encryptionDecryption(lines[0], lines[1], lines[2]))

main()