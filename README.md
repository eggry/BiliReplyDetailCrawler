# BiliReplyDetailCrawler
## 概述
本项目为Bilibili评论区楼中楼API封装了一套Python接口。基于此接口，本项目提供了爬取楼中楼内容、统计用户盖楼数量两个实用例程。此外，本项目还简述了Bilibili评论区楼中楼的API接口调用方法。
## 楼中楼数据接口分析
### 请求接口
api.bilibili.com/x/v2/reply/detail
### 请求方式
GET
### 接口权限
无需登录
### 请求参数
|名称|含义|说明|
|----|----|----|
|oid|AV号||
|root|主楼ID||
|type|请求类型|意义不明，必须为1|
|ps|请求页大小|默认值20，最大值20|
|next|请求起始楼号|楼号从1编号|
### 请求示例
https://api.bilibili.com/x/v2/reply/detail?oid=85002656&root=4098382684&type=1&ps=20&next=6
### 返回格式
`application/json; charset=utf-8`
### 关键返回结果
|名称|含义|说明|
|----|----|----|
|`.code`|返回码|触发风控规则时返回-412|
|`.data.cursor`|记录游标||
|`.data.cursor.is_end`|是否到达楼中楼末尾||
|`.data.cursor.next`|下次请求起始楼号|如果已到达末尾则为0|
|`.data.root.replies`|楼中楼列表||
|`.data.root.replies[index].rpid`|评论ID||
|`.data.root.replies[index].member.uname`|评论者昵称||
|`.data.root.replies[index].member.mid`|评论者UID||
|`.data.root.replies[index].content.message`|楼中楼内容||

## Python API说明
### `get_reply(oid, root, begin=1)`
该函数向Bilibili API请求JSON对象，请求成功则返回JSON转成的`dict`，请求失败则抛出异常。
### `parse_reply(reply_data)`
该函数从`dict`中解析所需数据，返回包含楼中楼信息的`list`和记录游标。如果二次开发时需要解析另外的字段，你可以修改该函数内的``for``循环。
### `get_all_reply(oid, root, print_log=True)`
该函数会获取某回复的所有楼中楼，返回包含楼中楼信息的`list`。当设置`print_log=True`时，每次请求成功会打印一下请求范围。
### `crawl_to_excel(oid, root, format_time=True, print_log=True)`
该函数会爬取某回复的所有楼中楼，并以主楼ID作为文件名输出到Excel中。当设置`print_log=True`时，会将时间戳转为友好格式。`print_log`与`get_all_reply`含义一致
## 安装依赖
```bash
pip install -r requirements.txt 
```
或
```bash
pip install requests
pip install pandas
pip install openpyxl
```
## 使用示例
### 爬取评论楼中楼到Excel (`excel_example.py`)
```python
from crawler import crawl_to_excel

# AV号
oid = 85002656

# 评论ID
roots = [4098373645, 4098382684]

for root in roots:
    crawl_to_excel(oid, root)
```
这段代码可以爬取[av85002656](https://www.bilibili.com/video/av85002656)某两层评论的楼中楼，将结果导出为Excel，同时将时间戳格式化为易读格式。
### 统计评论中各用户的盖楼数到Excel (`count_user_replies_example.py`)
```python
import pandas as pd
import openpyxl
from crawler import get_all_reply

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
```
这段代码可以统计[av85002656](https://www.bilibili.com/video/av85002656)某两层评论中各用户的盖楼数，并输出到Excel。
### 统计Excel中楼中楼内容，提取词云(`wordcloud_example.py`)
这段代码可以读取Excel，统计盖楼关键词，输出词云。
### 在你的程序中引入本接口
```python
import BiliReplyDetailCrawler
```

## 碎碎念
祝心華小姑娘生日快乐！

感谢@叶玖离 组织这次活动，感谢参与的各位，感谢喜欢心華的每一位小伙伴。

如果您喜欢此项目，请多关注Vocaloid歌手心華，请多支持心華的《横竖撇点折》([av85002656](https://www.bilibili.com/video/av85002656))。

此项目根据 MIT 许可的条款进行许可。
