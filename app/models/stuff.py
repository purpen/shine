# -*- coding: utf-8 -*-

from datetime import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()

class Stuff(db.Document):

    # 店铺名称
    shop_name = db.StringField()
    # 产品编号
    out_number = db.StringField()
    # 名称
    title = db.StringField()
    # 子名称
    sub_title = db.StringField()
    # 描述
    desc = db.StringField()
    # 标签
    tags = db.StringField()
    # meta
    metas = db.StringField()
    # 缩略图
    image_url = db.StringField()
    image = db.StringField()
    # 销售价/优惠价
    sale_price = db.FloatField()
    # 标准价 (无优惠期间，与优惠价相同)
    market_price = db.FloatField()
    # 点赞数
    love_count = db.IntField(default=0)
    # 评论数
    comment_count = db.IntField(default=0)
    # 浏览数
    view_count = db.IntField(default=0)
    # 链接
    url = db.StringField()
    # 库存数
    stock = db.IntField(default=0)
    # 来源站点
    from_site = db.StringField()
    # 上线时间
    published_at = db.DateTimeField(default=datetime.now)
    # 更新时间
    last_updated = db.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.title

    meta = {
        'ordering': ['-published_at'],
        'collection': 'stuffs',
    }