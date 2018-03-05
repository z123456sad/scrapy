# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from scrapytest.items import JobboleItem,ScrapyLoaderItem
from scrapytest.utils.common import get_md5
from datetime import datetime
from scrapy.contrib.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        1提取内容解析
        2提取文章的URl
        #获取下一页url
        next_url = response.css('.next.page-numbers::attr(href)').extract()
        if next_url:
            yield Request(url=parse.urljoin(response.url,post_url),callback=self.parse)
        '''
        #获取所有文章URl
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            post_url = post_node.css('::attr(href)').extract_first("")
            post_image = post_node.css('img::attr(src)').extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":post_image},callback=self.parse_detail)


    def parse_detail(self,response):
        jobbole_item = JobboleItem()
        front_image_url = response.meta.get('front_image_url','')

        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        time_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace('·',"")
        nice = response.xpath('//span[contains(@class,"vote-post-up")]').extract()
        fav_nums = response.xpath('//a[@href="#article-comment"]').extract()
        content = response.xpath('//div[@class="entry"]').extract()[0]


        try:
            time_date = datetime.strptime(time_date,"%Y/%m/%d").date()
        except Exception as e:
            time_date = datetime.now().date()
        jobbole_item["time_date"] = time_date
        jobbole_item["url_object_id"] = get_md5(response.url)
        jobbole_item["title"] = title
        jobbole_item["front_image_url"] = [front_image_url]
        jobbole_item["content"] = content
        jobbole_item["url"] = response.url

        #通过loaditem加载
        loaditem = ScrapyLoaderItem(item=JobboleItem(),response=response)
        loaditem.add_xpath('title','//div[@class="entry-header"]/h1/text()')
        loaditem.add_xpath('time_date','//p[@class="entry-meta-hide-on-mobile"]/text()')
        loaditem.add_xpath('content','//div[@class="entry"]')
        loaditem.add_value('front_image_url',[front_image_url])
        loaditem.add_value('url_object_id',[get_md5(response.url)])
        loaditem.add_value('url',[response.url])
        jobbole_item = loaditem.load_item()
        yield jobbole_item



