import struct


def xor(x, y):
    assert len(x) == len(y)
    return bytes(a ^ b for a, b in zip(x, y))


def groups_of(data, cnt):
    return [data[i:i+cnt] for i in range(0, len(data), cnt)]


def p32(val):
    return struct.pack('<I', val)


def p64(val):
    return struct.pack('<Q', val)


def u32(val):
    return struct.unpack('<I', val)[0]


def u64(val):
    return struct.unpack('<Q', val)[0]
