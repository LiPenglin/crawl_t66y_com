import requests
url = 'http://rmdown.com/download.php?ref=1723bb65b274c2a954b3bdf2f59c8be2d5a39b2b910&reff=MTUwMTU2MTYxNA%3D%3D&submit=download'
bt = requests.get(url).content

with open(file='F:\\1024bt\\2017-07-31\\test.torrent', mode='wb') as f:
    f.write(bt)