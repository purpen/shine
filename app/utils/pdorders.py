# -*- coding: utf-8 -*-
import pymongo
import pandas as pd
import numpy as np
from collections import Counter

class PdOrders:
    """
    Use pandas analysis the orders data
    """
    df = None

    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['bigdata']
        self.coll = db['orders']

        # 自动转载数据
        self._read_from_mongo()


    def _read_from_mongo(self, query={}, no_id=True):
        """
        Fetch data from mongo db.
        """
        cursor = self.coll.find(query)

        # expand the cursor and construct the DataFrame
        self.df = pd.DataFrame(list(cursor))

        # 选择需要显示的字段
        # df = df[['aear', 'cate', 'subcate', 'name', 'maxmoney', 'minmoney', 'time']]

        # delete the _id
        if no_id:
            del self.df['_id']


    def order_channel_stats(self):
        """
        生成订单来源分布图
        :return:
        """
        order_channels = self.df.groupby('order_channel')['order_channel'].agg(len)

        return order_channels


    def _get_value(self, id):
        return self.df[self.df['product_id'] == id]['product_name'].values[0]

    def top_product_stats(self,n_top=50):
        """
        生成销售商品TOP50
        """
        group_products = self.df.groupby('product_id')['order_money', 'quantity'].sum()

        total_money = group_products['order_money'].sum()
        top_products = group_products.sort_values(by='order_money', ascending=False)[:n_top]
        top_products['product_id'] = top_products.index
        y_max = top_products.max().values[0]
        top_products = [{
                    'product_id': item[2],
                    'total_money': item[0],
                    'quantity': item[1],
                    'percent': round(item[0]/total_money*100, 2),
                    'name': self._get_value(item[2])} for item in top_products.values]

        return (top_products, total_money, y_max)


    def order_count_hourly(self):
        """
        生成订单每小时变化趋势
        """
        sale_orders = self.df[['ordered_at', 'quantity', 'rid']]
        sale_orders['ordered_at'] = pd.to_datetime(sale_orders['ordered_at'])
        # 对下单时间进行分列，提取订单的小时数据
        time_split = pd.DataFrame((str(x).split(' ') for x in sale_orders.ordered_at),
                                  index=sale_orders.index, columns=['pickup_date', 'pickup_time'])
        # 将分列后的时间字段与原始数据表合并
        sale_orders = pd.merge(sale_orders, time_split, right_index=True, left_index=True)
        sale_orders['pickup_time'] = pd.to_datetime(sale_orders['pickup_time'])
        sale_orders = sale_orders.set_index('pickup_time')
        pickup_time = sale_orders.resample('H').apply(len)
        pickup_time.index = pickup_time.index.strftime('%H')
        group_pickup_time = pickup_time['rid']

        data = []
        for v in group_pickup_time.values:
            data.append([float(v)])

        for index, value in enumerate(group_pickup_time.index):
            data[index].insert(0, value)

        return data


    def order_quantity_stats(self):
        """
        生成订单商品数的分布图
        """
        sale_orders = self.df[['ordered_at', 'quantity', 'rid']]

        bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1000]
        group_quantity = [str(x) + '件' for x in bins if x > 0]

        sale_orders['group_quantity'] = pd.cut(sale_orders['quantity'], bins, labels=group_quantity)
        quantity_stats = sale_orders.groupby('group_quantity')['group_quantity'].agg(len)

        return quantity_stats


    def order_money_stats(self):
        """
        生成订单金额的分布范围
        """
        sale_orders = self.df[['order_money', 'quantity', 'rid']]

        bins = [0, 100, 200, 300, 400, 500, 800, 1000, 2000, 3000]

        group_money = [str(x) for x in bins if x > 0]

        sale_orders['group_money'] = pd.cut(sale_orders['order_money'], bins, labels=group_money)

        money_stats = sale_orders.groupby('group_money')['group_money'].agg(len)

        data = []
        for v in money_stats.values:
            data.append([float(v)])

        for index, value in enumerate(money_stats.index):
            data[index].insert(0, value)

        return data


    def order_count_monthly(self):
        """
        生成每月订单数趋势图
        """
        sale_orders = self.df[['ordered_at', 'quantity', 'rid']]
        # 将下单时间字段更改为时间格式
        sale_orders['ordered_at'] = pd.to_datetime(sale_orders['ordered_at'])
        # 将下单时间字段设置为数据表的索引字段
        sale_orders = sale_orders.set_index('ordered_at')
        # 将按月对数据表中的数据汇总计数
        monthly_order_count = sale_orders['rid'].resample('M').count()

        # result = pd.concat([monthly_order_count, monthly_order_quantity], axis=1)

        data = []
        for v in monthly_order_count.values:
            data.append([float(v)])

        for index, value in enumerate(monthly_order_count.index):
            data[index].insert(0, value.strftime('%Y年%m月'))

        return data


    def order_amount_monthly(self):
        """
        生成每月销售额变化
        """
        sale_orders = self.df[['ordered_at', 'order_money', 'rid']]
        # 将下单时间字段更改为时间格式
        sale_orders['ordered_at'] = pd.to_datetime(sale_orders['ordered_at'])
        # 将下单时间字段设置为数据表的索引字段
        sale_orders = sale_orders.set_index('ordered_at')
        # 将按月对数据表中的数据汇总计数
        monthly_order_amount = sale_orders['order_money'].resample('M').sum()

        data = []
        for v in monthly_order_amount.values:
            data.append([float(v)])

        for index, value in enumerate(monthly_order_amount.index):
            data[index].insert(0, value.strftime('%Y年%m月'))

        return data


    def order_area_stats(self):
        """
        统计销售订单与地域的关系
        """
        address_orders = self.df[['address', 'order_money']]

        p = lambda x: x[:2]

        address_orders['provinces'] = address_orders['address'].map(p)
        group_address = address_orders.groupby('provinces')['order_money'].agg(len)

        group_address = group_address.sort_values(ascending=False)

        data = []
        for v in group_address.values:
            data.append([float(v)])

        for index, value in enumerate(group_address.index):
            data[index].insert(0, value)

        return data


    def repurchase_stats(self):
        """
        复购率统计
        """
        people_orders = self.df[['account', 'ordered_at', 'order_money', 'quantity']]

        group_people_orders = people_orders.groupby('account')['order_money'].agg(len)
        group_people_orders = group_people_orders.sort_values(ascending=True)

        buy_times = Counter(group_people_orders.values)

        # 修正 > 10,累计到10
        for k in buy_times:
            if k > 10:
                buy_times[10] += 1

        return [[k, buy_times[k]] for k in buy_times if k <= 10]