# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyredisbiliPipeline(object):
    def process_item(self, item, spider):
        return item

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


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

