
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

    def song_download(self, id = '1834270728', level = 'standard'):
        result = self.song(id=id,level=level)
        # TODO : 判断歌曲是否能下载
        url_song =  result.json()['data'][0]['url']
        response = requests.get(url_song)
        # TODO : 文件名需要外部传入，后缀需要从url解析
        filename = 'a.mp3'
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(response.url)
        return response


# test 
NA = NeteaseAPI()
# result = NA.login()
# result = NA.singer()
# result = NA.singer_details()
# result = NA.singer_albums()
# result = NA.song()
result = NA.song_download(id="1309394503")

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

