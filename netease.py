
# 网易云爬虫，使用了NeteaseCloudMusicApi，文档参见：
# https://neteasecloudmusicapi.vercel.app
# 第三方API服务搭建在vercel上

import requests
import eyed3, time, random
from loguru import logger

logger.add('my_log.log')

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
        logger.info("response.url: {}".format(response.url))
        return response

    def singer(self, id = "11972054"):
        url = url_base + "/artist/desc"
        params = {
            'id':id
        }
        response = requests.get(url,params=params)
        logger.info("response.url: {}".format(response.url))
        return response

    def singer_details(self, id = "11972054"):
        url = url_base + "/artist/detail"
        params = {
            'id':id
        }
        response = requests.get(url,params=params)
        logger.info("response.url: {}".format(response.url))
        return response

    def album(self, id = "32311"):
        url = url_base + "/album"
        params = {
            'id':id
        }
        response = requests.get(url,params=params)
        logger.info("response.url: {}".format(response.url))
        return response

    def singer_albums(self, id = "11972054", limit=5, offset=0):
        url = url_base + "/artist/album"
        params = {
            'id':id,
            'limit':limit,
            'offset':offset
        }
        response = requests.get(url,params=params)
        logger.info("response.url: {}".format(response.url))
        return response

    def song_lyric(self, id = '436147423'):
        url = url_base + "/lyric"
        params = {
            'id':id
        }
        response = requests.get(url,params=params)
        logger.info("response.url: {}".format(response.url))
        return response

    def song_detail(self, id = '436147423'):
        url = url_base + "/song/detail"
        params = {
            'ids':id
        }
        response = requests.get(url,params=params)
        logger.info("response.url: {}".format(response.url))
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
        logger.info("response.url: {}".format(response.url))
        return response

    def song_download(self, id = '1834270728', level = 'standard', filename = "filename"):
        result = self.song(id=id,level=level)
        url_song =  result.json()['data'][0]['url']
        logger.info("url_song: {}".format(url_song))
        logger.info("song_path: {}".format(filename))
        # 判断歌曲是否能下载
        if url_song == None :
            appendix = ".txt"
            with open(filename + appendix, 'wb') as f:
                f.write(filename.encode())
        else :
            appendix = '.' + url_song.split(".")[-1]
            response = requests.get(url_song)
            # 文件名外部传入，后缀从url解析
            with open(filename + appendix, 'wb') as f:
                f.write(response.content)
            logger.info("response.url: {}".format(response.url))
        return filename + appendix


# test 
NA = NeteaseAPI()
# result = NA.login()
# result = NA.singer()
# result = NA.singer_details()
# result = NA.album()
# result = NA.singer_albums()
id="1974443814"
result = NA.song(id=id)
result = NA.song_detail(id=id)

song_name = result.json()['songs'][0]['name']
singer_name = result.json()['songs'][0]['ar'][0]['name']

with open("-".join([id,song_name,singer_name])+'.txt', 'wb') as f:
    f.write(result.content)

response = requests.get(result.json()['songs'][0]['al']['picUrl'])
with open(id+'.png', 'wb') as f:
    f.write(response.content)

result = NA.song_lyric(id=id)
with open(id+'.lrc', 'w') as f:
    f.write(result.json()['lrc']['lyric'])

result = NA.song_download(id=id,filename=id)

# 从歌手id收集专辑
def collect_singer_albums(id = "101988"):
    album_ids = []
    result = NA.singer_albums(id = id)
    albumSize = result.json()['artist']['albumSize'] # 专辑数量
    logger.info("albumSize: {}".format(albumSize))
    for i in range(albumSize//30+1):
        offset=30*i
        limit = 30
        result = NA.singer_albums(id = id, limit=limit, offset=offset)
        for j in range(min(30, albumSize-offset)):
            # 第j张专辑的id
            album_ids.append(result.json()['hotAlbums'][j]['id'])
    
    logger.info("album_ids: ")
    logger.info(album_ids)
    return(album_ids)


def download_album(album_id = "35069014", directory = "songs/", time_sleep=30):
    result = NA.album(album_id)
    # 出版时间
    timeStamp = result.json()["album"]["publishTime"]
    timeArray = time.localtime(timeStamp/1000)
    album_time = time.strftime("%Y", timeArray)
    logger.info("album_time: {}", album_time)
    # 专辑名称
    album_name = result.json()["album"]["name"]
    # 专辑描述
    album_description = result.json()["album"]["description"]
    # 专辑封面
    album_picture_url = result.json()["album"]["picUrl"]
    logger.info(album_name, album_time, album_picture_url, album_description)
    # 专辑集艺术家(可能有几个)
    album_artists = [album_artist["name"] for album_artist in result.json()["album"]["artists"]]
    # 单曲标题
    songs = result.json()["songs"]
    for song in songs:
        logger.info('sleeping...')
        time.sleep(time_sleep*random.random())
        # 单曲id
        song_id = song["id"]
        # 单曲名
        song_name = song["name"]
        # 音轨号
        song_track_num = 0 if song["no"] != None else song["no"]
        # 单曲艺术家
        song_artists = [song_artist["name"] for song_artist in song["ar"]]
        song_info = [", ".join(song_artists),album_name,song_name]
        song_filename = " - ".join(song_info)
        logger.info('song_filename: {}'.format(song_filename))
        # 下载单曲
        song_filename_appendix = NA.song_download(id = song_id, filename = directory + song_filename)
        logger.info("song_filename_appendix: {}", song_filename_appendix)
        # 如果下载了mp3结尾的或者flac结尾的文件，那么写入歌曲标签。
        if song_filename_appendix.split(".")[-1] in ['mp3']:
            audiofile = eyed3.load(song_filename_appendix)
            audiofile.tag.title = song_name                       # 标题 ok
            audiofile.tag.artist = ", ".join(song_artists)        # 艺术家
            audiofile.tag.album = album_name                      # 唱片集 ok
            audiofile.tag.recording_date = album_time                 # 年份   ok
            audiofile.tag.track_num = song_track_num              # 音轨号 ok
            audiofile.tag.album_artist = ", ".join(album_artists)       # 专辑集艺术家 ok
            audiofile.tag.images.set(type_=3, img_data=requests.get(album_picture_url).content, mime_type='image/jpeg')  # 封面(专辑封面) ok
            audiofile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')

        

# download_album(album_id = "34535673",time_sleep=0)

# # 歌手ID（默认谢春花）
# singer = "10557"  
# # 收集歌手所有专辑ID
# album_ids = collect_singer_albums(id = singer)
# # 遍历所有专辑
# for album_id in album_ids:
#     download_album(album_id = album_id)




