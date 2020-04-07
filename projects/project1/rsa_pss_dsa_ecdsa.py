import time
import csv
from Crypto.Signature import pss
from Crypto.PublicKey import ECC, DSA, RSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA512, SHA256

def RSA_PSS(data, n, e, d):

    privateKeyRSA = RSA.construct((n, e, d))
    publicKeyRSA = privateKeyRSA.publickey()

    times = []
    hashValue = SHA256.new(data)

    signFunction = pss.new(privateKeyRSA)
    start = time.clock()
    signature = signFunction.sign(hashValue)
    end = time.clock()

    print(signature.hex())
    times.append(end - start)

    verifier = pss.new(publicKeyRSA)
    try:
        start = time.clock()
        verifier.verify(hashValue, signature)
        end = time.clock()
        print("The signature is authentic.")
    except (ValueError, TypeError):
        print("The signature is not authentic.")

    times.append(end - start)

    return times

def DSA_1024(data):
    times = []

    key = DSA.generate(1024)
    h = SHA512.new(data)

    controler = DSS.new(key, 'fips-186-3')

    start = time.clock()
    signature = controler.sign(h)
    end = time.clock()

    print(signature.hex())
    times.append(end - start)

    try:
        start = time.clock()
        controler.verify(h, signature)
        end = time.clock()
        print('The message is authentic')
    except ValueError:
        print('The message is not authentic')

    times.append(end - start)

    return times

def ECDSA_521(data):
    times = []

    key = ECC.generate(curve = 'P-521')
    h = SHA512.new(data)

    controler = DSS.new(key, 'fips-186-3')

    start = time.clock()
    signature = controler.sign(h)
    end = time.clock()

    print(signature.hex())
    times.append(end - start)

    try:
        start = time.clock()
        controler.verify(h, signature)
        end = time.clock()
        print('The message is authentic')
    except ValueError:
        print('The message is not authentic')

    times.append(end - start)

    return times

with open('rsa_pss_dsa_ecdsa_test_vectors.csv') as testVectors, open('times_RSA_PSS_DSA_ECDSA.csv', 'w') as results:
    reader = csv.reader(testVectors, delimiter = ",")
    writer = csv.writer(results, quoting=csv.QUOTE_ALL)
    writer.writerow(['DSA signing', 'DSA verifing','ECDSA signing', 'ECDSA verifing', 'RSA PSS signing', 'RSA PSS verifing'])

    for row in reader:
        n = int(row[1], 16)
        e = int(row[2], 16)
        d = int(row[3], 16)
        data =  bytes.fromhex(row[0])

        print('\nRSA PSS')
        time_rsa_pss = RSA_PSS(data, n, e, d)

        print('\nDSA')
        time_dsa = DSA_1024(data)

        print('\nECDSA')
        time_ecdsa = ECDSA_521(data)

        writer.writerow(time_dsa + time_ecdsa + time_rsa_pss)
