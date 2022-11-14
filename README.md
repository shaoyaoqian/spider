# spider
my spider
TODO: 
1. [使用代理](https://blog.csdn.net/qq1261275789/article/details/111408400)
2. 增加电影项目的详细信息，写入csv文件
    打算爬去下面这些数据。
    - id	        3549046931
    - title	     天生杀人狂
    - subtitle   1994 / 美国 / 剧情 动作 犯罪 / 奥利佛·斯通 / 伍迪·哈里森 朱丽叶- 特·刘易斯
    - poster     https://img9.doubanio.com/view/photo/m_ratio_poster/- public/p1640827366.jpg
    - pubdate  1994-08-26(美国)
    - url	        https://movie.douban.com/subject/1292229/
    - rating       7.9
    - genres	 剧情,动作,犯罪
3. [爬取电影的评论](https://blog.csdn.net/qq_45720042/article/details/118833756)
4. 设立独立的数据库
5. [时间设置](https://blog.csdn.net/Ximerr/article/details/123501772)
6. 发送邮件提醒



由于数据库代码是二进制文件，因此每次提交代码，数据库文件都会完整保存下来。我想定时清空仓库历史:
```bash
git checkout --orphan latest_branch
git add -A
git commit -am "commit"
git branch -D main
git branch -m main
git push -f origin main
```




