import time
import csv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

def AES_ECB(key, data):
	times = []

	cipher = AES.new(key, AES.MODE_ECB)

	start = time.clock()
	ct = cipher.encrypt(pad(data, AES.block_size))
	end = time.clock()

	times.append(end-start)

	start = time.clock()
	pt = unpad(cipher.decrypt(ct), AES.block_size)
	end = time.clock()

	times.append(end-start)

	return times


def  AES_CBC(key, data):

	times = []

	cipher = AES.new(key, AES.MODE_CBC)

	start = time.clock()
	ct = cipher.encrypt(pad(data, AES.block_size))
	end = time.clock()

	times.append(end-start)

	decipher = AES.new(key, AES.MODE_CBC, cipher.iv)

	start = time.clock()
	pt = unpad(decipher.decrypt(ct), AES.block_size)
	end = time.clock()

	times.append(end-start)

	return times

with open("aesTestVectors.csv", 'r') as file, open("timesAES.csv", "w") as results:
	
	writer = csv.writer(results, quoting=csv.QUOTE_ALL)
	writer.writerow(["AES-EBC E", "AES-EBC D", "AES-CBC E", "AES-CBC D"])

	for line in file:

		line = line.replace("\"\"", "").replace("\n", "")

		data = bytes(line, "utf-8")		
		key = get_random_bytes(32)

		tebc = AES_ECB(key, data)

		tcbc = AES_CBC(key, data)

		writer.writerow(tebc + tcbc)