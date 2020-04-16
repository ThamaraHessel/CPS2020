import math
import sys

def main(p):
    if not isPrime(p):
        print(p, "p is not a prime")
        return False
    #such that p- 1 = 2q, where q is also prime.
    q = int((p - 1)/2)

    if not isPrime(q):
        print(q, "q is not a prime")
        return False

    #The group G is the subgroup of order q in Zp*
    G = subgroup(q, p)
    print("subgroup:", G)

    #We restrict a message to be an element of the set (1,..., q) = (1, 2, 3, 4, 5),
    #and "encode" it by squaring it modulo p(11), giving us an element in G(1, 2, 3, 4, 5)
    message = 3

    # calculate square
    square = int(math.pow(message, 2))

    encode = square % p
    print(encode)

def subgroup(sub, modulo):
    subgroup = []
    for i in range(2, modulo):
        g = int((i**sub)%modulo)
        if g == 1:
            print("generator:", i)
            for z in range(0, sub):
                s = int((i**z)%modulo)
                subgroup.append(s)
            break
    subgroup.sort()
    return subgroup

def isPrime(n) :
    p = int(math.ceil(math.sqrt(n)))
    for i in range(2, p):
        if(n % i == 0):
            return False

    return True

#We choose a large prime p
prime = long(sys.argv[1])
main(prime)