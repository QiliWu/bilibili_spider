# bilibili_spider

分别使用requests, scrapy,scrapy_redis（分布式）实现的三个关于B站用户信息的网络爬虫, 爬取B站用户注册信息（昵称，id, 头像，等级，注册时间, 关注者等），将 数据存储到mysql中。

项目具体信息：

    1. 爬虫逻辑
    分析网站发现，B站用户id都是顺序递增的数字，页面的用户信息是通过ajax异步加载json数据实现的。所以POST方式请求json文件对应的url，并传入用户id，即可获得包含用户信息的json数据。
    通过自己新注册一个账户，获取最新的id,如3244329271，则可以理解为截止到我注册那一刻，B站共有3244329270个注册用户。通过迭代id值(0-3244329270),就可以获取b站所有用户的注册信息。

    2. 分布式设置
    使用scrapy-redis提供的调度器和去重器，将带爬取的request和已经爬取的url分别保存到redis数据库中，各个机器上的爬虫都从同一redis数据库中获取数据，实现集中管理。

    3. 底层存储设置
    爬取结果分别存入制定MySQL数据库的数据表中。
    使用了twisted提供的adbapi包，将数据插入到数据库变为一个异步过程。

    4. 避免爬虫被禁的策略
    实现了一个RandomUserAgentMiddleware， 可以不停的改变user-agent
    实现了一个ProxyMiddleware，可以不停地改变ip代理。
    修改headers信息
    控制并发数
   
 需要使用的库： scrapy, scrapy-redis,requests, mysqldb, redis, fake-useragent,


