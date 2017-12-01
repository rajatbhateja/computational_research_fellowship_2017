import glob
import os.path
from bs4 import BeautifulSoup
import csv
import re
import psycopg2
from psycopg2.extensions import *
import logging

path = 'C:/Users/USER/Documents/Fellowship/etd-data/etd-data/test2'
l = []
list_text = []
Dest = {}
final_result = ""
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename= "", level= logging.DEBUG, format= LOG_FORMAT, filemode='w')
logger = logging.getLogger()

# traversing through the file names to get the pid from file name and text in the file using Beautiful Soup
for file_name in glob.glob(os.path.join(path, "*.html")):
    logger.debug("Processing file name %s" %file_name)
    with open(file_name, encoding="utf8") as html_file:
        soup = BeautifulSoup(html_file, "lxml")
        visible_text = soup.getText()
        start = '\\'
        end = '__'
        result = file_name[file_name.find(start)+1:file_name.find(start)+7]
        for char in result:
            if char in "_":
                final_result = result.replace(char, '')
            else:
                final_result = result
        Dest = dict(pid=final_result, content=visible_text)
        list_text.append(Dest)

import json
with open('output.json', 'w') as fout:
    json.dump(list_text, fout)


# Define our connection string
#conn_string = "host='' dbname='' user='' password='' port='5432'"

# print the connection string we will use to connect
print("Connecting to database\n	->%s" % (conn_string))

# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect(conn_string)

# conn.cursor will return a cursor object, you can use this cursor to perform queries
cursor = conn.cursor()
print("Connected!")

for item in list_text:
    columns = item.keys()
    values = [item[column] for column in columns]
    insert_statement = 'insert into html (%s) values %s'
    cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
    print(cursor.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values))))


conn.commit()
