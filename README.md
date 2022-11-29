# spider
#### TODO for douban spider: 
- [ ] [使用代理](https://blog.csdn.net/qq1261275789/article/details/111408400)
- [x] 详细解析电影项目的详细信息，写入csv文件
- [ ] [爬取电影的评论](https://blog.csdn.net/qq_45720042/article/details/118833756)
- [ ] 设立独立的sql数据库，而不是写在 GitHub仓库中
- [x] [时间设置](https://blog.csdn.net/Ximerr/article/details/123501772)，目前是每10分钟爬取一次数据。
- [x] 发送邮件提醒，目前是启动的时候发送一次，每爬取20条消息也会法送一次
- [ ] 使用scrapy框架

#### TODO for netease spider
- [ ] 使用scrapy框架
- [x] 使用vercel搭建服务，访问地址为https://netease.pengfeima.cn
- [x] 爬取一个歌手的所有歌曲：歌手 => 专辑 => 歌曲

##### 用eyeD3写入 mp3 标签 
# 参考：https://blog.csdn.net/lly1122334/article/details/119570021

import eyed3
audiofile = eyed3.load('阿的说法饿.mp3')
audiofile.tag.title = '晴天'                   # 标题          ok
audiofile.tag.artist = '周杰伦'                # 艺术家         ok
audiofile.tag.album = '叶惠美'                 # 唱片集         ok
audiofile.tag.recording_date = '2003'         # 年份           ok
audiofile.tag.track_num = 3                   # 音轨号         ok
audiofile.tag.genre = 'Pop'                   # 流派           X
audiofile.tag.comments.set('Hello World!')    # 注释(专辑描述)  ok
audiofile.tag.album_artist = '周杰伦'          # 专辑集艺术家    ok
audiofile.tag.composer = '周杰伦'              # 作曲家          X
audiofile.tag.aa = 3                          # CD号 光盘编号   X
audiofile.tag.images.set(
   type_=3, 
   img_data=open('RE4wEas.jpeg', 'rb').read(), 
   mime_type='image/jpeg')                      # 封面(专辑封面) ok
audiofile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')



清空Git仓库所有历史，减少仓库体积的方法：
```bash
git checkout --orphan latest_branch
git add -A
git commit -am "commit"
git branch -D main
git branch -m main
git push -f origin main
```


# 文本生成 https://zhuanlan.zhihu.com/p/188446640



name: String, 歌曲标题
id: u64, 歌曲ID
pst: 0，功能未知
t: enum,
  0: 一般类型
  1: 通过云盘上传的音乐，网易云不存在公开对应
    如果没有权限将不可用，除了歌曲长度以外大部分信息都为null。
    可以通过 `/api/v1/playlist/manipulate/tracks` 接口添加到播放列表。
    如果添加到“我喜欢的音乐”，则仅自己可见，除了长度以外各种信息均为未知，且无法播放。
    如果添加到一般播放列表，虽然返回code 200，但是并没有效果。
    网页端打开会看到404画面。
    属于这种歌曲的例子: https://music.163.com/song/1345937107
  2: 通过云盘上传的音乐，网易云存在公开对应
    如果没有权限则只能看到信息，但无法直接获取到文件。
    可以通过 `/api/v1/playlist/manipulate/tracks` 接口添加到播放列表。
    如果添加到“我喜欢的音乐”，则仅自己可见，且无法播放。
    如果添加到一般播放列表，则自己会看到显示“云盘文件”，且云盘会多出其对应的网易云公开歌曲。其他人看到的是其对应的网易云公开歌曲。
    网页端打开会看到404画面。
    属于这种歌曲的例子: https://music.163.com/song/435005015
ar: Vec<Artist>, 歌手列表
alia: Vec<String>,
  别名列表，第一个别名会被显示作副标题
  例子: https://music.163.com/song/536623501
pop: 小数，常取[0.0, 100.0]中离散的几个数值, 表示歌曲热度
st: 0: 功能未知
rt: Option<String>, None、空白字串、或者类似`600902000007902089`的字符串，功能未知
fee: enum,
  0: 免费或无版权
  1: VIP 歌曲
  4: 购买专辑
  8: 非会员可免费播放低音质，会员可播放高音质及下载
  fee 为 1 或 8 的歌曲均可单独购买 2 元单曲
v: u64, 常为[1, ?]任意数字, 代表歌曲当前信息版本
version: u64, 常为[1, ?]任意数字, 代表歌曲当前信息版本
crbt: Option<String>, None或字符串表示的十六进制，功能未知
cf: Option<String>, 空白字串或者None，功能未知
al: Album, 专辑，如果是DJ节目(dj_type != 0)或者无专辑信息(single == 1)，则专辑id为0
dt: u64, 歌曲时长
sq: Option<Quality>, 无损质量文件信息
h: Option<Quality>, 高质量文件信息
m: Option<Quality>, 中质量文件信息
l: Option<Quality>, 低质量文件信息
a: Option<?>, 常为None, 功能未知
cd: Option<String>, None或如"04", "1/2", "3", "null"的字符串，表示歌曲属于专辑中第几张CD，对应音频文件的Tag
no: u32, 表示歌曲属于CD中第几曲，0表示没有这个字段，对应音频文件的Tag
rtUrl: Option<String(?)>, 常为None, 功能未知
rtUrls: Vec<String(?)>, 常为空列表, 功能未知
djId: u64,
  0: 不是DJ节目
  其他：是DJ节目，表示DJ ID
copyright: u32, 0, 1, 2: 功能未知
s_id: u64, 对于t == 2的歌曲，表示匹配到的公开版本歌曲ID
mark: u64, 功能未知
originCoverType: enum
  0: 未知
  1: 原曲
  2: 翻唱
originSongSimpleData: Option<SongSimpleData>, 对于翻唱曲，可选提供原曲简单格式的信息
single: enum,
  0: 有专辑信息或者是DJ节目
  1: 未知专辑
noCopyrightRcmd: Option<NoCopyrightRcmd>, None表示可以播，非空表示无版权
mv: u64, 非零表示有MV ID
rtype: 常为0，功能未知
rurl: Option<String(?)>, 常为None，功能未知
mst: u32, 偶尔为0, 常为9，功能未知
cp: u64, 功能未知
publishTime: i64, 毫秒为单位的Unix时间戳
pc: 云盘歌曲信息，如果不存在该字段，则为非云盘歌曲