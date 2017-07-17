#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import csv
import sqlite3
import zipfile
import urllib.request


def ejdict():
    fname = 'EJDict/src/ejdic-hand-utf8.txt'
    with open(fname) as csvf:
        reader = csv.reader(csvf, delimiter='\t')
        for row in reader:
            yield row[0], ', '.join(row[1:])


def jedict():
    url = 'http://ftp.monash.edu/pub/nihongo/edict.zip'
    print('downloading EDICT...')
    res = urllib.request.urlopen(url)
    print('opening EDICT...')
    f = io.BytesIO(res.read())

    print('reading EDICT...')
    with zipfile.ZipFile(f) as zf:
        with zf.open('edict') as csvf:
            for row in csvf.readlines():
                split = row.decode('euc-jp').split('/')
                word, mean = split[0], split[1:]
                yield word, ', '.join(mean)


if __name__ == '__main__':
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS dictionary (word, mean)")

    for word, mean in ejdict():
        c.execute("INSERT INTO dictionary VALUES (?, ?)", (word, mean))
    for word, mean in jedict():
        c.execute("INSERT INTO dictionary VALUES (?, ?)", (word, mean))

    conn.commit()
    conn.close()
