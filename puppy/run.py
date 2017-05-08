# -*- coding: utf-8 -*-

import sys, os, logging

from redis import Redis
# scrapy api
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

# add system path
_basedir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(_basedir)

from app.models import Rule
from mongoengine import connect
from puppy.spiders.doggy import DoggySpider
from puppy.settings import *


if __name__ == '__main__':
    settings = get_project_settings()
    configure_logging(settings)

    # connect redis
    r = Redis.from_url(REDIS_URL)
    if not r:
        logging.info('redis connect failed!!!')
        sys.exit(1)

    # connect db
    connect('bigdata', host='127.0.0.1', port=27017)
    rules = Rule.objects(enabled=1).all()
    runner = CrawlerRunner(settings)

    for rule in rules:
        redis_key = rule.name+':start_urls'
        r.lpush(redis_key, rule.start_urls)
        logging.info('rule: %s, allow domains: %s ' % (rule.name, rule.allow_domains))
        runner.crawl(DoggySpider, rule=rule)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()

    logging.info('all finished.')
