from Crypto.Util.number import getPrime, bytes_to_long
from secret import BITS, hints, flag

p = getPrime(BITS)
q = getPrime(BITS)
n = p * q
print(f'n = {n}')

e = 0x10001
c = pow(bytes_to_long(flag), e, n)
print(f'c = {c}')

print('Give you some boring pows:')
for i in range(len(hints)):
    print(hints[i])
