"""
Implements a simple recursive digram coding scheme for ascii text.
See also https://en.wikipedia.org/wiki/Byte_pair_encoding
The most commonly used pair of characters (digram) is replaced by one of
the 128 unused hi-bit characters, and the digram is added to a lookup table
for that key.
This process is repeated recursively until we fill the lookup table
with 128 digrams or run out of common pairs to replace.
The recursion means that the hi-bit characters that replace digrams
in the string can themselves appear in subsequent commonly appearing pairs.
The 0 character (string terminator) is treated specially:
it's never replaced, and never appears in the digram lookup table.
This lets us find string terminators without decompressing.
"""

from collections import Counter


def dizzy(s: bytes) -> (bytes, dict[int, bytes]):
    """Compute a lookup table while compressing the source string"""
    assert all(x < 128 for x in s), "Input must be 7-bit bytes"

    k = 128
    digrams: dict(int, bytes) = {}
    while k < 256:
        pairs = [s[i:i+2] for i in range(0, len(s), 2)]
        pairs = [p for p in pairs if len(p) == 2 and 0 not in p]    # avoid zero
        pair, n = Counter(pairs).most_common(1)[0]
        if n < 3:       # nothing interesting to replace
            break
        digrams[k] = pair
        s = s.replace(pair, bytes([k]))
        k+=1
    return s, digrams


def dizzy_squeeze(s: bytes, digrams: dict[int, bytes]) -> bytes:
    """Encode a string using an existing lookup table"""
    while True:
        n = len(s)
        for (k, pair) in digrams.items():
            s = s.replace(pair, bytes([k]))
        if len(s) == n:
            break
    return s


def undizzy(s: bytes, digrams: dict[int, bytes]) -> bytes:
    """Decode a string using on a lookup table"""
    while True:
        k = next((x for x in s if x & 0x80), 0)
        if not k:
            break
        s = s.replace(bytes([k]), digrams[k])
    return s


def undizzy_stack(s: bytes, digrams: dict[int, bytes]) -> bytes:
    """
    Alternative stack-based decoder that avoids string mutation.
    """
    stack = bytearray()
    out = bytearray()
    maxdepth = 0
    for x in s:
        while True:
            if x & 0x80 == 0:
                out.append(x)
                if not stack:
                    break
                x = stack.pop()
            else:
                x,y = digrams[x]
                stack.append(y)
                if len(stack) > maxdepth: maxdepth = len(stack)
    print(f"undizzy_stack: max stack depth {maxdepth}")
    return out

"""
The stack implementation is nice for assembly.
This is a working 40-byte implementation of undizzy_stack for the 65c02:


; uncompress a zero-terminated dizzy string at dizzyp using digrams lookup
; outputs uncompressed characters via putc (excluding the terminator)

dizzyp  = $10       ; pointer to compressed data
digrams = $12       ; digram lookup table (128 2-byte pairs)


undizzy:
        ldx #0      ; track stack depth
@nextz: lda (dizzyp)   ; get encoded char
        tay
        inc dizzyp  ; inc pointer
        bne @ready
        inc dizzyp+1
@ready: tya
@chk7:  bmi @subst  ; is it a digraph (bit 7 set)?
        beq @done   ; if 0 we're done
        jsr putc
@stk:   cpx #0      ; any stacked items?
        beq @nextz
        dex
        pla         ; pop latest
        bra @chk7
@subst: sec
        rol         ; index*2+1 for second char in digram
        tay
        lda (digrams),y
        inx         ; track stack depth
        pha         ; stack the second char
        dey
        lda (digrams),y   ; fetch the first char of the digram
        bra @chk7   ; keep going
@done:  rts


putc:   sta $f001   ; pymon character output, or could write buffer etc
        rts

"""


if __name__ == "__main__":
    """
    The input file used here is the text of Alice in Wonderland from Project Gutenberg
    at https://www.gutenberg.org/ebooks/11

    The recursive digram coding gets about 1.8x compression vs about 2.7x for gzip
    source: 168,042 bytes
    dizzy:   92,730 bytes
    gzip:    61,006 bytes

    The original UTF-8 + BOM format was converted to ascii by:

        sed '1s/^\xEF\xBB\xBF//' < alice.txt > tmp
        iconv -f utf-8 -t ascii//TRANSLIT tmp > alice.asc
    """
    alice = open('alice.asc').read().encode('ascii')

    data, lookup = dizzy(alice)
    ratio = 1. * len(alice) / len(data)
    print(f"Compressed {len(alice)} bytes to {len(data)} bytes: ratio {ratio:.1f}x")

    recover = undizzy(data, lookup)
    print("undizzy ok?", recover == alice)

    recover = undizzy_stack(data, lookup)
    print("undizzy_stack ok?", recover == alice)

    altdata = dizzy_squeeze(alice, lookup)
    print("dizzy_encode ok?", altdata == data)
