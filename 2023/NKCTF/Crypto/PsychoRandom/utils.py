class ToyGen:
    def __init__(self, state):
        self.nbits = 128
        self.state = state & ((1 << self.nbits) - 1)

        self.mask = 230336355081348639216651218083300669636

        self.alpha = 237299571639771708626086074576623691999
        self.beta = 83015690654496181240783151904447565127

    def func0(self, steps=1):
        for _ in range(steps):
            res = self.state & self.mask
            bit = sum([(res >> i) & 1 for i in range(self.nbits)]) & 1
            self.state = ((self.state << 1) ^ bit) & ((1 << self.nbits) - 1)
        return

    def func1(self):
        res = (self.state ^ self.beta) & self.alpha
        bit = sum([(res >> i) & 1 for i in range(self.nbits)]) & 1
        return bit

    def __next__(self):
        out = 0
        for _ in range(8):
            self.func0(37)
            bit = self.func1()
            out = (out << 1) ^ bit
        return out

