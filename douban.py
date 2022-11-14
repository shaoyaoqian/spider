import requests
from bs4 import BeautifulSoup
import re
import random
import string

from utils import email
from database import *

# 分析网页
def analysis_movie(soup):
    # 查找标题
    heading = soup.find(name='h1')
    if heading == None:
        exit()
    else :
        heading = heading.findAll(name='span')
    # 查找年份
    year = ' ' if len(heading) == 1 else heading[1].string[1:5]
    title = heading[0].string
    # 查找导演
    directors_temp   = soup.findAll(name='a', attrs={"rel"      :"v:directedBy"})
    directors = [director.string for director in directors_temp]
    # 查找评分人数
    voter    =  0  if soup.find(name='span', attrs={"property" :"v:votes"}) == None else soup.find(name='span', attrs={"property" :"v:votes"}).string
    # 查找演员
    actors_temp   = soup.findAll(name='a', attrs={"rel"      :"v:starring"})
    actors = [actor.string for actor in actors_temp]
    # 查找类型
    kinds_temp    = soup.findAll(name='span', attrs={"property" :"v:genre"})
    kinds = [kind.string for kind in kinds_temp]
    # 查找国家
    country = soup.find_all(name='span',text='制片国家/地区:')
    country = ' ' if len(country) == 0 else country[0].next_sibling
    # 拼接副标题
    subtitle = " {} / {} / {} / {} ".format(
        ",".join(country.split(" / ")), 
        ','.join(kinds), 
        ','.join(directors), 
        ','.join(actors))
    # 查找评分
    rating   = soup.find(id='interest_sectl').find(name='strong').string
    # 查找电影海报
    poster_temp   = soup.find(id='mainpic')
    poster = ' ' if poster_temp == None else poster_temp.find(name='img').attrs['src']
    return title, year, subtitle, rating, poster, voter


def find_movie_recommendations(soup):

    # 寻找相邻网页链接
    # 如果没有找到就跳过
    if soup.find(id='recommendations') == None:
        return []
    
    recommendations = soup.find(id='recommendations').findAll('a')
    all_subject_id = []
    for item in recommendations:
        item_url = item.attrs['href']
        subject_id = re.match(".*subject/(\d+)", item_url)[1]
        all_subject_id.append(int(subject_id))
    
    return all_subject_id


def fetch_one_subject(timeout=20):
    # 从数据库中选取1条未爬取的数据
    # 如果数据库中没有爬取过的数据，那么生成一个7位数的随机数
    result = curs.execute(SELECT_STATUS.format(status=0))
    result = list(result)
    if len(result)>0:
        seed = result[0][0]
    else: 
        seed = 1292403

    url = url_base + str(seed)
    print(url)

    # 请求数据，如果请求失败，停止此次任务，下次继续。
    headers['Cookie']=Cookie.format(bid = "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11)))
    # headers['Cookie'] = ''
    try: 
        response_movie = requests.get(url=url, headers=headers, timeout=timeout)
    except:
        exit()
    if response_movie.status_code != 200:
        print(response_movie)
        exit()

    # 初始化soup库
    soup = BeautifulSoup(response_movie.text, 'html.parser')

    # 解析并数据
    movie_info = analysis_movie(soup)
    csv_writer(str(seed),movie_info)

    # 更新数据库
    # 如果数据库中没有这个条目，那么将此条目写入数据库
    result = curs.execute(SELECT_ID.format(id = seed))
    if len(list(result))==0:
        curs.execute(INSERT.format(id = seed))
        connection.commit()

    # 更新数据库中此条目为已读
    curs.execute(UPDATE.format(id = seed))
    connection.commit()

    # 统计页面中的其他条目
    all_subject_id = find_movie_recommendations(soup)
    for id in all_subject_id:
        # 判断是否已经存在
        result = curs.execute(SELECT_ID.format(id = id))
        if len(list(result))==0:
            curs.execute(INSERT.format(id = id))
            connection.commit()
        else:
            pass # 如果已存在，那么不再添加



# 请求头
url_base = "https://movie.douban.com/subject/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
    'Cookie': "ll=\"118371\"; bid=ujBcNwnZ9Lc; __utmz=30149280.1668276173.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=b6acfc64c8d441ac-22b7559f40d80002:T=1668276176:RT=1668276176:S=ALNI_MZdL-d_l65y7cW4EOfY4WKGi83LKw; push_noty_num=0; push_doumail_num=0; __yadk_uid=3qqwL8vX4Y42dTT0SerwrQAVqnfcTES4; __utmv=30149280.6250; __gpi=UID=00000b7ae4562923:T=1668276176:RT=1668350550:S=ALNI_MaVl14ymNIBMp9Kma3BBYiS7-E2Cw; _pk_id.100001.8cb4=78c23fb0f9637844.1668306835.6.1668434978.1668350547.; _pk_ses.100001.8cb4=*; __utma=30149280.657680781.1668276173.1668350552.1668434981.12; __utmc=30149280; __utmt=1; __utmb=30149280.1.10.1668434981"
}
Cookie = "ll=\"118371\"; {bid:s}; __utmz=30149280.1668276173.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=b6acfc64c8d441ac-22b7559f40d80002:T=1668276176:RT=1668276176:S=ALNI_MZdL-d_l65y7cW4EOfY4WKGi83LKw; push_noty_num=0; push_doumail_num=0; __yadk_uid=3qqwL8vX4Y42dTT0SerwrQAVqnfcTES4; __utmv=30149280.6250; __gpi=UID=00000b7ae4562923:T=1668276176:RT=1668350550:S=ALNI_MaVl14ymNIBMp9Kma3BBYiS7-E2Cw; _pk_id.100001.8cb4=78c23fb0f9637844.1668306835.6.1668434978.1668350547.; _pk_ses.100001.8cb4=*; __utma=30149280.657680781.1668276173.1668350552.1668434981.12; __utmc=30149280; __utmt=1; __utmb=30149280.1.10.1668434981"

proxies = {
  'http': 'http://127.0.0.1:7890',
  'https': 'http://127.0.0.1:7890'
}

import time
connection, curs = init_database()
for i in range(200):
    # time.sleep(2)
    result = curs.execute("SELECT id, status  from MOVIE")
    message = "Number of items: " + str(len(list(result)))
    print(i, message)
    if i % 20 == 0 :
        email(message,'主题测试','发件人','收件人','mpf_npu@icloud.com')
    fetch_one_subject()


result = curs.execute("SELECT id, status  from MOVIE")
message = "Number of items: " + str(len(list(result)))
print(message)

		
						
# import sqlite3
# connection = sqlite3.connect('test.db')
# print ("数据库打开成功")
# c = connection.cursor()
# c.execute('''CREATE TABLE MOVIE
#        (ID INT PRIMARY KEY     NOT NULL,
#         STATUS            INT     NOT NULL);''')
# print ("数据表创建成功")
# connection.commit()
# connection.close()


# connection = sqlite3.connect('test.db')
# c = connection.cursor()
# print ("数据库打开成功")
# curs.execute("INSERT INTO MOVIE (ID,STATUS) VALUES (100, 0)")
# connection.commit()
# connection.close()



# result = curs.execute("SELECT id, status  from MOVIE")
# for row in result:
#    print("ID = ", row[0])
#    print("NAME = ", row[1])

# print ("数据操作成功")
# connection.close()
