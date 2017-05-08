# -*- coding: utf-8 -*-

from datetime import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()

post_status = (
    (0, 'draft'),
    (1, 'published')
)

class Post(db.Document):

    title = db.StringField(required=True, max_length=64)
    content = db.StringField(required=True)
    author = db.StringField()
    tags = db.ListField(db.StringField(max_length=64))
    status = db.IntField(required=True, choices=post_status)
    created_at = db.DateTimeField(default=datetime.now)
    updated_at = db.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.title

    meta = {
        'ordering': ['-created_time']
    }
