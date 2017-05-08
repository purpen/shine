# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RuleForm(FlaskForm):
    site = StringField('Site name')
    name = StringField('Spider name', validators = [DataRequired(), Length(1, 64)])
    allow_domains = StringField()
    start_urls = StringField()
    next_page = StringField()
    allow_url = StringField()
    extract_from = StringField()

    title_xpath = StringField()
    meta_xpath = StringField()
    desc_xpath = StringField()
    image_xpath = StringField()
    price_xpath = StringField()
    original_price_xpath = StringField()
    comment_xpath = StringField()

    shop_name_xpath = StringField()


    enabled = BooleanField('Enabled', default = False)