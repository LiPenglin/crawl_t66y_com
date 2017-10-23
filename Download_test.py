import urllib.request
url = 'http://i3.hunantv.com/p1/20150906/1637244570C.jpg'
file_name = 'F:\\img\\ym.jpg'
...
# Download the file from `url` and save it locally under `file_name`:
urllib.request.urlretrieve(url, file_name)