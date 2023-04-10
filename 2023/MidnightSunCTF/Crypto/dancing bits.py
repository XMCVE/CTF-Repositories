import os
import zlib
from flask import Flask, request, jsonify
from secrets import token_bytes

app = Flask(__name__)

# The secret key and nonce for the DancingBits stream cipher
SECRET_KEY = int.from_bytes(token_bytes(4), 'big')
NONCE = int.from_bytes(token_bytes(4), 'big')

FLAG = ""

def lfsr(state):
    bit = ((state >> 31) ^ (state >> 21) ^ (state >> 1) ^ state) & 1
    return (state << 1) | bit

def rotl(x, k):
    return ((x << k) | (x >> (8 - k))) & 0xff

def swap(x):
    return ((x & 0x0f) << 4) | ((x & 0xf0) >> 4)

def dancingbits_encrypt(plaintext, key, nonce):
    state = (key << 32) | nonce
    ciphertext = bytearray()

    for byte in plaintext:
        state = lfsr(state)
        ks_byte = (state >> 24) & 0xff
        c = byte ^ ks_byte
        c = rotl(c, 3)
        c = swap(c)
        ciphertext.append(c)

    return ciphertext

def dancingbits_decrypt(ciphertext, key, nonce):
    state = (key << 32) | nonce
    plaintext = bytearray()

    for byte in ciphertext:
        state = lfsr(state)
        ks_byte = (state >> 24) & 0xff
        c = swap(byte)
        c = rotl(c, -3)
        p = c ^ ks_byte
        plaintext.append(p)

    return plaintext

@app.route('/encrypted_flag', methods=['GET'])
def encrypted_flag():
    compressed_flag = zlib.compress(FLAG.encode('utf-8'))
    encrypted_flag = dancingbits_encrypt(compressed_flag, SECRET_KEY, NONCE)
    return encrypted_flag

@app.route('/decrypt_oracle', methods=['POST'])
def decrypt_oracle():
    encrypted_data = request.data

    if len(encrypted_data) < 1:
        return jsonify(status=500, message="Error: Data too short")


    try:
        decrypted_data = dancingbits_decrypt(encrypted_data, SECRET_KEY, NONCE)
        decompressed_data = zlib.decompress(decrypted_data)

        for i in range(len(decompressed_data.decode('utf-8'))):
            if decompressed_data.decode('utf-8')[i] == FLAG[i]:
                return jsonify(status=500, message="Error: CTF character at index found: " + str(i))
        return jsonify(status=200, message="Success")
    except Exception as e:
        return jsonify(status=500, message="Error")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
