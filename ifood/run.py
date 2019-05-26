from scrapy.cmdline import execute
try:
    execute(
        [
            'scrapy',
            'crawl',
            'ifood_spider',
            '-o',
            'out.json',
        ]
    )
except SystemExit:
    pass