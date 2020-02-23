"""
	Author: Luis Angel Hernandez Garcia
	Date: February 14, 2020

	This program implements RC4 stream cipher
"""

import fileinput

# Key-scheduling algorithm
def KSA(key):
	# S initialized to the identity permutation
	S = [i for i in range(256)]

	j = 0
	# S is processed for 256 iterations, mixing in bytes of the key 
	for i in range(256):
		j = (j + S[i] + ord(key[i % len(key)])) % 256
		S[i], S[j] = S[j], S[i] # swap values of S[i] and S[j]

	return S

# Pseudo-random generation algorithm
def PRGA(i, j, S):
	# increment of i, looking for the i-th element of S
	i = (i + 1) % 256
	# The i-th element of S is added to j
	j = (j + S[i]) % 256
	S[i], S[j] = S[j], S[i] # swap values of S[i] and S[j]
	k = S[(S[i] + S[j]) % 256] # the byte of the keystream is created
	return i, j, k


def RC4(key, message):
	S = KSA(key)
	i, j, k = 0, 0, 0
	
	c = []
	# each message element is XORed with each element of the keystream
	for e in message:
		i, j, k = PRGA(i, j, S)
		c.append(ord(e) ^ k)

	return "".join(["%02X"%(e) for e in c]) # output format

def main():
	lines = []
	
	for line in fileinput.input():
		lines.append(line.replace('\n',''))

	print(RC4(lines[0], lines[1]))

main()