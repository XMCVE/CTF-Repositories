from gmpy2 import next_prime
from Crypto.Util.number import getPrime, isPrime, bytes_to_long
import random
from secret import flag

def init():
    primes = []
    p = 1
    while len(primes) < 100:
        p = next_prime(p)
        primes.append(int(p))
    return primes

def genMyPrimeA(bits):
    while True:
        g = 2
        while g < 2 ** bits:
            g *= random.choice(primes)
        g += 1
        if isPrime(g):
            return g

def genMyPrimeB(bits):
    while True:
        g = 2
        while g < 2 ** bits:
            g *= random.choice(primes)
        g -= 1
        if isPrime(g):
            return g

def gen(st, n, a, b, c, d):
    A = [st + 2023, st + 2024, st + 2025]
    for i in range(6**666):
        A.append((a * A[-3] + b * A[-2] + c * A[-1] + d) % n)
    return A

primes = init()
p1 = getPrime(256)
print(p1)
q1 = 1
while p1 > q1:
    q1 = genMyPrimeA(256)
print(q1)
p2 = getPrime(256)
q2 = 1
while p2 > q2:
    q2 = genMyPrimeB(256)
n1 = p1 * q1
n2 = p2 * q2
print(f'n1 = {n1}')
print(f'n2 = {n2}')

r = getPrime(512)
print(f'r = {r}')

A = gen(bytes_to_long(flag), r, p1, q1, p2, q2)
print(f'A[-3] = {A[-3]}')
print(f'A[-2] = {A[-2]}')
print(f'A[-1] = {A[-1]}')


# n1 = 39755206609675677517559022219519767646524455449142889144073217274247893104711318356648198334858966762944109142752432641040037415587397244438634301062818169
# n2 = 30725253491966558227957591684441310073288683324213439179377278006583428660031769862224980605664642101191616868994066039054762100886678504154619135365646221
# r = 7948275435515074902473978567170931671982245044864706132834233483354166398627204583162848756424199888842910697874390403881343013872330344844971750121043493
# A[-3] = 6085327340671394838391386566774092636784105046872311226269065664501131836034666722102264842236327898770287752026397099940098916322051606027565395747098434
# A[-2] = 1385551782355619987198268805270109182589006873371541520953112424858566073422289235930944613836387546298080386848159955053303343649615385527645536504580787
# A[-1] = 2529291156468264643335767070801583140819639532551726975314270127875306069067016825677707064451364791677536138503947465612206191051563106705150921639560469