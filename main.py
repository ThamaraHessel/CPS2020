import math
import sys
import random
import numpy

def main():
    p = int(sys.argv[1])
    m = sys.argv[2]
    message = numpy.fromstring(m, dtype=numpy.uint8)

    if not isPrime(p):
        print(p, "p is not a prime")
        return False
    q = int((p - 1)/2)

    if not isPrime(q):
        print(q, "q is not a prime")
        return False

    print("p:", p)
    print("q:", q)
    G = subgroup(q, p)
    Zq = group(q)
    print("Zq:", Zq)
    print("subgroup:", G)

    print('ASCII msg:', m)

    keys = keysGenerator(G,Zq,p)
    print('Public and Private keys:',keys)

    enc = encrypt(message, keys, G, Zq, p)
    print('Encrypted message:', enc)

def encrypt(message, keys, G, Zq, p):
    encrypt = []
    for i in range(0, len(message)):
        m = G[message[i]]
        cipher = cipherText(Zq, p, keys, m)
        print('CipherText:',cipher)
        encrypt.append(cipher)

    return encrypt

def cipherText(Zq, p, keys, m):
    r = random.choice(Zq)
    print('Random r',r)

    g1 = keys[0][0]
    print('g1',g1)

    u1 = powMod(g1,r,p)
    print('u1',u1)

    g2 = keys[0][1]
    print('g2',g2)

    u2 = powMod(g2,r,p)
    print('u2',u2)

    h = keys[0][4]
    print('h',h)


    e = (powMod(h,r,p)*m)%p
    print('e',e)


    print('e', e)

    c = keys[0][2]
    print('c',c)

    y1 = keys[1][2]
    print('y1',y1)

    y2 = keys[1][3]
    print('y2',y2)

    v = vGenerator(r, c, p, m, y1, y2, g1, g2)

    return [u1,u2,e,v]

def keysGenerator(G,Zq,mod):
    g1 = random.choice(G)
    g2 = random.choice(G)

    print('G random choice:',g1,g2)

    x1 = random.choice(Zq)
    x2 = random.choice(Zq)
    y1 = random.choice(Zq)
    y2 = random.choice(Zq)
    z = random.choice(Zq)

    print('Zq random choice:',x1,x2,y1,y2,z)

    c = (powMod(g1,x1,mod) * powMod(g2,x2,mod))
    print('c:',c)
    d = (powMod(g1,y1,mod) * powMod(g2,y2,mod))
    print('d:',d)
    h = powMod(g1,z,mod)
    print('h:',h)

    publicKey = [g1,g2,c,d,h]
    privateKey = [x1,x2,y1,y2,z]

    return (publicKey, privateKey)

def vGenerator(r, c, mod, m, y1, y2, g1, g2):
    v = powMod(c, r, mod)
    d = ((powMod(g1,y1,mod) * powMod(g2,y2,mod))%mod)
    print('d',d)
    a = (m*r)%mod
    print('a',a)
    v = ((v * powMod(d,a, mod))%mod)
    print('v:',v)

    return v

def group(p):
    group = []
    for i in range(0, p):
        group.append(i)

    group.sort()
    return group


def subgroup(pow, mod):
    subgroup = []
    gtr = generator(pow, mod)
    for q in range(0, pow):
        s = powMod(gtr,q,mod)
        subgroup.append(s)

    subgroup.sort()
    return subgroup

def powMod(i,pow,mod):
     return int((i**pow)%mod)

def generator(pow, mod):
    for i in range(2, mod):
        g = powMod(i,pow,mod)
        if g == 1:
            print("generator:", i)
            return i


def isPrime(n) :
    p = int(math.ceil(math.sqrt(n)))

    if (n % 2 == 0 or n % 3 == 0):
        return False

    for i in range(4, p):
        if(n % i == 0):
            return False

    return True

#We choose a large prime p

main()