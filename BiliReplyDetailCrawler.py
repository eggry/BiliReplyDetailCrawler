"""
Author: Eggry
URL: https://github.com/eggry/BiliReplyDetailCrawler
License: MIT License
"""

import requests
import pandas as pd
import openpyxl
from time import localtime, strftime

api_url = "https://api.bilibili.com/x/v2/reply/detail?type=1&oid={oid}&root={root}&next={begin}"


def get_reply(oid, root, begin=1):
    request_url = api_url.format(oid=oid, root=root, begin=begin)
    r = requests.get(request_url)
    r.raise_for_status()
    return r.json()


def parse_reply(reply_data):
    next_cursor = reply_data["data"]["cursor"]
    reply_list = []
    if reply_data["data"]["root"]["replies"] is not None:
        for reply in reply_data["data"]["root"]["replies"]:
            now = {}
            member = reply["member"]
            content = reply["content"]
            now["id"] = reply["rpid"]
            now["time"] = reply["ctime"]
            now["uid"] = member["mid"]
            now["name"] = member["uname"]
            now["message"] = content["message"]
            reply_list.append(now)
    return reply_list, next_cursor


def get_all_reply(oid, root, print_log=True):
    all_reply = []
    begin = 1
    is_end = False
    while not is_end:
        reply_data = get_reply(oid, root, begin)
        reply_list, next_cursor = parse_reply(reply_data)
        all_reply.extend(reply_list)
        if print_log:
            print(
                "begin:",
                begin,
                "next",
                next_cursor["next"],
                "end:",
                next_cursor["is_end"],
            )
        begin = next_cursor["next"]
        is_end = next_cursor["is_end"]
    return all_reply


def crawl_to_excel(oid, root, format_time=True, print_log=True):
    reply = get_all_reply(oid, root, print_log)
    df = pd.DataFrame(reply)
    df.set_index("id", inplace=True)
    if format_time:
        df["time"] = df["time"].apply(
            lambda x: strftime("%Y-%m-%d %H:%M:%S", localtime(x))
        )
    df.to_excel("{root}.xlsx".format(root=root))