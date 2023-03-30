import random
import signal

def guess_number_1():
    randoms = []
    for _ in range(208):
        randoms.append(random.getrandbits(96))

    print("randoms = "+str(randoms))
    number = str(random.getrandbits(96))
    guess = str(input("Guess after number:"))
    if guess != number:
        print("Wrong Number! Guess again.")
        exit(0)

def guess_number_2():
    number = str(random.getrandbits(96))
    randoms = []
    for _ in range(627):
        randoms.append(random.getrandbits(32))

    print("randoms = "+str(randoms))
    guess = str(input("Guess pre number:"))
    if guess != number:
        print("Wrong Number! Guess again.")
        exit(0)

def guess_number_3():

    def _int32(x):
        return int(0xFFFFFFFF & x)  
    def init(seed):
        mt = [0] * 624
        mt[0] = seed
        for i in range(1, 624):
            mt[i] = _int32(1812433253 * (mt[i - 1] ^ mt[i - 1] >> 30) + i)
        return mt[-1]
    number = random.getrandbits(32)
    print("last number = "+ str(init(number)))
    guess = int(str(input("Guess seed number:")))
    if guess != number:
        print("Wrong Number! Guess again.")
        exit(0)

def guess_number_4():
    def extract_number(y):
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        return y&0xffffffff

    number = random.getrandbits(32)
    print("extract number = "+ str(extract_number(number)))
    guess = int(str(input("Guess be extracted number:")))
    if guess != number:
        print("Wrong Number! Guess again.")
        exit(0)
    

print("Welcome to the Mersenne Twister basic challenge. Please try to solve 20 challenges in 60 seconds.")
signal.alarm(60)

for i in range(20):
    print("Round: "+str(i+1))
    random.choice([guess_number_1,guess_number_2,guess_number_3,guess_number_4])()
    print("Good job!")

flag = open('/flag').read()
print("Congratulations on passing the challenge. This is your flag: " + str(flag))

