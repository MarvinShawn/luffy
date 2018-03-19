# -*- coding: utf-8 -*-

# Scrapy settings for qiushibaike project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'qiushibaike'

SPIDER_MODULES = ['qiushibaike.spiders']
NEWSPIDER_MODULE = 'qiushibaike.spiders'

MONGO_URI = 'localhost'
MONGO_DB = 'qiushibaike'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qiushibaike (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
  'Cookie':'_xsrf=2|fcc8798e|1fed86277b3dba7290ed47443048f897|1513519767; _ga=GA1.2.1115992353.1513519769; ADEZ_BLOCK_SLOT=FUCKIE; ADEZ_ST=FUCKIE; ADEZ_PVC=1026761-1-jbbbqo0q; _qqq_uuid_="2|1:0|10:1519272590|10:_qqq_uuid_|56:NmVlN2UwYjhjNzZiOGQ5NDBlY2FiM2Q5YzEwN2UyZTdiYzlmYzFlYg==|9005734482c01ac34f5c49a6622deec83a6308910783e18073a6af80e7011581"; _gid=GA1.2.1946717262.1520986512; __cur_art_index=4904; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1521369411,1521376213,1521376230,1521460843; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1521463455; _gat=1'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'qiushibaike.middlewares.QiushibaikeSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#   'qiushibaike.middlewares.JSMiddleware': 543,
#   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None, #禁止内置的中间件
# }


# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'qiushibaike.pipelines.ImgRatioPipeline': 300,
    'qiushibaike.pipelines.MongoDBPipeline': 303,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#这几行注释的作用是，Scrapy会缓存你有的Requests!当你再次请求时，如果存在缓存文档则返回缓存文档，而不是去网站请求
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
