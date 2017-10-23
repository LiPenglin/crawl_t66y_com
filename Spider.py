import requests
import pymongo
import os
import re
# import base64
import time
import viidii

from pyquery import PyQuery as pq
from Config import *

from urllib import parse


# db
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
global table

# 时间
import datetime
today = datetime.date.today()
one_day = datetime.timedelta(1)
yesterday = today - one_day
# yesterday = today
before_day = yesterday - one_day

yesterday_str = yesterday.strftime('%Y-%m-%d')
before_day_str = before_day.strftime('%Y-%m-%d')

# 计数器
global count

def insert_to_mongo(info):
    global count
    global table
    query_info = {'art_name': info['art_name']}
    if table.find(query_info).limit(1).count() == 0:
        table.insert(info)
        count += 1
        print('成功插入第 ', count, ' 数据:', info)
    else:
        print('重复:', info)
    '''
    1. 插入mongo 之前，info 中被加入一条_id字段
    2. python 传递参数
        对于不可变对象作为函数参数，相当于C系语言的值传递；
        对于可变对象作为函数参数，相当于C系语言的引用传递。
    3. 所以如果新插入的info 如果不flush，mongo 将会报错
    '''

def art_bt_hash(url):
    '''
    得到hash 码
    :param url: 
    :return: 
    '''
    doc = requests.get(url=url, proxies=PROXIES).content.decode('gbk')
    hash = re.search(r'rmdown\.com/link\.php\?hash=(.*?)<', doc, re.S).group(1) # 正则直接匹配
    return hash

def art_item(tr):
    '''
    得到一条（一件艺术品），获取这个art 的hash 码，对info 进行封装
    :param tr: 
    :return: 
    '''
    info = {}
    info['art_name'] = tr.find('h3').text()
    hash_url = tr.find('.tal > h3 > a').attr('href')
    art_url = '{}{}'.format(CLSQ, hash_url)
    info['art_url'] = art_url
    try:
        info['art_hash'] = art_bt_hash(art_url)
    except AttributeError as e:
        print(e.args)
        return
    except UnicodeDecodeError as e:
        print(e.args)
        return
    info['art_time'] = yesterday_str
    info['art_flag'] = '0'
    insert_to_mongo(info=info)

def next_tags(**kwargs):
    '''
    翻页
    :param kwargs: 
    :return: 
    '''
    base = kwargs['base']
    page_num = kwargs['page_num']
    url = '{}&page={}'.format(base, page_num)
    print(url)
    try:
        doc = requests.get(url=url, proxies=PROXIES).content
    except requests.exceptions.ContentDecodingError as e:
        print(e.args)
        time.sleep(2)
        next_tags(base=base, page_num=page_num)
        return
    html = pq(doc)
    trs = html.find('#ajaxtable > tbody:nth-child(2) > tr').items()

    for tr in trs:
        art_time = tr.find('div[class=f10]').text()
        if art_time == before_day_str:
            return
        if art_time == yesterday_str:
            art_item(tr)
    next_tags(base=base, page_num=page_num+1)

# 得到 hash 码，然后放入mongodb
def art_tags(**kwargs):
    url = kwargs['url']
    print(url)
    doc = requests.get(url=url, proxies=PROXIES).content
    html = pq(doc)
    trs = html.find('#ajaxtable > tbody:nth-child(2) > tr').items()
    flag = False

    for tr in trs:
        if flag:
            art_time = tr.find('div[class=f10]').text()
            if art_time == before_day_str:
                return
            if art_time == yesterday_str:
                art_item(tr)
        if tr.text() == '普通主題':
            flag = True
    next_tags(base=url, page_num=2)

def downloader(**kwargs):
    '''
    下载器
    r = requests.get(url).content
    with open(file=path, mode='wb') as f:
        f.write(r)
    :param kwargs: 
    :return: 
    '''
    url = kwargs['url']
    hash = kwargs['hash']
    r = requests.get(url).content
    # print(url, r)
    path = '{}{}.torrent'.format(BT_PATH.format(yesterday_str), hash)
    try:
        with open(file=path, mode='wb') as f:
            f.write(r)
    except FileNotFoundError as e:
        print(e.args)
        return False
    print('bt -> ', path)
    return True
# bt 下载器，从mongodb 中得到hash，下载bt
def art_bt_download(**kwargs):
    global table
    query_info = kwargs['query_info']
    for item in table.find(query_info):
        art_hash = item['art_hash']
        # stamp_base64 = parse.quote(base64.b64encode(str(time.time())[0:10].encode()).decode())
        stamp_base64 = parse.quote(viidii.get_b64(art_hash=art_hash))
        url = '{}ref={}&reff={}&submit=download'.format(CLSQ_DOWNLOAD, art_hash, stamp_base64)
        if downloader(url=url, hash=art_hash):
            update_data = {'$set' : {'art_flag' : '1'}}
            table.update(spec=item, document=update_data, upsert=False)
        else:
            table.remove(item)
            print('删除一条数据...')

if __name__ == '__main__':
    global count

    # 创建文件夹
    if not os.path.exists(BT_PATH.format(yesterday_str)):
        os.makedirs(BT_PATH.format(yesterday_str))
    # 类别list
    url_dict = {'2' : '亞洲無碼原創區', '15' : '亞洲有碼原創區', '5' : '動漫原創區'}
    # 遍历
    for type, name in url_dict.items():
        count = 0
        global table
        table = db[name]
        print('启动maker...')
        art_tags(url='{}thread0806.php?fid={}'.format(CLSQ, type))
        # print('启动下载器...')
        # art_bt_download(query_info={'art_flag': '0'})



