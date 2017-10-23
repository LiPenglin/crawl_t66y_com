import requests
import re
proxies = { "http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080", }
doc = requests.get("http://t66y.com/htm_data/2/1707/2551453.html", proxies=proxies).content.decode('gbk')
print(doc)
hash = re.search(r'rmdown\.com/link\.php\?hash=(.*?)<', doc, re.S).group(1)
print(hash)