# -*- coding: utf-8 -*-
import re, datetime
from urllib.parse import urlparse

import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy_redis.utils import bytes_to_str

from puppy.items import StuffItem

class DoggySpider(RedisCrawlSpider):
    """
    Spider that reads urls from redis queue (doggy:start_urls).
    """
    name = 'doggy'

    # Redis key of the start urls
    #redis_key = 'doggy:start_urls'

    # 保持登录状态
    cookies = {}

    # 发送给服务器的http头信息
    headers = {
        # 'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    # 对请求的返回进行处理配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    start_urls = [
        # 差评黑市
        'http://detail.youzan.com/show/goods/newest?alias=1ybe6arp2oy1z'
        # 遇见美好的店
        'http://detail.youzan.com/show/goods/newest?alias=2xe09s6o5w3xj'
    ]

    #rules = (
        # 最新列表页 http://detail.youzan.com/show/goods?alias=2onv2imrac4on
    #    Rule(LinkExtractor(allow=('show/goods/newest',), )),
        # 宝贝详情页 http://detail.youzan.com/show/goods?alias=2g2ouio6hvlpz
    #    Rule(LinkExtractor(allow=('show/goods\?alias\=([\w]+)',)), callback='parse_item'),
    #)


    def __init__(self, rule):
        self.rule = rule
        self.name = rule.name
        self.redis_key = rule.name + ':start_urls'

        self.allowed_domains = rule.allow_domains.split(',')
        self.start_urls = rule.start_urls.split(',')

        rule_list = []
        # 添加`下一页`的规则
        if rule.next_page:
            rule_list.append(
                Rule(LinkExtractor(restrict_xpaths=rule.next_page))
            )

        # 添加目标详情页的规则
        rule_list.append(Rule(
            LinkExtractor(allow=[rule.allow_url], restrict_xpaths=[rule.extract_from]),
            callback='parse_item')
        )
        self.rules = tuple(rule_list)

        super(DoggySpider, self).__init__()


    def make_request_from_data(self, data):
        """
        从start_urls_key中获取start_url，生成初始request
        """
        self.log('Make a request from data[%s].' % data)

        url = bytes_to_str(data)

        # 带有headers、cookies去请求self.start_urls[0],
        # 返回的response会被送到回调函数parse中
        # yield Request(self.start_urls[0], callback=self.parse, headers=self.headers,
        #              cookies=self.cookies, meta=self.meta)

        return Request(url, callback=self.parse)


    def parse(self, response):
        """
        从列表页提取产品详情Url
        :param response: 返回结果
        """
        self.log('This is an list page! %s' % response.url)

        for p in response.css('.goods-list').xpath('li'):
            url = p.xpath('a/@href').extract_first()
            yield Request(url, callback=self.parse_item)

        # 检查是否有分页
        pagination = response.xpath('//div[@class="pagination"]')
        pagination_next_url = pagination.css('.pagination-next').xpath('@href').extract_first()
        if pagination_next_url:
            self.log('Next url %s append to request!' % pagination_next_url)
            yield Request(pagination_next_url, callback=self.parse)


    def parse_item(self, response):
        """
        根据产品详情页提取数据
        :param response: 返回结果
        """
        self.log('Hi, a item page! %s' % response.url)

        url = response.url

        stuff = StuffItem()

        # 获取产品信息
        stuff['url'] = url
        # 获取alias as id
        stuff['out_number'] = self._get_outer_id(url)
        stuff['title'] = response.xpath(self.rule.title_xpath).extract_first()
        # 销售价 or 优惠价
        sale_price_text = response.xpath(self.rule.price_xpath).extract()
        # 49.00 - 65.00
        sale_prices = sale_price_text[1].split('-')
        stuff['sale_price'] = float(sale_prices[0].strip())
        # 市场价 or 原价
        market_price = response.xpath(self.rule.original_price_xpath).extract()
        if market_price:
            stuff['market_price'] = float(market_price[0].strip())
        else:
            stuff['market_price'] = stuff['sale_price']

        metas = response.xpath(self.rule.meta_xpath).extract_first()
        stuff['metas'] = metas

        # 获取产品图片, 默认选取第一张
        first_image_url = response.xpath(self.rule.image_xpath).extract_first()
        stuff['image_url'] = first_image_url

        stuff['published_at'] = self._get_published_at(first_image_url)
        stuff['last_updated'] = stuff['published_at']
        stuff['from_site'] = self.rule.name

        # 获取店铺信息
        stuff['shop_name'] = response.xpath(self.rule.shop_name_xpath).extract_first()

        # 将创建并赋值好的Item对象传递到PipeLine当中进行处理
        return stuff


    def _get_outer_id(self, url):
        """
        根据Url推测id
        """
        up = urlparse(url)
        for qs in up.query.split('&'):
            param = qs.split('=')
            if param[0] == 'alias':
                return param[1]


    def _get_published_at(self, image_url):
        """
        通过图片创建时间，推测产品上架时间
        """
        sc_time = ''
        grp = re.search(r'.*/(\d{4})/(\d{2})/(\d{2})/.*', image_url)
        if grp:
            res = [int(x) for x in grp.groups()]
            sc_time = datetime.datetime(res[0], res[1], res[2])

        return sc_time