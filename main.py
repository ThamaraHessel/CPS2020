import math
import sys
import random
import numpy

ENABLED_TRACE = 0
DECODE = "cp1252"

def main():
    m = sys.argv[2]
    message = numpy.frombuffer(m.encode(), dtype=numpy.uint8)
    showTrace("ASCII msg", message, ENABLED_TRACE)

    p = int(sys.argv[1])
    if not isPrime(p):
        print(p, "p is not a prime")
        return False

    showTrace("p", p, ENABLED_TRACE)

    q = int((p - 1)/2)
    if not isPrime(q):
        print(q, "q is not a prime")
        return False
    showTrace("q", q, ENABLED_TRACE)

    G = subgroup(q, p)

    if len(G) < 255:
        print(len(G), "The subgroup must contain at least 255 to support ASCII")
        return False

    showTrace("subgroup", G, ENABLED_TRACE)

    Zq = group(q)
    showTrace("Zq", Zq, ENABLED_TRACE)

    keys = keysGenerator(G,Zq,p)
    showTrace("Public and Private keys", keys, ENABLED_TRACE)

    enc = encrypt(message, keys, G, Zq, p)
    sys.stdout.write('\n\n')
    print("Encrypted message: ", enc)

    dec = decrypt(enc,p,G,keys)
    sys.stdout.write('\n\n')
    sys.stdout.buffer.write("Decrypted message: ".encode())
    sys.stdout.buffer.write(dec.encode(DECODE))
    sys.stdout.write('\n\n')

def decrypt(enc,mod,G,keys):
    message = ''
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
            message=message+(chr(G.index(e*inv%mod)))
        else:
            return 'rejected'
    return message

def encrypt(message, keys, G, Zq, p):
    encrypt = []
    for i in range(0, len(message)):
        showTrace("message", message[i], ENABLED_TRACE)
        m = G[(message[i])]
        showTrace("m", m, ENABLED_TRACE)
        cipher = cipherText(Zq, p, keys, m)
        showTrace("CipherText", cipher, ENABLED_TRACE)
        encrypt.append(cipher)

    return encrypt

def cipherText(Zq, p, keys, m):
    r = random.choice(Zq)
    showTrace("Random r", r, ENABLED_TRACE)

    g1 = keys[0][0]
    showTrace("g1", g1, ENABLED_TRACE)

    u1 = powMod(g1,r,p)
    showTrace('u1',u1, ENABLED_TRACE)

    g2 = keys[0][1]
    showTrace('g2',g2, ENABLED_TRACE)

    u2 = powMod(g2,r,p)
    showTrace('u2',u2, ENABLED_TRACE)

    h = keys[0][4]
    showTrace('h',h, ENABLED_TRACE)

    e = (powMod(h,r,p)*m)%p
    showTrace('e', e, ENABLED_TRACE)

    c = keys[0][2]
    showTrace('c',c, ENABLED_TRACE)

    d1 = keys[0][3][0]
    d2 = keys[0][3][1]
    d3 = keys[0][3][2]
    showTrace('d1',d1, ENABLED_TRACE)
    showTrace('d2',d2, ENABLED_TRACE)
    showTrace('d3',d3, ENABLED_TRACE)

    y1a = keys[1][2]
    showTrace('y1',y1a, ENABLED_TRACE)
    y2a = keys[1][3]
    showTrace('y2',y2a, ENABLED_TRACE)

    y1b = keys[1][4]
    showTrace('y1b',y1b, ENABLED_TRACE)
    y2b = keys[1][5]
    showTrace('y2b',y2b, ENABLED_TRACE)

    y1c = keys[1][6]
    showTrace('y1c',y1c, ENABLED_TRACE)
    y2c = keys[1][7]
    showTrace('y2c',y2c, ENABLED_TRACE)

    v = vGenerator(u1,u2,e,p, r, c, d1, d2, d3)

    return [u1,u2,e,v]

def keysGenerator(G,Zq,mod):
    g1 = random.choice(G)
    g2 = random.choice(G)

    showTrace('G random choice g1',g1, ENABLED_TRACE)
    showTrace('G random choice g2',g2, ENABLED_TRACE)

    x1 = random.choice(Zq)
    x2 = random.choice(Zq)
    y1a = random.choice(Zq)
    y1b = random.choice(Zq)
    y1c = random.choice(Zq)

    y2a = random.choice(Zq)
    y2b = random.choice(Zq)
    y2c = random.choice(Zq)
    z = random.choice(Zq)

    showTrace('Zq random choice x1,x2,y1a,y2a,y1b,y2b,y1c,y2c,z ',[x1,x2,y1a,y2a,y1b,y2b,y1c,y2c,z], ENABLED_TRACE)

    c = ((powMod(g1,x1,mod) * powMod(g2,x2,mod))%mod)
    showTrace('c',c, ENABLED_TRACE)

    d1 = ((powMod(g1,y1a,mod) * powMod(g2,y2a,mod))%mod)
    d2 = ((powMod(g1,y1b,mod) * powMod(g2,y2b,mod))%mod)
    d3 = ((powMod(g1,y1c,mod) * powMod(g2,y2c,mod))%mod)
    d = [d1,d2,d3]

    showTrace('d',d, ENABLED_TRACE)
    h = powMod(g1,z,mod)
    showTrace('h',h, ENABLED_TRACE)

    publicKey = [g1,g2,c,d,h]
    privateKey = [x1,x2,y1a,y2a,y1b,y2b,y1c,y2c,z]

    return (publicKey, privateKey)

def vGenerator(u1, u2, e, mod, r, c, d1, d2, d3):
    v = powMod(c, r, mod)
    v = ((v * powMod(d1,(u1*r), mod))%mod)
    showTrace('v-u1',v, ENABLED_TRACE)
    v = ((v * powMod(d2,(u2*r), mod))%mod)
    showTrace('v-u2',v, ENABLED_TRACE)
    v = ((v * powMod(d3,(e*r), mod))%mod)
    showTrace('v-e',v, ENABLED_TRACE)

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

def powMod(i, pow, mod):
    r = 1
    i = i % mod

    if (i == 0) :
        return 0

    while (pow > 0) :
        if ((pow & 1) == 1) :
            r = (r * i) % mod
        pow = pow >> 1
        i = (i * i) % mod

    return r

def generator(pow, mod):
    for i in range(2, mod):
        g = powMod(i,pow,mod)
        if g == 1:
            showTrace('generator',i, ENABLED_TRACE)
            return i

def isPrime(n) :
    p = int(math.ceil(math.sqrt(n)))

    if (n % 2 == 0 or n % 3 == 0):
        return False

    for i in range(4, p):
        if(n % i == 0):
            return False

    return True

def showTrace(traceKey, traceValue, enable) :
    if (int(enable) == 1):
        print(traceKey+" : ", traceValue)

main()