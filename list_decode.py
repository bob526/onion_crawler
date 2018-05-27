import json
import datetime

fileptr = open('list.json', 'r')
decode_list = json.load(fileptr)

#decode_list[u'onions'][0~???]

#print(datetime.datetime.fromtimestamp(int(u'1526867199')).strftime('%Y-%m-%d %H:%M:%S'))

all_url=[]
for one_record in decode_list[u'onions']:
    #print(one_record[u'address']+'.onion')
    all_url.append(one_record[u'address']+'.onion')
    #raw_input()
    #No check up or down

#print(len(all_url))

fileptr = open('url_pool.txt', 'w')
for url in all_url:
    fileptr.write(url+'\n')
