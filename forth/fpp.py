import re
import sys
from os import path
from warnings import warn


consts = {}
referenced = set()


def define_const(m):
    val = m.group(1)
    val = inline_consts(val)
    if ' ' in val:
        val = re.sub(r'\$([0-9a-fA-F]+)\b', r'0x\1', val)
        # only allow v1 v2 op
        a, b, c = val.split(' ')
        val = str(eval(f"{a} {c} {b}"))
    consts[m.group(2)] = val
    return ''

def ref_const(m):
    c = m.group(0)
    if c not in consts:
        warn(f"constant {c} not found")
        return c
    referenced.add(c)
    return consts[c]

def extract_consts(s):
    return re.sub(r'^(.*?)\s+constant\s+([A-Z][A-Z&-_]+)$', define_const, s)

def inline_consts(s):
    return re.sub(r'[A-Z][A-Z&-_]+', ref_const, s)

def strip_comments(lines):
    return [re.sub(r'\\.*', '', line).rstrip() for line in lines]

def include_files(lines, basedir):
    out = []
    for line in lines:
        m = re.match(r'include (\S+)', line.strip())
        if m:
            out += read_lines(m.group(1), basedir)
        else:
            out.append(line)
    return out

def read_lines(fname, basedir=''):
    fname = path.join(basedir, fname)
    return include_files(strip_comments(open(fname).read().splitlines()), basedir)

assert len(sys.argv) == 2, "Usage: python fpp.py infile"

infile = sys.argv[1]
base, ext = path.splitext(infile)
outfile = f"{base}_fpp{ext}"

print(f"fpp: {infile} => {outfile}")

lines = read_lines(path.basename(infile), basedir = path.dirname(infile))

# lines = map(inline_consts, map(extract_consts, lines))

open(outfile, "w").write('\n'.join([line for line in lines if line]))
