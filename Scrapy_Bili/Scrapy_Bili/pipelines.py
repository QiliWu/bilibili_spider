# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapybiliPipeline(object):
    def process_item(self, item, spider):
        return item


import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline


class MysqlTwistedPipeline(object):
    # 通过twisted实现数据库的异步操作
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 从settings获取参数
        dbparams = dict(
            host='127.0.0.1',
            user='root',
            password='password',
            database='bili',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
            # 注意，这里的变量名一定要与connect函数中的参数名一样
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入 变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item)
        return item

    # 添加一个处理异步插入时出现的异常错误的函数
    def handle_error(self, failure, item):
        print(failure)

    def do_insert(self, cursor, item):
        # 从item类中调用定制的insert_sql, params
        insert_sql = """
                    INSERT INTO users_info(home_url, mid, `name`, face_img, curr_level,
                    sex, regtime, follower, following)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
        params = (item['home_url'], item['mid'], item['name'], item['face_img'],item['curr_level'],
        item['sex'], item['regtime'], item['follower'], item['following'])
        cursor.execute(insert_sql, params)
        print('成功抓取第 {0} 条用户数据'.format(item['mid']))

class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='password',
            database='bili')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
                            INSERT INTO users_info(home_url, mid, `name`, face_img, curr_level,
                            sex, regtime, follower, following)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
        params = (item['home_url'], item['mid'], item['name'], item['face_img'], item['curr_level'],
                  item['sex'], item['regtime'], item['follower'], item['following'])
        self.cursor.execute(insert_sql, params)
        self.conn.commit()
        print('成功抓取第 {0} 条用户数据'.format(item['mid']))

    def spider_closed(self, spider):
        self.conn.close()

#自定义一个图片处理管道文件, 使其产生front_image_path字段
class ArticleimagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        # 先用pass在这里设断点，获得results的格式
        # results = [(True, {'url': 'http://wx2.sinaimg.cn/large/7cc829d3gy1fptsk9tvx8j20go0b441z.jpg',
        #                         'path': 'full/031407902bdeff19a2af7d3163aefed119d82c52.jpg',
        #                         'checksum': '277e1d3743656284ce99910973cdca73'})]
        if 'face_img' in item:
            for status, value in results:
                item['face_img'] = value['path']
        # 一定要有return item
        return item
