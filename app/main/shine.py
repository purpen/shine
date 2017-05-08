# -*- coding: utf-8 -*-
from flask import g, current_app, request, redirect, url_for, render_template
from flask_login import current_user
from app import babel
from config import LANGUAGES
from app.main import main
from app.models import Rule

@babel.localeselector
def get_locale():
    """
    localeselector装饰器
    在请求之前被调用，当产生响应时，选择使用的语言
    """
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(LANGUAGES.keys())

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


@main.route('/')
def index():
    rules = Rule.objects(enabled=True).all()

    return render_template('index.html', rules=rules)
