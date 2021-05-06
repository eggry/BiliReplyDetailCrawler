"""
Author: Eggry
URL: https://github.com/eggry/BiliReplyDetailCrawler
License: MIT License
"""

"""
这段代码可以读取Excel，统计包含指定读音的评论数
警告：拼音数据可能不准确，请勿用于生产环境！
WARNING: PINYIN DATA MAY NOT BE ACCURATE, DO NOT USE UNDER PROCUTION ENVIRONMENT!
"""
import pandas as pd
import re
import pypinyin
import os

df = pd.read_excel("4502367846.xlsx")
df["message"] = (
    df["message"]
    .apply(lambda x: re.sub(r"\[.*\]", "", x))
    .apply(lambda x: re.sub(r"回复 @.* :", "", x))
)
df["pinyin"] = df["message"].apply(lambda x: pypinyin.slug(
    x, heteronym=True, errors="ignore", separator=" ", style=pypinyin.Style.NORMAL)+" ")

df["contains"] = df["pinyin"].apply(
    lambda x: ("ye " in x) or ("jiu " in x) or ("li " in x))

df["invalid"] = ""

df.to_excel("all_comment.xlsx")

print("使用invalid列标记无效评论\n")

os.startfile("all_comment.xlsx")

os.system("pause")

df = pd.read_excel("all_comment.xlsx")

df[(df["contains"] == True) & (df["invalid"].isnull())].groupby(
    ["uid", "name"]).size().sort_values(ascending=False).to_excel("rank.xlsx")
