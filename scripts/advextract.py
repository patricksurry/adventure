"""
source files

advent1.txt: long desc [MAXLOCJ=140, max 1299, total 17207]
advent2.txt: short desc [MAXLOC=140, max 124, total 5567]
advent3.txt: items [MAXOBJ=64, max 438, total 5042]
advent4.txt: messages [MAXMSG=201, max 1395, total 16976]

advcave.h: 140 x ..16 x u32

advword.h: word/code x 306
"""

import re
import json


def slurp_text(fname: str):
    n = 0
    s = ''
    chunks = {}
    for line in open(fname).readlines():
        if line.strip() == f"#{n+1}":
            if n:
                chunks[n] = s.rstrip()
            s = ''
            n += 1
        else:
            s += line
    chunks[n] = s.rstrip()      # drop trailing newline on everything
    assert list(chunks.keys()) == list(range(1, len(chunks)+1))
    return list(chunks.values())


def read_words(fname: str):
    # read lines like { "above", 29 },
    lines = open(fname).read().splitlines()
    lines = [line for line in lines if re.match(r'\s+{.*},?\s*', line)]
    data = [eval(line.replace('{', '(').replace('}', ')').rstrip(',')) for line in lines]
    data = [(word, code % 1000, code // 1000) for (word, code) in data]
    return data


def parse_cave(fname: str):
    # read lines like 	"129044000,124077000,126028000,",
    lines = open(fname).read().splitlines()
    lines = [line for line in lines if re.match(r'\s*"[0-9,]+"?,\s*', line)]
    data = [[int(x) for x in line.strip().rstrip(',').strip('"').split(',') if x] for line in lines]
    return data


text = {}
for i,typ in enumerate(['long', 'short', 'items', 'messages']):
    fname = f"src/advent{i+1}.txt"
    chunks = slurp_text(fname)
    print(f"{fname} {typ} n={len(chunks)} maxlen={max(len(s) for s in chunks)} chrs={sum(len(s) for s in chunks)}")
    text[typ] = chunks

fname = 'src/advword.h'
words = read_words(fname)
print(
    f"{fname} n={len(words)} u={len(set(word for (word, _, _) in words))} "
    f"maxlen={max(len(word) for (word, _, _ ) in words)} maxlo={max(lo for (_,lo,_) in words)} "
    f"maxhi={max(hi for (_,_,hi) in words)}"
)
fname = 'src/advcave.h'
travel = parse_cave(fname)
dups = sum(text['long'][i] == text['short'][i] for i in range(len(text['short'])))
print(f"{fname} n={len(travel)} maxdir={max(len(xs) for xs in travel)} "
    f"maxval={max(sum(travel, []))} dups={dups}")

items = [chunk.strip().strip('/').split('/') for chunk in text['items']]
items = [[s.rstrip() for s in states] for states in items]
print(f"items n={len(items)} maxstate={max(len(ds) for ds in items)} "
    f"maxlen={max(len(d) for d in sum(items, []))}")

advent = dict(
    words = words,
    messages = text['messages'],
    items = items,
    caves = [
        dict(
            long=text['long'][i],
            short=text['short'][i],
            travel=travel[i],
        )
        for i in range(len(travel))
    ],
)

json.dump(advent, open('data/advent.json', 'w'), indent=4)
