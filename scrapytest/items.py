# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import datetime
from scrapy.loader.processors import TakeFirst,MapCompose
from scrapy.contrib.loader import ItemLoader
from w3lib.html import remove_tags

class ScrapytestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def remove_split(value):
    return value.replace("/","")


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip()!="查看地图"]
    return "".join(addr_list)


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date

def splid(value):
    salary_list =re.split(r"-",value)
    if salary_list.__len__() == 2 and value == 1:
        return salary_list[1]
    pass


class ScrapyLoaderItem(ItemLoader):
    default_output_processor = TakeFirst()





class JobboleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    image_url_path = scrapy.Field()
    front_image_url = scrapy.Field()
    time_date = scrapy.Field(
    input_processor = MapCompose(date_convert)
    )

class LagouItem(scrapy.Item):
    salary = scrapy.Field(
        input_processor = MapCompose(splid)
    )
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    url_object_id =scrapy.Field()
    salary_job_min = scrapy.Field()
    salary_job_max = scrapy.Field()
    address_job = scrapy.Field(
        input_processor = MapCompose(splid)
    )
    work_exp_min = scrapy.Field()
    work_exp_max = scrapy.Field()
    education = scrapy.Field(
        input_processor = MapCompose(splid)
    )
    allure = scrapy.Field()
    company = scrapy.Field(
        input_processor = MapCompose(remove_tags,handle_jobaddr)
        )
    company_url = scrapy.Field()
    company_object_id = scrapy.Field()
    date_time = scrapy.Field()


class LagouLoaderItem(ItemLoader):
    default_output_processor = TakeFirst()