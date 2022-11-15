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
