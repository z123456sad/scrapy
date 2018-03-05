#coding:utf-8
__author__ = 'cccccc'
__date__ = '2018/2/9 1:27'
from scrapy.cmdline import execute
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy','crawl','lagou'])