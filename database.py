import sqlite3
import csv


def init_database(path='test.db'):
    # 数据库代码
    connection = sqlite3.connect(path)
    curs = connection.cursor()
    return connection, curs

def create_database():
    pass


# 数据库参数
INSERT = "INSERT INTO MOVIE (ID,STATUS) VALUES ({id:d}, 0)"
SELECT_ID = "SELECT id, status from MOVIE where id={id:d}"
SELECT_STATUS = "SELECT id, status from MOVIE where status={status:d}"
UPDATE = "UPDATE MOVIE set status = 1 where ID={id:d}"



# 保存数据
# ID,标题,年份,副标题（国家/类型/导演/演员）,评分,海报,评分人数
#
# 创建csv文件
def create_csv(path = 'movie.csv'):
    f = open(path,'w',encoding='utf-8')
    csv_writer = csv.writer(f)
    csv_writer.writerow(['ID','标题','年份','副标题（国家/类型/导演/演员）', '评分', '海报', '评分人数'])
    f.close()
#
def csv_writer(id, movie_info, path = 'movie.csv'):
    title, year, subtitle, rating, poster, voter = movie_info
    # 1. 创建文件对象
    f = open(path,'a+',encoding='utf-8')
    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)
    # 4. 写入csv文件内容
    csv_writer.writerow([id, title, year, subtitle, rating, poster, voter])
    # 5. 关闭文件
    f.close()
