import time
import csv
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random

def RSA_OAEP(data, n, e, d):
    times = []

    privateKey = RSA.construct((n, e, d))
    publicKey = privateKey.publickey()

    cipher = PKCS1_OAEP.new(publicKey)

    start = time.clock()
    ciphertext = cipher.encrypt(data)
    end = time.clock()
    times.append(end - start)

    print("Encrypted:")
    print(ciphertext.hex())

    decipher = PKCS1_OAEP.new(privateKey)

    start = time.clock()
    plainText = decipher.decrypt(ciphertext)
    end = time.clock()
    times.append(end - start)

    print("Desencrypted:")
    print(plainText.hex())

    return times

with open("rsa_oaep_test_vectors.csv") as testVectors, open('times_RSA_OAEP.csv', 'w') as results:
    reader = csv.reader(testVectors, delimiter = ",")
    writer = csv.writer(results, quoting=csv.QUOTE_ALL)
    writer.writerow(['RSA OAEP encrypting', 'RSA OAEP desencryting'])
    for row in reader:
        n = int(row[0], 16)
        e = int(row[1], 16)
        d = int(row[2], 16)
        data =  bytes.fromhex(row[3])

        print('\nRSA OAEP')
        time_rsa_oaep = RSA_OAEP(data, n, e, d)

        writer.writerow(time_rsa_oaep)
