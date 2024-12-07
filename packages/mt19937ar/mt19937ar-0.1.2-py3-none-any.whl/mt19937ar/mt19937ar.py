class MT19937ar:
    def __init__(self) -> None:
        self.N = 624
        self.M = 397
        self.MATRIX_A = 0x9908B0DF
        self.UPPER_MASK = 0x80000000
        self.LOWER_MASK = 0x7FFFFFFF
        self.mt = [0] * self.N
        self.mti = self.N + 1

    def init_genrand(self, s: int) -> None:
        self.mt[0] = s & 0xFFFFFFFF
        for mti in range(1, self.N):
            self.mt[mti] = 1812433253 * (self.mt[mti - 1] ^ (self.mt[mti - 1] >> 30)) + mti
            self.mt[mti] &= 0xFFFFFFFF
        self.mti = self.N

    def init_by_array(self, init_key: list[int]) -> None:
        self.init_genrand(19650218)
        i = 1
        j = 0
        k = max(624, len(init_key))
        for _ in range(k):
            self.mt[i] = (self.mt[i] ^ ((self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) * 1664525)) + init_key[j] + j
            self.mt[i] &= 0xFFFFFFFF
            i += 1
            j += 1
            if i >= self.N:
                self.mt[0] = self.mt[self.N - 1]
                i = 1
            if j >= len(init_key):
                j = 0
        for _ in range(self.N - 1):
            self.mt[i] = (self.mt[i] ^ ((self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) * 1566083941)) - i
            self.mt[i] &= 0xFFFFFFFF
            i += 1
            if i >= self.N:
                self.mt[0] = self.mt[self.N - 1]
                i = 1

        self.mt[0] = 0x80000000

    def genrand_int32(self) -> int:
        mag01 = [0x0, self.MATRIX_A]

        if self.mti >= self.N:
            if self.mti == self.N + 1:
                self.init_genrand(5489)

            for kk in range(self.N - self.M):
                y = (self.mt[kk] & self.UPPER_MASK) | (self.mt[kk + 1] & self.LOWER_MASK)
                self.mt[kk] = self.mt[kk + self.M] ^ (y >> 1) ^ mag01[y & 1]
            for kk in range(self.N - self.M, self.N - 1):
                y = (self.mt[kk] & self.UPPER_MASK) | (self.mt[kk + 1] & self.LOWER_MASK)
                self.mt[kk] = self.mt[kk + (self.M - self.N)] ^ (y >> 1) ^ mag01[y & 1]
            y = (self.mt[self.N - 1] & self.UPPER_MASK) | (self.mt[0] & self.LOWER_MASK)
            self.mt[self.N - 1] = self.mt[self.M - 1] ^ (y >> 1) ^ mag01[y & 1]

            self.mti = 0

        y = self.mt[self.mti]
        self.mti += 1

        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18

        return y

    def genrand_int31(self) -> int:
        return self.genrand_int32() >> 1

    def genrand_real1(self) -> float:
        return self.genrand_int32() * (1.0 / 4294967295.0)

    def genrand_real2(self) -> float:
        return self.genrand_int32() * (1.0 / 4294967296.0)

    def genrand_real3(self) -> float:
        return (self.genrand_int32() + 0.5) * (1.0 / 4294967296.0)

    def genrand_res53(self) -> float:
        a = self.genrand_int32() >> 5
        b = self.genrand_int32() >> 6
        return (a * 67108864.0 + b) * (1.0 / 9007199254740992.0)
