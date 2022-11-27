
# 网易云爬虫，使用了NeteaseCloudMusicApi，文档参见：
# https://neteasecloudmusicapi.vercel.app
# 第三方API服务搭建在vercel上

import requests

phone    = '15991859247'
password = 'a12345'
url_base = "https://netease.pengfeima.cn"

class NeteaseAPI():
    def login(self):
        url = url_base+"/login/cellphone"
        params = {
            'phone': phone,
            'password': password
        }
        response = requests.get(url,params=params)
        print(response.url)
        return response

    def singer(self, id = "11972054"):
        url = url_base + "/artist/desc"
        params = {
            'id':id
        }
        response = requests.get(url,params=params)
        print(response.url)
        return response

    def singer_details(self, id = "11972054"):
        url = url_base + "/artist/detail"
        params = {
            'id':id
        }
        response = requests.get(url,params=params)
        print(response.url)
        return response

    def album(self, id = "32311"):
        url = url_base + "/album"
        params = {
            'id':id
        }
        response = requests.get(url,params=params)
        print(response.url)
        return response

    def singer_albums(self, id = "11972054", limit=5, offset=0):
        url = url_base + "/artist/album"
        params = {
            'id':id,
            'limit':limit,
            'offset':offset
        }
        response = requests.get(url,params=params)
        print(response.url)
        return response

    def song(self, id = '436147423', level = 'standard'):
        # url = url_base + "/song/url"          # old API
        url = url_base + "/song/url/v1"
        params = {
            'id'    : id,
            'level' : level  
            # standard => 标准
            # higher   => 较高
            # exhigh   => 极高
            # lossless => 无损 
            # hires    => Hi-Res
        }
        response = requests.get(url,params=params)
        print(response.url)
        return response

    def song_download(self, id = '1834270728', level = 'standard', filename = "filename"):
        result = self.song(id=id,level=level)
        # TODO : 判断歌曲是否能下载
        url_song =  result.json()['data'][0]['url']
        appendix = '.' + url_song.split(".")[-1]
        response = requests.get(url_song)
        # TODO : 文件名需要外部传入，后缀需要从url解析
        with open(filename + appendix, 'wb') as f:
            f.write(response.content)
        print(response.url)
        return filename + appendix


# test 
NA = NeteaseAPI()
# result = NA.login()
# result = NA.singer()
# result = NA.singer_details()
# result = NA.album()
# result = NA.singer_albums()
# result = NA.song()
# result = NA.song_download(id="1309394503")

# 从歌手id收集专辑
# id = "101988"
# result = NA.singer_albums(id = id)
# albumSize = result.json()['artist']['albumSize'] # 专辑数量
# print(albumSize)
# for i in range(albumSize//30+1):
#     offset=30*i
#     limit = 30
#     result = NA.singer_albums(id = id, limit=limit, offset=offset)
#     for j in range(min(30, albumSize-offset)):
#         print(result.json()['hotAlbums'][j]['id'])  # 第j张专辑的id



# 用eyeD3写入 mp3 标签 
# 参考：https://blog.csdn.net/lly1122334/article/details/119570021

import eyed3
audiofile = eyed3.load('阿的说法饿.mp3')
audiofile.tag.title = '晴天'                 # 标题 ok
audiofile.tag.artist = '周杰伦'              # 艺术家
audiofile.tag.album = '叶惠美'               # 唱片集 ok
# audiofile.tag.recording_date = '2003'       # 年份   ok
# audiofile.tag.track_num = 3                 # 音轨号 ok
# audiofile.tag.genre = 'Pop'                 # 流派   X
# audiofile.tag.comments.set('Hello World!')  # 注释(专辑描述) ok
# audiofile.tag.album_artist = '周杰伦'        # 专辑集艺术家 ok
# audiofile.tag.composer = '周杰伦'            # 作曲家     X
# audiofile.tag.aa = 3                        # CD号,光盘编号 X
# audiofile.tag.images.set(type_=3, img_data=open('RE4wEas.jpeg', 'rb').read(), mime_type='image/jpeg')  # 封面(专辑封面) ok
# audiofile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')

import eyed3, time

def download_album(album_id = "73256816", directory = "songs/"):
    result = NA.album(album_id)
    # 出版时间
    timeStamp = result.json()["album"]["publishTime"]
    timeArray = time.localtime(timeStamp/1000)
    album_time = time.strftime("%Y%m%d", timeArray)
    # 专辑名称
    album_name = result.json()["album"]["name"]
    print(album_name)
    # 专辑描述
    album_description = result.json()["album"]["description"]
    print(album_description)
    # 专辑封面
    album_picture_url = result.json()["album"]["picUrl"]
    print(album_picture_url)
    # 专辑集艺术家(可能有几个)
    album_artists = [album_artist["name"] for album_artist in result.json()["album"]["artists"]]
    # 单曲标题
    songs = result.json()["songs"]
    for song in songs:
        # 单曲id
        song_id = song["id"]
        # 单曲名
        song_name = song["name"]
        # 音轨号
        song_track_num = song["no"]
        # 单曲艺术家
        song_artists = [song_artist["name"] for song_artist in song["ar"]]
        song_info = [", ".join(song_artists),album_name,song_name]
        song_filename = " - ".join(song_info)
        print(song_filename)
        # 下载单曲
        song_filename_appendix = NA.song_download(id = song_id, filename = directory + song_filename)
        audiofile = eyed3.load(song_filename_appendix)
        audiofile.tag.title = song_name                       # 标题 ok
        audiofile.tag.artist = ", ".join(song_artists)        # 艺术家
        audiofile.tag.album = album_name                      # 唱片集 ok
        audiofile.tag.release_date = album_time                 # 年份   ok
        audiofile.tag.track_num = song_track_num              # 音轨号 ok
        audiofile.tag.comments.set(album_description)         # 注释(专辑描述) ok
        audiofile.tag.album_artist = ", ".join(album_artists)       # 专辑集艺术家 ok
        audiofile.tag.images.set(type_=3, img_data=requests.get(album_picture_url).content, mime_type='image/jpeg')  # 封面(专辑封面) ok
        audiofile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')

        


download_album()

import time



