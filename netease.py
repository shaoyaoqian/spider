
# 网易云爬虫，使用了NeteaseCloudMusicApi，文档参见：
# https://neteasecloudmusicapi.vercel.app
# 第三方API服务搭建在vercel上

import requests
import time, random
from loguru import logger

logger.add('my_log.log')

phone    = '15991859247'
password = 'a12345'
url_base = "https://neteaseapi.pengfeima.cn"

body = {
    'cookie': 'MUSIC_R_T=1458378773117; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/api/feedback; HTTPOnly;MUSIC_A_T=1458378730164; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/weapi/feedback; HTTPOnly;MUSIC_R_T=1458378773117; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/wapi/clientlog; HTTPOnly;MUSIC_A_T=1458378730164; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/api/clientlog; HTTPOnly;MUSIC_R_T=1458378773117; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/neapi/clientlog; HTTPOnly;MUSIC_R_T=1458378773117; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/openapi/clientlog; HTTPOnly;MUSIC_R_T=1458378773117; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/wapi/feedback; HTTPOnly;MUSIC_SNS=; Max-Age=0; Expires=Tue, 07 Feb 2023 07:04:16 GMT; Path=/;MUSIC_A_T=1458378730164; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/eapi/clientlog; HTTPOnly;MUSIC_R_T=1458378773117; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/eapi/feedback; HTTPOnly;MUSIC_A_T=1458378730164; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/neapi/feedback; HTTPOnly;__csrf=150aeebc0a75d90aa2cbf1eab675221a; Max-Age=1296010; Expires=Wed, 22 Feb 2023 07:04:26 GMT; Path=/;;MUSIC_R_T=1458378773117; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/api/clientlog; HTTPOnly;MUSIC_A_T=1458378730164; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/neapi/clientlog; HTTPOnly;MUSIC_A_T=1458378730164; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/eapi/feedback; HTTPOnly;MUSIC_A_T=1458378730164; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/wapi/feedback; HTTPOnly;MUSIC_A_T=1458378730164; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/wapi/clientlog; HTTPOnly;MUSIC_R_T=1458378773117; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/weapi/clientlog; HTTPOnly;MUSIC_R_T=1458378773117; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/neapi/feedback; HTTPOnly;MUSIC_A_T=1458378730164; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/openapi/clientlog; HTTPOnly;MUSIC_A_T=1458378730164; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/api/feedback; HTTPOnly;MUSIC_R_T=1458378773117; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/weapi/feedback; HTTPOnly;MUSIC_R_T=1458378773117; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/eapi/clientlog; HTTPOnly;MUSIC_U=9e989f17616003dac853e13d9fe8b598fbe7ddbc550303f83e4411627598e2851e8907c67206e1ed57d74b51b574d70cbe24b29a98079908d4203591aaeb3f3b350fc70521cd88eca0d2166338885bd7; Max-Age=15552000; Expires=Sun, 06 Aug 2023 07:04:16 GMT; Path=/; HTTPOnly;MUSIC_A_T=1458378730164; Max-Age=2147483647; Expires=Sun, 25 Feb 2091 10:18:23 GMT; Path=/weapi/clientlog; HTTPOnly'
}

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
    
    def login_qr(self):
        # 获取二维码的key
        url = url_base+"/login/qr/key"
        params = { }
        response = requests.get(url,params=params)
        logger.info("response.url: {}".format(response.url))
        logger.info("key: {}".format(response.json()['data']['unikey']))
        key = response.json()['data']['unikey']
        # 获取二维码图片
        url = url_base+"/login/qr/create?key={}&qrimg=true".format(key)
        response = requests.get(url,params=params)
        logger.info("{}".format(response.json()['data']['qrimg']))
        # 保存二维码图片
        import base64        
        request_base64=response.json()['data']['qrimg'][21:]
        imgdata = base64.b64decode(request_base64)
        with open("NeteaseQR.png","wb") as fh:
            fh.write(imgdata)
        # 等待扫描二维码
        time.sleep(100)
        # 打印cookie
        url = url_base+"/login/qr/check?key={}".format(key)
        response = requests.get(url,params=params)
        logger.info("{}".format(response.json()['cookie']))
        return response

    def singer(self, id = "11972054"):
        """
        获取歌手信息
        """
        url = url_base + "/artist/desc"
        params = {
            'id':id
        }
        response = requests.get(url,params=params, data=body)
        logger.info("response.url: {}".format(response.url))
        return response

    def singer_details(self, id = "11972054"):
        url = url_base + "/artist/detail"
        params = {
            'id':id
        }
        response = requests.get(url,params=params, data=body)
        logger.info("response.url: {}".format(response.url))
        return response

    def album(self, id = "32311"):
        url = url_base + "/album"
        params = {
            'id':id
        }
        response = requests.get(url,params=params, data=body)
        logger.info("response.url: {}".format(response.url))
        return response

    def singer_albums(self, id = "11972054", limit=5, offset=0):
        url = url_base + "/artist/album"
        params = {
            'id':id,
            'limit':limit,
            'offset':offset
        }
        response = requests.get(url,params=params, data=body)
        logger.info("response.url: {}".format(response.url))
        return response

    def song_lyric(self, id = '436147423'):
        url = url_base + "/lyric"
        params = {
            'id':id
        }
        response = requests.get(url,params=params, data=body)
        logger.info("response.url: {}".format(response.url))
        return response

    def song_detail(self, id = '436147423'):
        url = url_base + "/song/detail"
        params = {
            'ids':id
        }
        response = requests.get(url,params=params, data=body)
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
        response = requests.get(url,params=params, data=body)
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


NA = NeteaseAPI()

def song_download_entirely(id="28660001",path='songs'):
    result = NA.song(id=id)
    result = NA.song_detail(id=id)
    song_name = result.json()['songs'][0]['name']
    singer_name = [song_artist["name"] for song_artist in result.json()['songs'][0]["ar"]]
    singer_name = ", ".join(singer_name)
    # 保存歌曲信息
    with open(path+'/'+"-".join([id,song_name,singer_name])+'.json', 'wb') as f:
        f.write(result.content)
    # 下载封面
    response = requests.get(result.json()['songs'][0]['al']['picUrl'])
    with open(path+'/'+id+'.png', 'wb') as f:
        f.write(response.content)
    # 下载歌词
    result = NA.song_lyric(id=id)
    with open(path+'/'+id+'.lrc', 'w') as f:
        f.write(result.json()['lrc']['lyric'])
    # 下载歌曲
    result = NA.song_download(id=id,filename=path+'/'+id)
    cdn_base = "https://raw.githubusercontent.com/shaoyaoqian/spider/main/"+path
    song_info = {}
    song_info['name'] = song_name
    song_info['artist'] = singer_name
    song_info['info'] = cdn_base+"-".join([id,song_name,singer_name])+'.json'
    song_info['audio'] = cdn_base+id+".mp3"
    song_info['cover'] = cdn_base+id+".png"
    song_info['lrc'] = cdn_base+id+".lrc"
    song_info['id'] = id
    return song_info

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

# 下载一张专辑
def download_album(album_id = "35069014", directory = "songs/albums/", time_sleep=30):
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
    songs_info = []
    path = directory+album_name+"/"
    import os
    if not os.path.isdir(path):
        os.makedirs(path)
    for song in songs:
        logger.info('sleeping...')
        time.sleep(time_sleep*random.random())
        # 单曲id
        song_id = str(song["id"])
        song_info = song_download_entirely(id=song_id, path=path)
        songs_info.append(song_info)
    with open (path+'info.json','w') as f:
        import json
        json.dump(songs_info,f)


        
# 下载一张专辑
album_id = "34535673"
download_album(album_id = album_id)

# 下载一位歌手的所有专辑
# # 歌手ID（默认谢春花）
# singer = "10557"  
# # 收集歌手所有专辑ID
# album_ids = collect_singer_albums(id = singer)
# # 遍历所有专辑
# for album_id in album_ids:
#     download_album(album_id = album_id)




