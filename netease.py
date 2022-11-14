# https://neteasecloudmusicapi.vercel.app
# 网易云爬虫使用了NeteaseCloudMusicApi
# 调用API的两种方法:
#
# 方法一
import requests
response = requests.get('http://localhost:3000/song/url?id=208891')
#
#
# 方法二
import requests
data = {
    'id': '436147423'
}
response = requests.get('http://localhost:3000/download/song/url', params=data)

with open('a.mp3', 'wb') as f:
    f.write(response.content)

# 我想用爬