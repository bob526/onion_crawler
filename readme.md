# Tor 網站爬蟲

## 安裝Tor
參考[Using Tor with the Python Requests Library][1]，先要把Tor建起來，
因此再去看[Tor的官方安裝教學][2]，照著他上面寫的，把apt的source list手動加一些來源
```
deb https://deb.torproject.org/torproject.org xenial main
deb-src https://deb.torproject.org/torproject.org xenial main
```
然後又因為安全性的關係，需要有金鑰才可以下載，所以又需要執行下面的指令
```
gpg --keyserver keys.gnupg.net --recv A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89
gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | sudo apt-key add -
```
然後就是apt update和install，套件名稱要打「deb.torproject.org-keyring」

## 讓Python連上Tor
用Python掛Tor Proxy時出現的問題：
Missing dependencies for SOCKS support
照著上述[英文教學網站][1]弄的程式碼，卻出現了這個錯誤，
網路上有人提供了[環境變數all_proxy的解法][3]，我試過了，沒有用，看起來這個環境變數是走http的proxy，
可是問題是，Tor並不是走http的proxy，他是有socks5，所以會有問題。
我也連進去[環境變數all_proxy的解法][3]裡面引用的[Github Issue連結][4]，裡面提供一個解法，是用「pip install requests[socks]」，一樣的問題，他要走http的proxy，但是tor並不是。

目前翻到[Python中Request 使用socks5代理的两种方法(个人推荐方法二)][5]這個文件，測試完，可以用。
然而，實際上還是無法連線到Tor的網站，從錯誤訊息來看，好像是python的requests函式把.onion的網域直接擋掉。就去網路上搜尋解法，根據[此stackoverflow的回答][6]，好像是dns的解析問題，就照著該回答的建議
不知道為什麼，類似的打法，換成參考6的寫法，就可以連上Tor了。

## 使用Daniel所整理好的Tor網站清單
由網友Daniel所寫出來的php程式和網站[「Onion link list」][7](需要Tor的連線)，有一起把其他網站整理好的.onion網域的網站，一起整理進去，還順便分類，注記加入時間、最後可以連上的時間等等。
他也有把[php原始碼開源在Github上][8]，我大略看一下，他是參考好幾個其他網站所整理的.onion網站清單，把這些整理好的網站加入自己伺服器的資料庫上，在24小時做一次的網站連線測試去更新資訊和清單。
以下是他的php原始碼裡，更新網站所參考的網站
```
check_links($onions, $ch, 'https://tt3j2x4k5ycaa5zt.onion.to/antanistaticmap/stats/yesterday');
check_links($onions, $ch, 'https://tt3j2x4k5ycaa5zt.tor2web.org/antanistaticmap/stats/yesterday');
check_links($onions, $ch, 'http://tt3j2x4k5ycaa5zt.onion/onions.php?format=text');
check_links($onions, $ch, 'http://skunksworkedp2cg.onion/sites.txt');
check_links($onions, $ch, 'http://7cbqhjnlkivmigxf.onion/');
check_links($onions, $ch, 'http://visitorfi5kl7q7i.onion/address/');
//opyright (C) 2016 Daniel Winzen <d@winzen4.de>
```
不過由於我想專注在爬蟲上，所以這部份，我是直接拿Daniel大大所提供的[Json格式][9](需要Tor連線)來當作網址清單。

## 簡易網頁爬蟲
使用Python的requests函式庫，把所有的網站下載下來，等待以後做分析使用。
本部份的程式碼分成兩個部份，一個是連接到Tor，一個是下載網頁。
### Connect to Tor
```
session = requests.session()
session.proxies = {'http':  'socks5h://localhost:9050',
                   'https': 'socks5h://localhost:9050'}
```
這是連接到Tor網路的程式碼，因為需要常駐Tor的Proxy界面，所以需要使用到Python requests的session object，讓一些設定能夠直接記住，這樣就不用每次連線都要設定參數。
proxy的設定就是參照Tor的api規定的，要用sock5，連上本機端的9050 port。記得要先確定自己電腦的Tor服務是有啟動的，不然會連不上去。
### 簡易爬蟲
```
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
        down_url_file.write(one_url)
```
這部份就是先讀取事先取得的Tor網站清單，然後request過去，如果可以成功連上去，就把網頁下載下來。如果不能連上去，那就會出現requests所定義的ConnectionError，排除掉，即可。

## 時間
109個網站，費時25分鐘（平均一個網站4分多鐘）
Python程式只有單執行緒。

運行環境：
>CPU: Intel Xeon E3-1231v3@3.4GHz  
>RAM: 8 GB @1600MHz  
>OS: Kubuntu 16.04  
>Disk: HDD  

## Reference
```
[1]: https://medium.com/@mr_rigden/using-tor-with-the-python-request-library-79015b2606cb "Using Tor with the Python Requests Library"
[2]: https://www.torproject.org/docs/debian.html.en " Home » Documentation » Debian/Ubuntu Instructions "
[3]: https://stackoverflow.com/questions/38794015/pythons-requests-missing-dependencies-for-socks-support-when-using-socks5-fro "stackoverflow-python request missing ..."
[4]: https://github.com/kennethreitz/requests/issues/3516 "Missing dependencies for SOCKS support."
[5]: https://doomzhou.github.io/coder/2015/03/09/Python-Requests-socks-proxy.html "Python中Request 使用socks5代理的两种方法(个人推荐方法二)"
[6]: https://stackoverflow.com/questions/42971622/fetching-a-onion-domain-with-requests?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa "Stackoverflow fetching a .onion domain"
[7]: http://onionsnjajzkhm5g.onion/onions.php "Onion link list"
[8]: https://github.com/DanWin/onion-link-list "onion-link-list - A set of scripts to list tor hidden services - Github"
[9]: http://onionsnjajzkhm5g.onion/onions.php?format=json "Onion link list - Json format"
```

[1]: https://medium.com/@mr_rigden/using-tor-with-the-python-request-library-79015b2606cb "Using Tor with the Python Requests Library"
[2]: https://www.torproject.org/docs/debian.html.en " Home » Documentation » Debian/Ubuntu Instructions "
[3]: https://stackoverflow.com/questions/38794015/pythons-requests-missing-dependencies-for-socks-support-when-using-socks5-fro "stackoverflow-python request missing ..."
[4]: https://github.com/kennethreitz/requests/issues/3516 "Missing dependencies for SOCKS support."
[5]: https://doomzhou.github.io/coder/2015/03/09/Python-Requests-socks-proxy.html "Python中Request 使用socks5代理的两种方法(个人推荐方法二)"
[6]: https://stackoverflow.com/questions/42971622/fetching-a-onion-domain-with-requests?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa "Stackoverflow fetching a .onion domain"
[7]: http://onionsnjajzkhm5g.onion/onions.php "Onion link list"
[8]: https://github.com/DanWin/onion-link-list "onion-link-list - A set of scripts to list tor hidden services - Github"
[9]: http://onionsnjajzkhm5g.onion/onions.php?format=json "Onion link list - Json format"