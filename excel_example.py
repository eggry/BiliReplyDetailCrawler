"""
Author: Eggry
URL: https://github.com/eggry/BiliReplyDetailCrawler
License: MIT License
"""

"""
这段代码可以爬取AV85002656某两层评论的楼中楼，将结果导出为Excel，同时将时间戳格式化为易读格式
"""
from BiliReplyDetailCrawler import crawl_to_excel

# AV号
oid = 85002656

# 评论ID
roots = [4098373645, 4098382684]

for root in roots:
    crawl_to_excel(oid, root)