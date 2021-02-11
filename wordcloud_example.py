"""
Author: Eggry
URL: https://github.com/eggry/BiliReplyDetailCrawler
License: MIT License
"""

"""
这段代码可以读取Excel，统计盖楼关键词，输出词云
requirements:
停止词表    hit_stopwords.txt
中文字体    font.ttf
用户词表    userdict.txt
"""
import pandas as pd
import re
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

df1 = pd.read_excel("4098373645.xlsx")
df2 = pd.read_excel("4098382684.xlsx")
df = pd.concat([df1, df2])
x = (
    df["message"]
    .apply(lambda x: re.sub(r"\[.*\]", "", x))
    .apply(lambda x: re.sub(r"回复 @.* :", "", x))
)
jieba.load_userdict("userdict.txt")
words = []
for msg in x:
    words.extend(jieba.cut(msg))

with open("hit_stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = f.read().splitlines()


words = [word for word in words if word not in stopwords and len(word) > 1]
rank = pd.DataFrame(words).groupby(0).size().sort_values(ascending=False)
wc = WordCloud(
    background_color=None,  # 背景颜色
    max_words=500,  # 词云显示的最大词数
    font_path="font.ttf",
    max_font_size=50,  # 字体最大值
    random_state=233,
    scale=8,
    width=500,
    height=500,
    margin=2,
    mode="RGBA",
)
wc.generate_from_frequencies(rank)
wc.to_file("wordcloud.png")