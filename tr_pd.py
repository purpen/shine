#!venv/bin/python
# -*- coding: utf-8 -*-
import os, sys, json, logging, re
from bson.objectid import ObjectId
import pandas as pd

# add system path
_basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(_basedir)

from app.models import Orders
from mongoengine import connect

connect('bigdata', host='127.0.0.1', port=27017)

fields = [
    'rid', 'product_id', 'product_name', 'quantity', 'pay_away', 'ordered_at', 'jd_price', 'order_money', 'checkout_money',
    'remain_money', 'pay_money', 'order_status', 'order_type', 'account', 'name', 'address', 'phone', 'summary',
    'voice_type', 'voice_title', 'voice_body', 'seller_summary', 'freight', 'payed_time', 'zz_voice', 'goods_number',
    'finished_time', 'order_ref', 'order_channel'
]

columns = {
    '订单号': 'rid',
    '商品ID': 'product_id',
    '商品名称': 'product_name',
    '订购数量': 'quantity',
    '支付方式': 'pay_away',
    '下单时间': 'ordered_at',
    '京东价': 'jd_price',
    '订单金额': 'order_money',
    '结算金额': 'checkout_money',
    '余额支付': 'remain_money',
    '应付金额': 'pay_money',
    '订单状态': 'order_status',
    '订单类型': 'order_type',
    '下单帐号': 'account',
    '客户姓名': 'name',
    '客户地址': 'address',
    '联系电话': 'phone',
    '订单备注': 'summary',
    '发票类型': 'voice_type',
    '发票抬头': 'voice_title',
    '发票内容': 'voice_body',
    '商家备注': 'seller_summary',
    '商家备注等级（等级1-5为由高到低）': 'seller_level',
    '运费金额': 'freight',
    '付款确认时间': 'payed_time',
    '增值税发票': 'zz_voice',
    '货号': 'goods_number',
    '订单完成时间': 'finished_time',
    '订单来源': 'order_ref',
    '订单渠道': 'order_channel'
}

def read_excel(file):
    """
    read from excel file
    """
    df = pd.read_excel(file)
    df.rename(columns=columns, inplace=True)
    data_json = json.loads(df.to_json(orient='records',date_format='iso',date_unit='s'))

    fields = Orders._fields
    counter = 0
    for item in data_json:
        # 验证是否已导入
        if Orders.objects(rid=item.get('rid')).first():
            print('Skip....')
            continue

        print('Item: %s.' % item)

        for k in item.keys():
            if item[k] is None and k not in ['seller_level','finished_time','phone','seller_summary','payed_time']:
                item[k] = ''

        order = Orders()

        order.rid = item.get('rid')
        order.product_id = item.get('product_id')
        order.product_name = item.get('product_name')
        order.quantity = item.get('quantity')
        order.pay_away = item.get('pay_away')
        order.jd_price = item.get('jd_price')
        order.order_money = item.get('order_money')
        order.checkout_money = item.get('checkout_money')
        order.remain_money = item.get('remain_money')
        order.pay_money = item.get('pay_money')
        order.order_status = item.get('order_status')
        order.order_type = item.get('order_type')

        order.account = str(item.get('account'))

        order.name = item.get('name')
        order.address = item.get('address')
        phone = re.sub(r'\D', "", item.get('phone'))
        if phone is None or phone == '':
            phone = 0
        order.phone = phone
        order.summary = item.get('summary', '')

        order.voice_type = item.get('voice_type')
        order.voice_title = item.get('voice_title')
        order.voice_body = item.get('voice_body')

        if item.get('seller_level') is None:
            item['seller_level'] = 0.0
        order.seller_level = item.get('seller_level')

        order.seller_summary = str(item.get('seller_summary'))

        order.freight = item.get('freight')
        order.payed_time = item.get('payed_time')
        order.zz_voice = item.get('zz_voice')
        # 货物编号
        order.goods_number = item.get('goods_number', '')
        order.order_ref = item.get('order_ref')
        order.order_channel = item.get('order_channel')

        order.finished_time = item.get('finished_time')
        order.ordered_at = item.get('ordered_at')

        order.save()

        counter += 1

        print('Total count [%d] to save.' % counter)


if __name__ == '__main__':
    file = _basedir + '/data/201607_12-JD.xlsx'
    read_excel(file)
