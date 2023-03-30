from Crypto.Util.strxor import strxor as xor
import os
from secret import flag


def round(s, k):
    l, r = s[:16], s[16:]
    l_, r_ = xor(xor(r, k), l), l
    return l_ + r_


def encode(s, k):
    t = s
    for i in range(8):
        t = round(t, k[i])
    return t


r = os.urandom(32)
print(r)

key = [os.urandom(16) for _ in range(8)]

print(encode(r, key))
m = flag.strip(b'NKCTF{').strip(b'}').replace(b'-', b'')
print(encode(m, key))

# b"t\xf7\xaa\xac\x9d\x88\xa4\x8b\x1f+pA\x84\xacHg'\x07{\xcc\x06\xc4i\xdd)\xda\xc9\xad\xa9\xe8\x1fi"
# b"'{<z}\x91\xda\xc5\xd5S\x8b\xfa\x9f~]J\x0f\xf4\x9a\x1e\xe0\xef\x129N\xe7a\x928+\xe0\xee"
# b'8\x1f"\x83B4\x86)\xce\xebq3\x06\xa0w\x16U\x04M/w\xa1\x8f;)M\xdd~\x11:\xe3\xb3'
