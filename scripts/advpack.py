import struct
import json
from itertools import accumulate
from dizzy import dizzy, undizzy, dizzy_squeeze


def compact_word(word: str, lo: int, hi: int):
    """
    byte 0: code % 1000 (<=147)
    byte 1: code // 1000 (<=3)
    byte 2: strlen (<=15), points to next entry, 0/0/0 header for last
    n byte str
    """
    assert lo < 256 and hi < 4
    return struct.pack("<BBB", lo, hi, len(word)) + word.encode('ascii')


def compact_cave(long: bytes, short: bytes, travel: list[int]):
    """
    compact representation for cave data

    byte 0: offset to long (or 0 if none)
    byte 1: # travel
    byte 2: 4 x # travel uint32
    @short: strz
    [@long: strz]
    """
    if long == short:
        offset = 0
    else:
        offset = 2 + 4 * len(travel) + len(short) + 1
        assert offset < 256

    data = struct.pack(f"<BB{len(travel)}I", offset, len(travel), *travel)
    data += short
    if offset:
        data += long
    return data


# fetch the extracted data
advent = json.load(open('data/advent.json'))

caves = advent['caves']
corpus = (
    [c['long'] for c in caves]
    + [c['short'] for c in caves if c['short'] != c['long']]
    + advent['messages']
    + sum(advent['items'], [])
)
print('corpus has', len(corpus), 'strings', len(''.join(corpus)), 'characters')

# make a digram lookup table
source = b'\0'.join(line.encode('ascii') for line in corpus)+b'\0'
data, digrams = dizzy(source)

print(f"dizzy compress {len(source)} source bytes to {len(data)} compressed bytes "
    f"with {len(digrams)} digrams. uncompress ok? {undizzy(data, digrams) == source}")

def sqz(s):
    return dizzy_squeeze(s.encode('ascii'), digrams) + bytes([0])

"""
print(', '.join(f'${x:02x},${y:02x}' for x,y in d.values()))
print(', '.join(f'${x:02x}' for x in z.split(b'\0')[0]))
print(src.split(b'\0')[0].decode('ascii'))
"""

n = 0
# words
data = b''.join(
    compact_word(*w) for w in advent['words']
) + bytes(3)
print(f"compact words {len(data)} bytes")
n += len(data)

# caves
data = b''.join(
    compact_cave(sqz(c['long']), sqz(c['short']), c['travel']) for c in advent['caves']
)
print(f"compact cave data {len(data)} bytes plus {len(advent['caves'])*2} byte index")
n += len(data)

# messages
zs = [sqz(msg) for msg in advent['messages']]
offsets = list(accumulate((len(z) for z in zs), initial=0))[:-1]
assert len(offsets) == len(zs)
data = b''.join(zs)
print(f"compact message data {len(data)} byte plus {len(offsets)*2} byte index")
n += len(data)

# items
zs = [b''.join(sqz(s) for s in states) for states in advent['items']]
offsets = list(accumulate((len(z) for z in zs), initial=0))[:-1]
assert len(offsets) == len(zs)
data = b''.join(zs)
print(f"compact item data {len(data)} byte plus {len(offsets)*2} byte index")
n += len(data)

print(f"total {n} bytes")
