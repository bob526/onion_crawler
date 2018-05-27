import requests
import json

# Connect to Tor
session = requests.session()
session.proxies = {'http':  'socks5h://localhost:9050',
                   'https': 'socks5h://localhost:9050'}

respond = session.get('http://onionsnjajzkhm5g.onion/onions.php?format=json')

fileptr = open('list.json', 'w')
fileptr.write(respond.text)