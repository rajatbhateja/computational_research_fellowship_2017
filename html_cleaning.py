import glob
import os.path
from bs4 import BeautifulSoup
import csv
import re
import psycopg2
from psycopg2.extensions import *
from psycopg2.extras import *
import urllib.parse
from datetime import datetime
startTime = datetime.now()

cedilla2latin = [[u'Á', u'A'], [u'á', u'a'], [u'Č', u'C'], [u'č', u'c'], [u'Š', u'S'], [u'š', u's'], [u'è', u'e'], [u'é', u'e'], [u'ê', u'e'], [u'ë', u'e'], [u'ç', u'c'], [u'à', u'a'], [u'â', u'a'], [u'ù', u'u'], [u'û', u'u'], [u'ü', u'u'], [u'ÿ', u'y']]
tr = dict([(a[0], a[1]) for (a) in cedilla2latin])

def transliterate(line):
    new_line = ""
    for letter in line:
        if letter in tr:
            new_line += tr[letter]
        else:
            new_line += letter
    return new_line


# Define our connection string
#conn_string = "host='' dbname='' user='' password='' port=''"

# print the connection string we will use to connect
print("Connecting to database\n	->%s" % (conn_string))

# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect(conn_string)

# conn.cursor will return a cursor object, you can use this cursor to perform queries
dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
print("Connected!!")

dict_cur.execute("SELECT distinct pid, content FROM html")
ans = dict_cur.fetchall()
ans1 = []
for row in ans:
    ans1.append(dict(row))



for Dest in ans1:
    line = Dest['content']
    punctuation = "–~`'!@#$%^&*,;.?:\/]}[{()\"_\\>|<+=\r"
    replace = "                                  "
    filter = str.maketrans(punctuation, replace)
    line = line.translate(filter)
    # remove digits with regex
    line = re.sub("(^|\W)\d+($|\W)", " ", line)
    #remove http links
    line = re.sub(r'https?:\/\/.*[\r\n]*', '', line, flags=re.MULTILINE)
    #remove \x characters
    # escape_char = re.compile(r'\\x[0123456789abcdef]+')
    line = re.sub(r'[^\x00-\x7f]', r'', line)
    # transliterate to Latin characters
    line = transliterate(line)
    line = line.lower()
    line = line.strip(' ')
    # print(line)
    Dest['content'] = line
    columns = Dest.keys()
    values = [Dest[column] for column in columns]
    insert_statement = 'insert into html_clean (%s) values %s'
    dict_cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
    print(dict_cur.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values))))
    conn.commit()


print(datetime.now() - startTime)