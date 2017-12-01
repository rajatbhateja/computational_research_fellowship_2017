import xml.etree.ElementTree as ET
import bs4
import os
import csv
from collections import defaultdict
import psycopg2
from psycopg2.extensions import *

final = []
l = []

def get_first(Node):
  for x in Node:
    return x

dates_dict = defaultdict(list)

# local directory path where the xml files are stored
path = 'C:/Users/USER/Documents/Fellowship/etd-data/etd-data/test'

for filename in os.listdir(path):
    fullname = os.path.join(path, filename)
    tree = ET.parse(fullname)
    code = []
    codes = []
    Dest = {}

    for elem in tree.findall(".//md"):
        Dest = {
            'value': (elem.findtext("value"))
        }
        codes.append(Dest)

    for elem in tree.findall(".//relation"):
        Pid = {
            'pid': (elem.findtext("pid"))
        }
        code.append(Pid)
    # you can extract other fields instead of just date and degreediscipline based on your needs
    generator = (dict['value'] for dict in codes)
    for i in generator:
        l.append(i)
        soup = bs4.BeautifulSoup(''.join(i), "lxml")
        str_date = (soup.find('dc:date'))
        if str_date is not None:
            str_date1 = str_date.string
            for el in code:
                el['year'] = str_date1
        str_dept = soup.find('dcterms:localthesisdegreediscipline')
        if str_dept is not None:
            str_dept1 = str_dept.string
            for el in code:
                el['dept'] = str_dept1

    final.append(code)

list_xml = []
for x in final:
    for y in x:
        list_xml.append(y)

for item in list_xml:
    columns = item.keys()
    values = [item[column] for column in columns]

    insert_statement = 'insert into xml (%s) values %s'

    cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
    # print(cursor.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values))))


conn.commit()