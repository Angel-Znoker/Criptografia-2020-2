"""
	Author: Luis Angel Hernandez Garcia
	Date: March 02, 2020

	This program implements MD2 hash function
"""
import fileinput

# The message is increased to be a multiple of 16 bytes
def padding(message):
	i = 16 - (len(message) % 16)
	for j in range(i): # "i" bytes of value "i" are appended
		message.append(i)

	return message

def checksum(message, S):
	# each Ci and L are set with 0 
	C = [0 for i in range(16)]
	L = 0

	# checksum calculation
	for i in range(len(message) // 16):
		for j in range(16):
			c = message[16 * i + j]
			C[j] = C[j] ^ S[c ^ L]
			L = C[j]

	# The padded message is increased with another 16 bytes (checksum)
	return message + C

def theHash(message, S):
	# initializing 48 bytes Xi to 0
	X = [0 for i in range(48)]

	# hash value calculation
	for i in range(len(message) // 16):
		for j in range(16):
			X[j + 16] = message[16 * i + j]
			X[j + 32] = X[j + 16] ^ X[j]
		t = 0
		for j in range(18):
			for k in range(48):
				t = X[k] ^ S[t]
				X[k] = t
			t = (t + j) % 256
	
	# The final hash value is the first 16 bytes of X
	return X[:16]

def md2(message):
	# Permutation of 0..255, called S
	S = [41, 46, 67, 201, 162, 216, 124, 1, 61, 54, 84, 161, 236, 240, 6, 19, 98, 167, 5, 243, 192, 199, 115, 140, 152, 147, 43, 217, 188, 76, 130, 202, 30, 155, 87, 60, 253, 212, 224, 22, 103, 66, 111, 24, 138, 23, 229, 18, 190, 78, 196, 214, 218, 158, 222, 73, 160, 251, 245, 142, 187, 47, 238, 122, 169, 104, 121, 145, 21, 178, 7, 63, 148, 194, 16, 137, 11, 34, 95, 33, 128, 127, 93, 154, 90, 144, 50, 39, 53, 62, 204, 231, 191, 247, 151, 3, 255, 25, 48, 179, 72, 165, 181, 209, 215, 94, 146, 42, 172, 86, 170, 198, 79, 184, 56, 210, 150, 164, 125, 182, 118, 252, 107, 226, 156, 116, 4, 241, 69, 157, 112, 89, 100, 113, 135, 32, 134, 91, 207, 101, 230, 45, 168, 2, 27, 96, 37, 173, 174, 176, 185, 246, 28, 70, 97, 105, 52, 64, 126, 15, 85, 71, 163, 35, 221, 81, 175, 58, 195, 92, 249, 206, 186, 197, 234, 38, 44, 83, 13, 110, 133, 40, 132, 9, 211, 223, 205, 244, 65, 129, 77, 82, 106, 220, 55, 200, 108, 193, 171, 250, 36, 225, 123, 8, 12, 189, 177, 74, 120, 136, 149, 139, 227, 99, 232, 109, 233, 203, 213, 254, 59, 0, 29, 57, 242, 239, 183, 14, 102, 88, 208, 228, 166, 119, 114, 248, 235, 117, 75, 10, 49, 68, 80, 180, 143, 237, 31, 26, 219, 153, 141, 51, 159, 17, 131, 20]
	message = padding(message) # padding calculation
	message = checksum(message, S) # checksum calculation
	return "".join("%02x"%(e) for e in theHash(message, S)) # hash value in hex

def main():
	lines = []
	for line in fileinput.input():
		lines.append(line.replace('\n','').replace('"',''))
	
	# encoding plain text with utf-8 and getting the decimal value of each character
	plaintext = [e for e in lines[0].encode("utf-8")] 
	
	print(md2(plaintext))

main()