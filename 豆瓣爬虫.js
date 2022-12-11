// undici 用法：https://github.com/nodejs/undici

const { request } = require('undici');
const {
  DOUBAN_API_HOST = 'frodo.douban.com',
  DOUBAN_API_KEY = '0ac44ae016490db2204ce0a042db2916',
  AUTH_TOKEN,
} = process.env;

const url = `https://${DOUBAN_API_HOST}/api/v2/user/lizheming/interests`;
const params = new URLSearchParams({
  type: 'movie',
  status: 'done',
  count: 50,
  start: 0,
  apiKey: DOUBAN_API_KEY
});

const { interests } = await request(url + '?' + params.toString(), {
  headers: {
    host: DOUBAN_API_HOST,
    authorization: AUTH_TOKEN ? 'Bearer ' + AUTH_TOKEN : '',
    'user-agent': 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001023) NetType/WIFI Language/zh_CN',
    referer: 'https://servicewechat.com/wx2f9b06c1de1ccfca/84/page-frame.html'
  }
}).then(({body}) => body.json());



// flyio 版本

DOUBAN_API_HOST = 'frodo.douban.com',
DOUBAN_API_KEY = '0ac44ae016490db2204ce0a042db2916',
AUTH_TOKEN = ''

const params = new URLSearchParams({
  // type: 'movie',
  // status: 'done',
  // count: 50,
  // start: 0,
  apiKey: DOUBAN_API_KEY
});
/

// const url_base = `https://${DOUBAN_API_HOST}/api/v2/user/lizheming/interests`;
const url_base = "https://frodo.douban.com/api/v2/subject_collection/movie_showing/items?apiKey=054022eaeae0b00e0fc068c0c0a2102a&count=30"
const url = url_base + '?' + params.toString();

var fly=require("flyio")
let a = fly.request(url,params,{
  headers: {
    host: DOUBAN_API_HOST,
    authorization: AUTH_TOKEN ? 'Bearer ' + AUTH_TOKEN : '',
    'user-agent': 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001023) NetType/WIFI Language/zh_CN',
    referer: 'https://servicewechat.com/wx2f9b06c1de1ccfca/84/page-frame.html'
  }
}).then(function (response) {
    console.log(response)
    console.log(response['data']['count']);
    return response['data']['count'];
})

// 网易云音乐
var fly=require("flyio")
url_base = "https://netease.pengfeima.cn"

const NeteaseMusicAPI = {
  download_lyric: (id) => {
    console.log('Downloading lyric...', id)    
    url = url_base + "/lyric"
    params = {
        'id':id
    }
    
    // 成功的回调函数
    function download_lyric_success(result) {
      console.log("Downloaded successfully.");
      return result;
    }
    
    // 失败的回调函数
    function download_lyric_fail(error) {
      console.loga("Failed to download." + error);
    }
    
    let result = fly.request(url, params).then(download_lyric_success,download_lyric_fail);
    let data = await result.then((result) => {return result['data']});
    return data;
  }
}
id = '436147423';
NeteaseMusicAPI.download_lyric(id)


    def song_lyric(self, id = '436147423'):

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
id="453927771"
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


url_base = "https://raw.githubusercontent.com/shaoyaoqian/images-1/main/music/"


print("audio: \'"+url_base+id+".mp3\',")
print("cover: \'"+url_base+id+".png\',")
print("lrc: \'"+url_base+id+".lrc\',")
print("name: \'"+song_name+'\',')
print("artist: \'"+singer_name+'\',')