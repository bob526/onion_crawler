import requests
import datetime

# Connect to Tor
session = requests.session()
session.proxies = {'http':  'socks5h://localhost:9050',
                   'https': 'socks5h://localhost:9050'}

'''
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket
'''

# Test section
respond = session.get('http://httpbin.org/ip')
print(respond.text)
raw_input('Test: The IP address should be different. Press any key to continue.')

url_pool_file = open('url_pool.txt', 'r')
down_url_file = open('down_url.txt', 'w')

#print(datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S'))
down_url_file.write(datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S')+'\n')

for one_url in url_pool_file:
    one_url = one_url.replace('\n','')
    try:
        respond = session.get('http://'+one_url)
        page_content = open('data/'+one_url+'.html', 'w')
        page_content.write(respond.text.encode('utf-8'))
        page_content.close
    except requests.ConnectionError as ce:
        print(ce)
        print(one_url+' is down right now.')
        down_url_file.write(one_url+'\n')
    
    #print(respond.text)
    #raw_input()

url_pool_file.close()
down_url_file.close()
