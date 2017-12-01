from collections import defaultdict
import sys
import gensim
import unicodecsv as csv
import json

word = sys.argv[1]
# word = 'man'
y1 = '1982'
model = gensim.models.Word2Vec.load('model_%s.bin' %y1)
l1 = model.wv.most_similar(positive=[word])
y2 = '1991'
model = gensim.models.Word2Vec.load('model_%s.bin' %y2)
l2 = model.wv.most_similar(positive=[word])

e = defaultdict(list)

l3 = []
for e in l1:
    e_list = list(e)
    e_list.append('1982')
    l3.append(e_list)

l4 = []
for e in l2:
    e_list = list(e)
    e_list.append('1991')
    l4.append(e_list)

l5 = []
for e in l3:
    my_dict= {}
    my_dict['word'] = e[0]
    my_dict['prob'] = e[1]
    my_dict['time'] = e[2]
    l5.append(my_dict)

l6 = []
for e in l4:
    my_dict= {}
    my_dict['word'] = e[0]
    my_dict['prob'] = e[1]
    my_dict['time'] = e[2]
    l6.append(my_dict)

l7 = l5 + l6

keys = l7[0].keys()
with open('public/results.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(l7)
# l8 = json.dumps(l7)
# print(l8)
# sys.stdout.flush()



# y1 = sys.argv[2]
# y2 = sys.argv[3]
# word = sys.argv[1]
# y1 = 1982
# y2 = 1992
# word = 'woman'
# send_list = []
# for i in range(y1, y2):
#     try:
#         model = gensim.models.Word2Vec.load('model_%s.bin' %i)
#         print(i)
#         a_list = model.wv.most_similar(positive=[word])
#         send_list.append(a_list)
#         print(a_list)
#         print('hello')
#     except:
#         pass
#
#
#
# print(send_list)
# sys.stdout.flush()
