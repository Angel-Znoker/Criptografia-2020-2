import fileinput

def keyGeneration(a, b, A, B, E_D = 'E'):
    M = a * b - 1
    e = A * M + a
    d = B * M + b
    n = (e * d - 1) / M
    if E_D == 'E':
        return n, e
    elif E_D == 'D':
        return n, d

def encrypt(n, e, m):
    return (m * e) % n

def decrypt(n, d, m):
    return (m * d) % n

def main():
    lines = []

    for line in fileinput.input():
        lines.append(line.replace('\n',''))

    E_D = lines[0]
    a = int(lines[1])
    b = int(lines[2])
    A = int(lines[3])
    B = int(lines[4])
    m = int(lines[5])

    if E_D == 'E':
        n, e = keyGeneration(a, b, A, B)
        print(int(encrypt(n, e, m)))
    elif E_D == 'D':
        n, d = keyGeneration(a, b, A, B, 'D')
        print(int(decrypt(n, d, m)))

main()