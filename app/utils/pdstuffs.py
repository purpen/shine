# -*- coding: utf-8 -*-
import pymongo
import pandas as pd
import numpy as np
from collections import Counter

class PdStuffs:
    """
        Use pandas analysis the orders data
        """
    df = None

    def __init__(self, query={}):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['bigdata']
        self.coll = db['stuffs']

        # 自动转载数据
        self._read_from_mongo(query)


    def _read_from_mongo(self, query={}, no_id=True):
        """
        Fetch data from mongo db.
        """
        cursor = self.coll.find(query)

        # expand the cursor and construct the DataFrame
        self.df = pd.DataFrame(list(cursor))

        # delete the _id
        if no_id:
            del self.df['_id']


    def stuff_money_stats(self):
        """
        生成产品价格的分布范围
        """
        money_stuffs = self.df[['sale_price', 'out_number']]

        bins = [0, 100, 200, 300, 400, 500, 800, 1000, 2000, 3000]

        group_money = [str(x) for x in bins if x > 0]

        money_stuffs['group_money'] = pd.cut(money_stuffs['sale_price'], bins, labels=group_money)

        money_stats = money_stuffs.groupby('group_money')['group_money'].agg(len)

        data = []
        for v in money_stats.values:
            data.append([float(v)])

        for index, value in enumerate(money_stats.index):
            data[index].insert(0, value)

        return data


    def stuff_count_monthly(self):
        """
        生成每月上架产品数趋势图
        """
        sale_stuffs = self.df[['published_at', 'out_number']]
        # 将下单时间字段更改为时间格式
        sale_stuffs['published_at'] = pd.to_datetime(sale_stuffs['published_at'])
        # 将下单时间字段设置为数据表的索引字段
        sale_stuffs = sale_stuffs.set_index('published_at')
        # 将按月对数据表中的数据汇总计数
        monthly_order_count = sale_stuffs['out_number'].resample('M').count()

        # result = pd.concat([monthly_order_count, monthly_order_quantity], axis=1)

        data = []
        for v in monthly_order_count.values:
            data.append([float(v)])

        for index, value in enumerate(monthly_order_count.index):
            data[index].insert(0, value.strftime('%y年%m月'))

        return data
