"""
Author: Eggry
URL: https://github.com/eggry/BiliReplyDetailCrawler
License: MIT License
"""

"""
这段代码可以统计AV85002656某两层评论中各用户的盖楼数，并输出到Excel
"""
import pandas as pd
import openpyxl
from BiliReplyDetailCrawler import get_all_reply

# AV号
oid = 85002656

# 评论ID
roots = [4098373645, 4098382684]

# 所有回复
replies = []

for root in roots:
    reply_list = get_all_reply(oid, root)
    replies.extend(reply_list)

df = pd.DataFrame(replies)
df.groupby(["uid", "name"]).size().sort_values(ascending=False).to_excel("rank.xlsx")