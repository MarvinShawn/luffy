from scrapy import cmdline
name = "qiushiuser"
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())