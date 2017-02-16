#!/usr/bin/env python3.6
import json
from itertools import groupby
from pathlib import Path

with Path('results.json').open() as f:
    results = json.load(f)


grouping = 'python', 'url', 'db', 'queries', 'concurrency'
sort_on = grouping + ('aiohttp',)
results.sort(key=lambda v: [v[g] for g in sort_on])

i = 0
head = None
url_previous = None
for k, g in groupby(results, lambda v: [v[g] for g in grouping]):
    python, url, db, queries, concurrency = k
    if url_previous and url_previous != url:
        print()
    url_previous = url
    if i == 0:
        head = f'{"url":>20} {"Py":>4} {"DB":>8} {"queries":>8} {"Conc":>8} '
    line =     f'{url:>20} {python:>4} {db:>8} {queries:>8} {concurrency:>8} '
    ref = None
    for j, data in enumerate(g):
        if i == 0:
            head += f'{data["aiohttp"]:>15} '
        s = f'{data["request_rate"]:0,.0f}'
        if j == 0:
            ref = data["request_rate"]
        else:
            improvement = (data['request_rate'] - ref) / ref * 100
            s += f' |{improvement:3.0f}%'
        line += f'{s:>15} '
    if i == 0:
        print(head)
    print(line)
    i += 1
