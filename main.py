import math
import sys
import random

def main():
    p = int(sys.argv[1])
    if not isPrime(p):
        print(p, "p is not a prime")
        return False
    #such that p- 1 = 2q, where q is also prime.
    q = int((p - 1)/2)

    if not isPrime(q):
        print(q, "q is not a prime")
        return False

    #The group G is the subgroup of order q in Zp*
    Zq = group(p)
    G = subgroup(q, p)

    print("group:", Zq)
    print("subgroup:", G)

    g1 = random.choice(G)
    g2 = random.choice(G)
    x1 = random.choice(Zq)
    x2 = random.choice(Zq)
    y1 = random.choice(Zq)
    y2 = random.choice(Zq)
    z = random.choice(Zq)

    print('Zp random choice:',x1,x2,y1,y2,z)
    print('G random choice:',g1,g2)

    c = ((powMod(g1,x1,p) * powMod(g2,x2,p))%p)
    print('c:',c)
    d = ((powMod(g1,y1,p) * powMod(g2,y2,p))%p)
    print('d:',d)
    h = powMod(g1,z,p)
    print('h:',h)

    message = 3

    square = int(math.pow(message, 2))

    encode = square % p
    print(encode)

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