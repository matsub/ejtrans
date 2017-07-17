#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import sqlite3

this_dir = os.path.dirname( os.path.abspath(__file__) )
db_path = os.path.join(this_dir, "dictionary.db")


SELECT = lambda w: "SELECT word, mean FROM dictionary WHERE word GLOB '%s*'" % w

if __name__ == "__main__":
    try:
        key = sys.argv[1]
    except IndexError:
        print('a word required.', file=sys.stderr)
        exit(1)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for word, mean in c.execute(SELECT(key)):
        print(word, '->', mean)
    conn.close()
