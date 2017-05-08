# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class PuImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['image_url']:
            yield scrapy.Request(item['image_url'])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images')
        item['image'] = image_paths[0]

        return item


class ProductPipeline(object):
    """
    清理HTML数据
    """

    def process_item(self, item, spider):
        return item

