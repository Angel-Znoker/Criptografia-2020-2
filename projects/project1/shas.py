import hashlib
import time
import csv

with open("shaTestVectors.txt", 'r') as file, open("timesSHA.csv", "w") as results:
	
	writer = csv.writer(results, quoting=csv.QUOTE_ALL)
	writer.writerow(["SHA-1", "SHA-2", "SHA-3"])
	
	times = [0,0,0]

	for line in file:

		line = line.replace("\"\"", "").replace("\n", "")

		message = line.encode()

		start = time.clock()
		SHA1 = hashlib.sha1(message).hexdigest()
		end = time.clock()

		print("SHA1: " + SHA1)
		times[0] = end-start

		start = time.clock()
		SHA256 = hashlib.sha256(message).hexdigest()
		end = time.clock()

		print("SHA2: "+ SHA256)
		times[1] = end-start

		start = time.clock()
		SHA3 =  hashlib.sha3_256(message).hexdigest()
		end = time.clock()

		print("SHA3-256: " + SHA3)
		times[2] = end-start

		writer.writerow(times)