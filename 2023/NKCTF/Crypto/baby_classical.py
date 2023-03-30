import string
import re
import numpy as np
flag = ''
print('flag length:',len(flag))
dic = string.ascii_uppercase+string.ascii_lowercase+string.digits+'+/'
f1nd = lambda x : dic.find(x)
class KeyEncryption:
    def __init__(self, m: int, fillchar: str="z", key: np.ndarray=None):
        self.m = m
        self.key = key
        self.dicn2s = {i: dic[i] for i in range(64)}
        self.dics2n = dict(zip(self.dicn2s.values(), self.dicn2s.keys()))
        self.fillchar = self.dics2n[fillchar]
    def setM(self, m: int) -> None:
        assert m > 0
        self.m = m
    def setKey(self, key: np.ndarray=None) -> None:
        if key is None:
            while key is None or KeyEncryption.modInv(np.linalg.det(key)) == -1:
                key = np.random.randint(0, 65, size=(self.m, self.m))
            print("random matrix：\n", key)
        else:
            assert KeyEncryption.modInv(np.linalg.det(key)) != -1
        self.key = key
    @staticmethod
    def modInv(x: int):
        y = 0
        while y < 64:
            y += 1
            if (x * y) % 64 == 1:
                return y
        return -1
    def _loopCrypt(self, long: np.ndarray, K: np.ndarray) -> np.ndarray:
        ans = np.array([])
        for i in range(long.shape[0] // self.m):
            ans = np.mod(np.hstack((
                ans, 
                np.dot(long[i*self.m:i*self.m+self.m], K)
            )), 64)
        return ans.astype(np.int64)
    def encrypt(self, plaintext: np.ndarray):
        assert self.m !=None and self.key is not None
        if plaintext.shape[0] % self.m:
            plaintext = np.hstack((
                plaintext, 
                [self.fillchar] *(self.m - plaintext.shape[0] % self.m)
            ))
        return self._loopCrypt(plaintext, self.key)
    def translate(self, s, to: str):
        if to == "text":
            return "".join([self.dicn2s[si] for si in s])
        elif to == "num":
            s = s.replace(" ", "")
            return np.array([self.dics2n[si] for si in s])
def getKey(key):
  he = KeyEncryption(m=3)
  he.setKey()              
  nums = he.translate(key, "num")
  res = he.encrypt(nums)
  enkey = ''.join(dic[i] for i in res.tolist())
  print('Encrypt key:',enkey)
  return enkey
if __name__ == '__main__':
  fir1 = ' '.join(map(lambda _:_[::-1],re.split("[ { _ } ]" , flag.swapcase())))
  ciphertext1 = ''
  key = ""  
  enkey = getKey(key)
  _enkey=[f1nd(i) for i in key]
  print('key lengeh:',len(_enkey))
  j = 0
  for i in fir1:
    if f1nd(i)>=0:
      ciphertext1 += dic[(f1nd(i) + _enkey[j % len(_enkey)])%64]
    else:
      ciphertext1 += i
    j += 1
  ciphertext = ciphertext1.replace(' ','_')
  print('ciphertext:%s{%s}' % (ciphertext[0:5],ciphertext[6:-1]))

'''
flag length: 48
random matrix：
 [[13 37 10]
 [15 17 41]
 [13  0 10]]
Encrypt key: pVvRe/G08rLhfwa
key lengeh: 14
ciphertext:1k2Pe{24seBl4_a6Ot_fp7O1_eHk_Plg3EF_g/JtIonut4/}
'''