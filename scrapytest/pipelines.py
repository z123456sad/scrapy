# -*- coding: utf-8 -*-
import json
import codecs
import pymysql
from twisted.enterprise import adbapi
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline

class ScrapytestPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonTestPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self,spider):
        self.file.close()


class Mysqlpipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host="192.168.1.131",user="root",password="mysql",db="scrapy_test",port=3306,charset="utf8", use_unicode=True)
        self.cur = self.db.cursor()
    def process_item(self, item, spider):
        a = item["url_object_id"]
        sql_insert ="""insert into jobbole(url_object_id,title,content)  VALUES (%s,%s,%s)"""
        self.cur.execute(sql_insert,(item["url_object_id"],item["title"],item["content"]))
        self.db.commit()

#mysql异步操作
class MysqlAsynchronouspipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dpparms = dict(
        host = settings["MYSQL_HOST"],
        password = settings["MYSQL_PASSWORD"],
        db = settings["MYSQL_DBNAME"],
        user = settings["MYSQL_NAME"],
        charset="utf8",
        use_unicode=True,
        cursorclass = pymysql.cursors.DictCursor
        )
        dbpool = adbapi.ConnectionPool("pymysql",**dpparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.db_insrt,item)
        query.addErrback(self.twisted_error)

    def twisted_error(self,failure):
        print(failure)

    def db_insrt(self,cursor,item):
        a = item["url_object_id"]
        sql_insert ="""insert into jobbole(url_object_id,title,content)  VALUES (%s,%s,%s)"""
        cursor.execute(sql_insert,(item["url_object_id"],item["title"],item["content"]))


class Mysqllagoupipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dpparms = dict(
            host = settings["MYSQL_HOST"],
            password = settings["MYSQL_PASSWORD"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_NAME"],
            charset="utf8",
            use_unicode=True,
            cursorclass = pymysql.cursors.DictCursor
        )
        dbpool = adbapi.ConnectionPool("pymysql",**dpparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.db_insrt,item)
        query.addErrback(self.twisted_error)

    def twisted_error(self,failure):
        print(failure)

    def db_insrt(self,cursor,item):
        a = item["url_object_id"]
        sql_insert ="""insert into lagou_job(url_object_id,title,company,url)  VALUES (%s,%s,%s,%s)"""
        cursor.execute(sql_insert,(item["url_object_id"],item["title"],item["company"],item["url"]))







class ImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_file_path = value["path"]

        item["image_url_path"] = image_file_path
        return item
