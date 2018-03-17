from scrapy import cmdline
name = "qiushi"
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())