#!/usr/bin/env python3
import os
import json
from itertools import groupby
from pathlib import Path

with Path('results.json').open() as f:
    results = json.load(f)

compare = os.getenv('COMPARE', 'aiohttp').lower()
assert compare in ('python', 'aiohttp')

not_compared = 'python' if compare == 'aiohttp' else 'aiohttp'
grouping = not_compared, 'url', 'db', 'queries', 'concurrency'
sort_on = grouping + (compare,)
results.sort(key=lambda v: [v[g] for g in sort_on])

i = 0
head = None
url_previous = None
for k, g in groupby(results, lambda v: [v[g] for g in grouping]):
    not_compared_version, url, db, queries, concurrency = k
    if url_previous and url_previous != url:
        print()
    url_previous = url
    if i == 0:
        head = f'{"URL":>18} {not_compared:>8} {"DB":>8} {"queries":>8} {"Conc":>8} '
    line =     f'{url:>18} {not_compared_version:>8} {db:>8} {queries:>8} {concurrency:>8} '
    ref = None
    for j, data in enumerate(g):
        s = f'{data["request_rate"]:0,.0f}'
        if j == 0:
            if i == 0:
                head += f'{data[compare]:>10} '

            ref = data["request_rate"]
            line += f'{s:>10} '
        else:
            if i == 0:
                head += f'{data[compare]:>15} '
            improvement = (data['request_rate'] - ref) / ref * 100
            s += f' |{improvement:3.0f}%'
            line += f'{s:>15} '
    if i == 0:
        print(head)
    print(line)
    i += 1
