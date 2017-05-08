# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StuffItem(scrapy.Item):
    """
    采集产品列表
    """
    # 店铺名称
    shop_name = scrapy.Field()
    # 产品编号
    out_number = scrapy.Field()
    # 名称
    title  = scrapy.Field()
    # 子名称
    sub_title = scrapy.Field()
    # 描述
    desc = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # meta
    metas = scrapy.Field()
    # 缩略图
    image_url = scrapy.Field()
    image = scrapy.Field()
    # 销售价/优惠价
    sale_price = scrapy.Field()
    # 标准价 (无优惠期间，与优惠价相同)
    market_price = scrapy.Field()
    # 点赞数
    love_count = scrapy.Field()
    # 评论数
    comment_count = scrapy.Field()
    # 浏览数
    view_count = scrapy.Field()
    # 链接
    url = scrapy.Field()
    # 库存数
    stock = scrapy.Field()
    # 来源站点
    from_site = scrapy.Field()
    # 上线时间
    published_at = scrapy.Field(serizlizer=str)
    # 更新时间
    last_updated = scrapy.Field(serizlizer=str)


class PuppyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass