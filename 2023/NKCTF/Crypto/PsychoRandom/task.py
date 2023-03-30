#!/usr/bin/env python
# Problem by rec, with a toy generator.
import os, utils

seed = int(os.urandom(16).hex(), 16)
gen = utils.ToyGen(seed)

sec = b'#####'
assert b'nkctf' in sec

msg = b'##MSG FROM NK: ' + sec
enc = bytes(m ^ next(gen) for m in msg).hex()
print(enc)
# 9c1250e1fefb6012cf74a7fd0156cd1a2817ee9381d086a1561399f5b7f519e5abf4437739fa254cd35b241375292d73aa8b8e6ff61f4977da3c68a699156e6bfbe2c38d7b08eed07e40e831c25f5327a21847bb156060228e2b
