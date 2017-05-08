# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from flask import g, current_app, request, redirect, url_for, render_template
from flask_login import current_user
from app.main import main
from app.models import Rule, Stuff

from app.utils.pdorders import PdOrders
from app.utils.pdstuffs import PdStuffs


@main.route('/stats/<string:id>')
def stats(id):
    rules = Rule.objects(enabled=True).all()
    current_rule = Rule.objects.get_or_404(_id=ObjectId(id))

    pd_stuff = PdStuffs({
        'from_site': current_rule.name
    })

    # 月度变化
    monthly_stats = pd_stuff.stuff_count_monthly()
    # 产品价格分布
    money_stats = pd_stuff.stuff_money_stats()


    # 获取产品列表
    stuff_list = Stuff.objects(from_site=current_rule.name).all()
    total_count = stuff_list.count()

    return render_template('stats/stuff.html',
                           rules=rules,
                           current_rule=current_rule,
                           monthly_stats=monthly_stats,
                           money_stats=money_stats,
                           stuff_list=stuff_list,
                           total_count=total_count,
                        )

@main.route('/stats/jd')
def jd():
    rules = Rule.objects(enabled=True).all()

    p_data = PdOrders()

    # 订单数趋势
    orders_monthly = p_data.order_count_monthly()
    # 销售额趋势
    amount_monthly = p_data.order_amount_monthly()
    # 24小时内
    orders_hourly = p_data.order_count_hourly()

    # 渠道分布图
    data = p_data.order_channel_stats()
    pie = []
    for v in data.values:
        pie.append([float(v)])

    for index, value in enumerate(data.index):
        pie[index].insert(0, value)

    # 客单价范围
    money_stats = p_data.order_money_stats()

    # TOP products
    (top_products, total_money, y_max) = p_data.top_product_stats(100)

    # Area
    area_stats = p_data.order_area_stats()

    # 复购率
    repurchase_stats = p_data.repurchase_stats()

    return render_template('stats/jd.html',
                           rules=rules,
                           amount_monthly=amount_monthly,
                           orders_monthly=orders_monthly,
                           orders_hourly=orders_hourly,
                           money_stats=money_stats,
                           pie=pie,
                           top_products=top_products,
                           area_stats=area_stats,
                           repurchase_stats=repurchase_stats,
                           y_max=y_max
                           )