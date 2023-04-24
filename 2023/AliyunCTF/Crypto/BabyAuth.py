import json
from gmssl import sm2, sm3, sm4
#gmssl version 3.2.1
from gmssl.func import bytes_to_list as b2l, list_to_bytes as l2b, padding as pad, unpadding as unpad
from hashlib import sha256
from os import urandom
from random import seed, choice
from secret import flag as FLAG
from string import ascii_letters, ascii_lowercase, digits
from sys import stdin

MENU = '''
1. Register
2. Login
3. Exit
'''

def proof_of_work():
    seed(urandom(8))
    proof = ''.join([choice(ascii_letters + digits) for _ in range(20)])
    digest = sha256(proof.encode('latin-1')).hexdigest()
    print('sha256(XXXX + {}) == {}'.format(proof[4: ], digest))
    print('Give me XXXX:')
    x = stdin.read(5).strip()
    if x != proof[: 4]: 
        return False
    return True

def check_name(s):
    return len(s) > 80 or not all([i in ascii_lowercase + digits for i in s]) or session_admin in s

def Register(name):
    msg = json.dumps({"rwx": False, "id": name}).encode()
    sig = SM2.sign(msg, urandom(32).hex()).encode()
    dig = sm3.sm3_hash(b2l(msg)).encode()
    pt = l2b(pad(b2l(msg)) + pad(b2l(sig)) + pad(b2l(dig)))
    iv = urandom(16)
    SM4.set_key(SM4_sk, sm4.SM4_ENCRYPT)
    ct = iv + SM4.crypt_cbc(iv, pt)
    return ct.hex()

def Login(token):
    try:
        token = bytes.fromhex(token)
        iv, ct = token[: 16], token[16: ]
        SM4.set_key(SM4_sk, sm4.SM4_DECRYPT)
        pt = SM4.crypt_cbc(iv, ct)
        items = []
        for _ in range(1, 4):
            pt = unpad(pt)
            pt, item = pt[: -64 * _], pt[-64 * _: ]
            items.append(item)
        if items[0] == sm3.sm3_hash(b2l(items[-1])).encode():
            if SM2.verify(items[1], items[-1]):
                msg = json.loads(items[-1])
                if msg['rwx'] == True and msg['id'] == session_admin:
                    return FLAG
                else:
                    return 'Login successed!'
        else:
                return 'Verification failed.'
    except:
        return 'Verification failed.'

if not proof_of_work():
    exit(0)

SM4_sk = urandom(16)
SM4 = sm4.CryptSM4()

SM2_sk = urandom(32).hex()
SM2_pk = None
SM2 = sm2.CryptSM2(SM2_sk, SM2_pk)
SM2.public_key = SM2._kg(int(SM2_sk, 16), sm2.default_ecc_table['g'])

session_id = urandom(32).hex()
session_admin = 'admin' + session_id

print('Session ID: {}'.format(session_id))
print(MENU)
for _ in range(500):
    op = int(input('> '))
    if op == 1:
        name = input('Name: ')
        if check_name(name):
            print('Your name is invalid.')
            break
        token = Register(name)
        print('Your token: {}'.format(token))
    elif op == 2:
        token = input('Token: ')
        response = Login(token)
        print('Response: {}'.format(response))
    elif op == 3:
        print('Byte!')
        break
    else:
        print('No such option!')
