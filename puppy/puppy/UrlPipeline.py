# -*- coding: utf-8 -*-
import re
from scrapy.exceptions import DropItem

class UrlPipeline(object):
    """
    Url 过滤器
    """

    def process_item(self, item, spider):
        spider.log('Start spider url pipeline!!!')

        pass
