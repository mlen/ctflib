from ctflib.util import xor


class block_decryptor(object):
    def __init__(self, data, oracle, blocksize=16):
        assert len(data) == blocksize

        self.data = data
        self.oracle = oracle
        self.blocksize = blocksize

    def _decrypt_byte(self, known, pos):
        for value in range(256):
            pivot = self.blocksize - pos
            block = bytes(pivot) + bytes([value]) + xor(known[pivot + 1:], [pos] * (pos - 1))

            if self.oracle(block + self.data) and self._verify_block(block, pos):
                return xor(bytes(pivot) + bytes([pos] * pos), block)

        raise RuntimeError('Failed to decrypt byte {}'.format(pos))

    def _verify_block(self, block, pos):
        if pos == self.blocksize:
            return True
        else:
            pivot = self.blocksize - pos - 1
            verifier = block[:pivot] + bytes([block[pivot] ^ 1]) + block[pivot + 1:]
            return self.oracle(verifier + self.data)

    def decrypt(self):
        known = bytes(self.blocksize)
        for x in range(self.blocksize):
            known = self._decrypt_byte(known, x + 1)

        return known


class padder(object):
    def __init__(self, blocksize=16):
        self.blocksize = blocksize
        self.size = 0

    def update(self, data):
        self.size += len(data)
        return data

    def final(self):
        pad = self.blocksize - self.size % self.blocksize
        return bytes([pad] * pad)


class plaintext_forger(object):
    def __init__(self, target, oracle, blocksize=16):
        self.oracle = oracle
        self.blocksize = blocksize

        p = padder(self.blocksize)
        self.target = p.update(target) + p.final()
        assert len(self.target) % self.blocksize == 0

    def forge(self):
        known = bytes(self.blocksize)

        while self.target:
            x = len(self.target) - self.blocksize
            self.target, block = self.target[:x], self.target[x:]
            plain = block_decryptor(known[:self.blocksize], self.oracle, self.blocksize).decrypt()
            known = xor(plain, block) + known

        return known
