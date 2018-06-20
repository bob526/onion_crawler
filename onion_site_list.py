import requests
import json

def writeOnionSiteList(listFileName):
    '''
    This function accesss the list of onion site provided by Daniel in json format.
    listFileName should be a string containing the filename that you want to save the onion site list.
    Recommend: from onion_site_list import *
    '''
    # Connect to Tor
    print('Prepare to connect to Tor')
    session = requests.session()
    session.proxies = {'http':  'socks5h://localhost:9050',
                       'https': 'socks5h://localhost:9050'}
    print('Prepare to access onion site list')
    respond = session.get('http://onionsnjajzkhm5g.onion/onions.php?format=json')
    print('Access completed')
    print('Open file: '+listFileName)
    fileptr = open(listFileName, 'w')
    fileptr.write(respond.text)
    fileptr.close()
    print('Close '+listFileName+'\nFunction complete')
