import requests
from bs4 import BeautifulSoup
import re
import sqlite3


# import .myemail
from smtplib import SMTP_SSL
from email.mime.text import MIMEText


# 导入CSV安装包
import csv



# 请求头
url_base = "https://movie.douban.com/subject/"
headers = {
    "Cookie": "ll=\"118371\"; bid=ujBcNwnZ9Lc; __utmc=30149280; __utmz=30149280.1668276173.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=223695111; __gads=ID=b6acfc64c8d441ac-22b7559f40d80002:T=1668276176:RT=1668276176:S=ALNI_MZdL-d_l65y7cW4EOfY4WKGi83LKw; _vwo_uuid_v2=DE24A7FF90CBF420B2CC3B2D77FAA2BEB|e643833b49240612b8cdb378253657a3; push_noty_num=0; push_doumail_num=0; __gpi=UID=00000b7ae4562923:T=1668276176:RT=1668306854:S=ALNI_MaVl14ymNIBMp9Kma3BBYiS7-E2Cw; __yadk_uid=agxs4UBjjo2L3vsmY17qHDiD1lZjFxkS; __utma=30149280.657680781.1668276173.1668310210.1668314045.4; __utmt=1; ap_v=0,6.0; dbcl2=\"62503351:VHCrjpteg4M\"; ck=4zhh; __utmv=30149280.6250; __utmb=30149280.15.10.1668314045; __utma=223695111.1099428811.1668276173.1668310213.1668314289.4; __utmb=223695111.0.10.1668314289; __utmz=223695111.1668314289.4.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1668314289%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=2828da9b05475a90.1668276172.4.1668314289.1668310242.; _pk_ses.100001.4cf6=*; report=ref=%2F&from=mv_a_pst",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52"
}




# 数据库代码
connection = sqlite3.connect('test.db')
curs = connection.cursor()
INSERT = "INSERT INTO MOVIE (ID,STATUS) VALUES ({id:d}, 0)"
SELECT_ID = "SELECT id, status from MOVIE where id={id:d}"
SELECT_STATUS = "SELECT id, status from MOVIE where status={status:d}"
UPDATE = "UPDATE MOVIE set status = 1 where ID={id:d}"



seed = 1292403
url = url_base + str(seed)
response_movie = requests.get(url=url, headers=headers, timeout=5)
soup = BeautifulSoup(response_movie.text, 'html.parser')
voter = soup.find(name='span', attrs={"property" :"v:votes"}).string
kinds_temp    = soup.findAll(name='span', attrs={"property" :"v:genre"})
kinds_temp[-1].next_sibling.next_sibling.next_sibling.next_sibling
