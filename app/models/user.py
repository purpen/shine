# -*- coding: utf-8 -*-
from datetime import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()

class User(db.Document):

    account = db.StringField(max_value=20, required=True, unique=True)
    password = db.StringField(max_value=20)
    nickname = db.StringField(max_length=64)
    type = db.IntField(default=1)
    role_id = db.IntField(default=1)
    status = db.IntField(default=1)

    # 软删除
    deleted = db.IntField(default=0)

    token = db.StringField(max_value=20, required=True, unique=True)

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.now)


    def get_id(self):
        return str(self.id)

    def __unicode__(self):
        return self.account


    meta = {
        'ordering': ['-created_at']
    }