# -*- coding: utf-8 -*-
from datetime import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()

class Orders(db.Document):

    rid = db.IntField()
    product_id = db.IntField()
    product_name = db.StringField()
    quantity = db.IntField()
    pay_away = db.StringField()
    jd_price = db.FloatField()
    order_money = db.FloatField()
    checkout_money = db.FloatField()
    remain_money = db.FloatField()
    pay_money = db.FloatField()
    order_status = db.StringField()
    order_type = db.StringField()
    account = db.StringField()
    name = db.StringField()
    address = db.StringField()
    phone = db.IntField()
    summary = db.StringField()

    voice_type = db.StringField(default=None)
    voice_title = db.StringField(default=None)
    voice_body = db.StringField(default=None)

    seller_level = db.FloatField()
    seller_summary = db.StringField()
    freight = db.FloatField()
    payed_time = db.DateTimeField()
    zz_voice = db.StringField()
    # 货物编号
    goods_number = db.StringField(default=None)
    order_ref = db.StringField()
    order_channel = db.StringField()

    finished_time = db.DateTimeField(default=datetime.now)
    ordered_at = db.DateTimeField()


    def __unicode__(self):
        return self.rid


    meta = {
        'ordering': ['-ordered_at'],
        'collection': 'orders',
    }
