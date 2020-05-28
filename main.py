import math
import sys
import random
import numpy
import string

LOG = 1

def main():
    m = sys.argv[2]
    message = numpy.fromstring(m, dtype=numpy.uint8)
    logTrace("ASCII msg", message, LOG)

    p = int(sys.argv[1])
    if not isPrime(p):
        print(p, "p is not a prime")
        return False

    logTrace("p", p, LOG)

    q = int((p - 1)/2)
    if not isPrime(q):
        print(q, "q is not a prime")
        return False
    logTrace("q", q, LOG)

    G = subgroup(q, p)
    logTrace("subgroup", G, LOG)

    Zq = group(q)
    logTrace("Zq", Zq, LOG)

    keys = keysGenerator(G,Zq,p)
    logTrace("Public and Private keys", keys, LOG)

    enc = encrypt(message, keys, G, Zq, p)
    print("Encrypted message", enc)

    dec = decrypt(enc,p,G,keys)
    print("Decrypted message", dec)

def decrypt(enc,mod,G,keys):
    message = []
    for j in range(0, len(enc)):

        u1 = enc[j][0]
        u2 = enc[j][1]
        e = enc[j][2]
        v = enc[j][3]
        z = keys[1][8]

        v2 = powMod(u1,((keys[1][0]+u1*keys[1][2])+(u2*keys[1][4])+(e*keys[1][6])),mod)
        v2 = v2*powMod(u2,((keys[1][1]+u1*keys[1][3])+(u2*keys[1][5])+(e*keys[1][7])),mod)
        v2 = v2%mod

        if v == v2:
            for i in range(0, mod):
                if powMod(u1,z,mod)*i%mod == 1:
                    inv = i
            message.append((chr(G.index(e*inv%mod))))
        else:
            return 'rejected'

    return string.join(message)


def encrypt(message, keys, G, Zq, p):
    encrypt = []
    for i in range(0, len(message)):
        logTrace("message[i]", message[i], LOG)
        m = G[(message[i])]
        logTrace("m", m, LOG)
        cipher = cipherText(Zq, p, keys, m)
        logTrace("CipherText", cipher, LOG)
        encrypt.append(cipher)

    return encrypt

def cipherText(Zq, p, keys, m):
    r = random.choice(Zq)
    logTrace("Random r", r, LOG)

    g1 = keys[0][0]
    logTrace("g1", g1, LOG)

    u1 = powMod(g1,r,p)
    logTrace('u1',u1, LOG)

    g2 = keys[0][1]
    logTrace('g2',g2, LOG)

    u2 = powMod(g2,r,p)
    logTrace('u2',u2, LOG)

    h = keys[0][4]
    logTrace('h',h, LOG)

    e = (powMod(h,r,p)*m)%p
    logTrace('e', e, LOG)

    c = keys[0][2]
    logTrace('c',c, LOG)

    d1 = keys[0][3][0]
    d2 = keys[0][3][1]
    d3 = keys[0][3][2]
    logTrace('d1',d1, LOG)
    logTrace('d2',d2, LOG)
    logTrace('d3',d3, LOG)

    y1a = keys[1][2]
    logTrace('y1',y1a, LOG)
    y2a = keys[1][3]
    logTrace('y2',y2a, LOG)

    y1b = keys[1][4]
    logTrace('y1b',y1b, LOG)
    y2b = keys[1][5]
    logTrace('y2b',y2b, LOG)

    y1c = keys[1][6]
    logTrace('y1c',y1c, LOG)
    y2c = keys[1][7]
    logTrace('y2c',y2c, LOG)

    v = vGenerator(u1,u2,e,p, r, c, d1, d2, d3)

    return [u1,u2,e,v]

def keysGenerator(G,Zq,mod):
    g1 = random.choice(G)
    g2 = random.choice(G)

    logTrace('G random choice g1',g1, LOG)
    logTrace('G random choice g2',g2, LOG)

    x1 = random.choice(Zq)
    x2 = random.choice(Zq)
    y1a = random.choice(Zq)
    y1b = random.choice(Zq)
    y1c = random.choice(Zq)

    y2a = random.choice(Zq)
    y2b = random.choice(Zq)
    y2c = random.choice(Zq)
    z = random.choice(Zq)

    logTrace('Zq random choice x1,x2,y1a,y2a,y1b,y2b,y1c,y2c,z ',[x1,x2,y1a,y2a,y1b,y2b,y1c,y2c,z], LOG)

    c = ((powMod(g1,x1,mod) * powMod(g2,x2,mod))%mod)
    logTrace('c',c, LOG)


    d1 = ((powMod(g1,y1a,mod) * powMod(g2,y2a,mod))%mod)
    d2 = ((powMod(g1,y1b,mod) * powMod(g2,y2b,mod))%mod)
    d3 = ((powMod(g1,y1c,mod) * powMod(g2,y2c,mod))%mod)
    d = [d1,d2,d3]

    logTrace('d',d, LOG)
    h = powMod(g1,z,mod)
    logTrace('h',h, LOG)

    publicKey = [g1,g2,c,d,h]
    privateKey = [x1,x2,y1a,y2a,y1b,y2b,y1c,y2c,z]

    return (publicKey, privateKey)

def vGenerator(u1, u2, e, mod, r, c, d1, d2, d3):
    v = powMod(c, r, mod)
    v = ((v * powMod(d1,(u1*r), mod))%mod)
    logTrace('v-u1',v, LOG)
    v = ((v * powMod(d2,(u2*r), mod))%mod)
    logTrace('v-u2',v, LOG)
    v = ((v * powMod(d3,(e*r), mod))%mod)
    logTrace('v-e',v, LOG)

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
            logTrace('generator',i, LOG)
            return i


def isPrime(n) :
    p = int(math.ceil(math.sqrt(n)))

    if (n % 2 == 0 or n % 3 == 0):
        return False

    for i in range(4, p):
        if(n % i == 0):
            return False

    return True

def logTrace(traceKey, traceValue, enable) :
    if (int(enable) == 1):
        print(traceKey+" =>=>=> ", traceValue)


#We choose a large prime p

main()