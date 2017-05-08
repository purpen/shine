# -*- coding: utf-8 -*-
from datetime import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()

class Rule(db.Document):

    _id = db.StringField()
    # site name
    site = db.StringField(max_length=32)
    # spider name
    name = db.StringField(max_length=32)

    allow_domains = db.StringField()
    start_urls = db.StringField()
    next_page = db.StringField()
    allow_url = db.StringField()
    extract_from = db.StringField()

    title_xpath = db.StringField()
    desc_xpath = db.StringField()
    meta_xpath = db.StringField()
    image_xpath = db.StringField()
    price_xpath = db.StringField()
    original_price_xpath = db.StringField()
    comment_xpath = db.StringField()
    # 店铺名称
    shop_name_xpath = db.StringField()

    enabled = db.IntField()
    created_at = db.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name

    def get_id(self):
        return str(self.id)

    meta = {
        'ordering': ['created_at'],
        'collection': 'rules',
        'strict': True,
        'id_field': '_id'
    }