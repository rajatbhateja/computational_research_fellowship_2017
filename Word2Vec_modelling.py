
from psycopg2.extras import *
import urllib.parse
import nltk, re, pprint
from nltk import word_tokenize
import pandas as pd
from collections import defaultdict
import unicodecsv as csv
# nltk.download('punkt')


import itertools
from gensim.models.wrappers.fasttext import FastText
import gensim, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Define our connection string
# conn_string = "host='' dbname='' user='' password='' port=''"

# print the connection string we will use to connect
print("Connecting to database\n	->%s" % (conn_string))

# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect(conn_string)

dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
print("Connected!!")

#the query below can be changed based on how you aggregate the data
dict_cur.execute("SELECT distinct year, content from fasttext_input_corpora where year='post-2000'")
ans = dict_cur.fetchall()
ans1 = []
for row in ans:
    ans1.append(dict(row))

string1 = ''
string2 = ''

for item in ans1:
    string2 = string2 + item['content']

string2 = string2.replace('\n', ' ')
ans2 = []
post_dict = dict(year = 'post-2000', content = string2)
ans2.append(post_dict)




for item in ans2:
    # my_data = [x.split(' ') for x in item['content'].split('   ')]
    my_data = item['content']
    # item['year'] = int(item['year'])
    # pprint.pprint(item)
    # eval("model_%s" % (item['year']))
    model = gensim.models.Word2Vec(min_count=1, workers=4, size=50)
    model.build_vocab(my_data)
    for epoch in range(5):
        model.train(my_data, total_examples=model.corpus_count, epochs=model.iter)
        model.alpha -= 0.002 # decrease the learning rate
        model.min_alpha = model.alpha # fix the learning rate, no decay

    model.save('model_%s.bin' %item['year'])
