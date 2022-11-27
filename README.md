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
